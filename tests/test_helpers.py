#!/usr/bin/env python3
"""Shared test helpers, environment managers, and inspection utilities for E2E tests."""

import os
import sys
import re
import json
import time
import zipfile
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Base Project Paths
PROJECT_ROOT = Path('/lzcapp/document/academic_english_book')
REPO_ROOT = Path('/lzcapp/document')
STYLE_FILE = PROJECT_ROOT / 'style' / 'academic_book_style.tex'
BUILD_SCRIPT = PROJECT_ROOT / 'build.sh'
MAKEFILE = PROJECT_ROOT / 'Makefile'
MAIN_TEX = PROJECT_ROOT / 'main.tex'
CHAPTERS_DIR = PROJECT_ROOT / 'chapters'
ASSETS_DIR = PROJECT_ROOT / 'assets'
RAW_TRAINING_DIR = ASSETS_DIR / 'raw_training'
RAW_MASTERY_DIR = ASSETS_DIR / 'raw_mastery'
BUILD_DIR = PROJECT_ROOT / 'build'
DELIVERABLE_PDF = PROJECT_ROOT / 'academic_english_book.pdf'

# Source Zip Paths
TRAINING_ZIP = REPO_ROOT / 'academic_english_training.zip'
MASTERY_ZIP = REPO_ROOT / 'academic_paragraph_and_essay_mastery.zip'

# Reference Rendering & TeX Live Paths
TEXLIVE_BIN = Path('/home/guangdai/.local/share/papers-pdf-texlive/2026/bin/x86_64-linux')
RUNTIME_BIN = Path('/home/guangdai/.local/share/papers-pdf-runtime/usr/bin')
RUNTIME_LIB = Path('/home/guangdai/.local/share/papers-pdf-runtime/usr/lib')
FONTCONFIG_FILE = Path('/home/guangdai/.local/share/papers-pdf-runtime/etc/fonts/fonts.conf')
RENDERING_VENV_PYTHON = Path('/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/.venv-toolkit-20261025/bin/python')


def get_tex_env() -> Dict[str, str]:
    """Construct an execution environment with user-space TeX Live and Fontconfig injected."""
    env = os.environ.copy()
    current_path = env.get('PATH', '')
    injected_paths = []
    if TEXLIVE_BIN.is_dir():
        injected_paths.append(str(TEXLIVE_BIN))
    if RUNTIME_BIN.is_dir():
        injected_paths.append(str(RUNTIME_BIN))
    if injected_paths:
        env['PATH'] = ':'.join(injected_paths) + ':' + current_path

    if RUNTIME_LIB.is_dir():
        current_ld = env.get('LD_LIBRARY_PATH', '')
        env['LD_LIBRARY_PATH'] = str(RUNTIME_LIB) + (':' + current_ld if current_ld else '')

    if FONTCONFIG_FILE.is_file():
        env['FONTCONFIG_FILE'] = str(FONTCONFIG_FILE)

    style_dir = PROJECT_ROOT / 'style'
    current_texinputs = env.get('TEXINPUTS', '')
    env['TEXINPUTS'] = f".:{style_dir}:{PROJECT_ROOT}:{current_texinputs}"

    return env


class CompilationResult:
    """Encapsulates the result of a XeLaTeX compilation run."""
    def __init__(self, returncode: int, stdout: str, stderr: str, log_text: str,
                 pdf_path: Optional[Path], duration: float):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.log_text = log_text
        self.pdf_path = pdf_path
        self.duration = duration
        self.pdf_exists = pdf_path is not None and pdf_path.is_file() and pdf_path.stat().st_size > 0
        self.pdf_size = pdf_path.stat().st_size if self.pdf_exists else 0

        # Heuristic counters from TeX log
        self.overfull_count = len(re.findall(r'Overfull \\[hv]box', log_text))
        self.underfull_count = len(re.findall(r'Underfull \\[hv]box', log_text))
        self.missing_char_count = len(re.findall(r'Missing character:', log_text))
        self.undefined_ref_count = len(re.findall(r'LaTeX Warning: Reference [^\n]+ undefined', log_text))
        self.fatal_error = (returncode != 0) or ('Fatal error occurred' in log_text) or ('Emergency stop' in log_text)


def compile_tex_snippet(tex_code: str, jobname: str = "test_doc", timeout: int = 35) -> CompilationResult:
    """Compile a standalone TeX snippet in an isolated temporary directory using XeLaTeX."""
    env = get_tex_env()
    start_time = time.time()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        tex_file = tmppath / f"{jobname}.tex"
        tex_file.write_text(tex_code, encoding='utf-8')

        cmd = [
            'xelatex',
            '-interaction=nonstopmode',
            '-halt-on-error',
            f'-output-directory={tmpdir}',
            str(tex_file)
        ]

        try:
            proc = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True, timeout=timeout)
            duration = time.time() - start_time
            log_file = tmppath / f"{jobname}.log"
            log_text = log_file.read_text(encoding='utf-8', errors='replace') if log_file.exists() else ""
            pdf_file = tmppath / f"{jobname}.pdf"
            
            # If PDF exists, copy it to a persistent temp location so caller can inspect
            temp_pdf_dest = None
            if pdf_file.exists() and pdf_file.stat().st_size > 0:
                fd, dest_str = tempfile.mkstemp(suffix=".pdf", prefix=f"{jobname}_")
                os.close(fd)
                temp_pdf_dest = Path(dest_str)
                temp_pdf_dest.write_bytes(pdf_file.read_bytes())

            return CompilationResult(
                returncode=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                log_text=log_text,
                pdf_path=temp_pdf_dest,
                duration=duration
            )
        except subprocess.TimeoutExpired:
            return CompilationResult(
                returncode=-1,
                stdout="",
                stderr="Compilation timed out",
                log_text="",
                pdf_path=None,
                duration=time.time() - start_time
            )


class PDFInspectionResult:
    """Encapsulates extracted PDF document metadata, page count, and outline tree."""
    def __init__(self, page_count: int = 0, bookmarks: Optional[List[Tuple[int, str, int]]] = None,
                 text_by_page: Optional[List[str]] = None, links: Optional[List[Dict[str, Any]]] = None,
                 is_valid: bool = False, extractor: str = "none"):
        self.page_count = page_count
        self.bookmarks = bookmarks or []  # List of (level, title, target_page_1_indexed)
        self.text_by_page = text_by_page or []
        self.links = links or []
        self.is_valid = is_valid
        self.extractor = extractor


def inspect_pdf(pdf_path: Path) -> PDFInspectionResult:
    """Extract structural data, page count, outlines, and text from a PDF file."""
    if not pdf_path.is_file():
        return PDFInspectionResult(is_valid=False)

    # Strategy 1: Attempt direct import of fitz (PyMuPDF) in current Python process
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        page_count = len(doc)
        bookmarks = []
        for item in doc.get_toc(simple=True):
            # item is [level, title, page] (1-indexed page)
            bookmarks.append((int(item[0]), str(item[1]), int(item[2])))
        
        text_by_page = [doc[i].get_text() for i in range(page_count)]
        links = []
        for i in range(page_count):
            for link in doc[i].get_links():
                links.append({
                    'from_page': i + 1,
                    'kind': link.get('kind'),
                    'target_page': link.get('page', -1) + 1 if link.get('page') is not None else None
                })
        doc.close()
        return PDFInspectionResult(
            page_count=page_count,
            bookmarks=bookmarks,
            text_by_page=text_by_page,
            links=links,
            is_valid=True,
            extractor="fitz_native"
        )
    except ImportError:
        pass

    # Strategy 2: Attempt running via the dedicated rendering venv Python containing PyMuPDF
    if RENDERING_VENV_PYTHON.is_file():
        script = r'''
import sys, json, fitz

pdf_path = sys.argv[1]
doc = fitz.open(pdf_path)
data = {
    "page_count": len(doc),
    "bookmarks": [[int(i[0]), str(i[1]), int(i[2])] for i in doc.get_toc(simple=True)],
    "text_by_page": [doc[i].get_text() for i in range(len(doc))],
    "links": [{"from_page": i + 1, "kind": l.get("kind"), "target_page": (l.get("page", -1) + 1) if l.get("page") is not None else None} for i in range(len(doc)) for l in doc[i].get_links()]
}
print(json.dumps(data))
'''
        try:
            res = subprocess.run([str(RENDERING_VENV_PYTHON), '-c', script, str(pdf_path)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
            if res.returncode == 0:
                d = json.loads(res.stdout)
                bookmarks = [(int(b[0]), str(b[1]), int(b[2])) for b in d.get("bookmarks", [])]
                return PDFInspectionResult(
                    page_count=d.get("page_count", 0),
                    bookmarks=bookmarks,
                    text_by_page=d.get("text_by_page", []),
                    links=d.get("links", []),
                    is_valid=True,
                    extractor="fitz_venv_subprocess"
                )
        except Exception:
            pass

    # Strategy 3: Fallback native PDF parser (binary inspection)
    try:
        raw_bytes = pdf_path.read_bytes()
        # Count pages via /Type /Page
        page_matches = re.findall(rb'/Type\s*/Page\b', raw_bytes)
        page_count = len(page_matches)
        
        # Extract title bookmarks via /Title (...)
        raw_titles = re.findall(rb'/Title\s*\((.*?)\)', raw_bytes)
        bookmarks = []
        for t in raw_titles:
            try:
                title_str = t.decode('utf-8', errors='ignore')
                bookmarks.append((1, title_str, 1))
            except Exception:
                pass

        return PDFInspectionResult(
            page_count=page_count,
            bookmarks=bookmarks,
            text_by_page=[],
            links=[],
            is_valid=page_count > 0,
            extractor="native_fallback"
        )
    except Exception:
        return PDFInspectionResult(is_valid=False)


def read_json_from_zip(zip_path: Path, internal_path: str) -> Optional[Any]:
    """Read and parse a JSON file directly from a zip archive without extracting to disk."""
    if not zip_path.is_file():
        return None
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            with zf.open(internal_path) as f:
                return json.load(f)
    except Exception:
        return None


def get_zip_namelist(zip_path: Path) -> List[str]:
    """Get list of all internal file paths in a zip archive."""
    if not zip_path.is_file():
        return []
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            return zf.namelist()
    except Exception:
        return []


class TestResult:
    """Standardized result of an individual test case."""
    def __init__(self, test_id: str, tier: int, name: str, status: str,
                 message: str = "", duration: float = 0.0, feature_id: str = ""):
        self.test_id = test_id
        self.tier = tier
        self.name = name
        self.status = status  # 'PASS', 'FAIL', 'SKIP'
        self.message = message
        self.duration = duration
        self.feature_id = feature_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            'test_id': self.test_id,
            'tier': self.tier,
            'feature_id': self.feature_id,
            'name': self.name,
            'status': self.status,
            'message': self.message,
            'duration_ms': round(self.duration * 1000, 2)
        }
