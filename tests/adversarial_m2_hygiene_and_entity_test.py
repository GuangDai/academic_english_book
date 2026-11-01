#!/usr/bin/env python3
"""Adversarial Milestone 2 Verification Suite: Data Ingestion Completeness & Character Hygiene.

Executed by teamwork_challenger_m2_1.
Empirically tests:
1. Exact counts and complete presence of:
   - 36 Grammar Rules (G001–G036) in chapters/part2_syntax.tex
   - 24 Expression Patterns (EP001–EP024) in chapters/part2_syntax.tex
   - 30 Logic Rules (L001–L030) in chapters/part3_discourse.tex
   - 48 Paragraph Blueprints (BP01–BP48) in chapters/part4_blueprints.tex
   - 60 Revision Cases (RC01–RC60) in chapters/part5_revision_clinic.tex
   - 24 Full Text Compositions (FT01–FT24) in chapters/part6_anthology.tex
2. Adversarial Character Hygiene across all files in chapters/:
   - Unicode circled numbers (①–⑳, U+2460–U+24FF, U+3251–U+32BF, U+2776–U+2793)
   - Currency dollar signs ($40 million vs \\$40 million)
   - Unescaped underscores (_) outside math and labels
   - Unescaped hashes (#) outside \\#
   - Unescaped ampersands (&) outside tabular/alignment environments
   - Unescaped percent signs (%) and PDF content truncation check
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "chapters"
ASSETS_DIR = PROJECT_ROOT / "assets"
PDF_PATH = PROJECT_ROOT / "academic_english_book.pdf"
if not PDF_PATH.exists() and (PROJECT_ROOT / "build" / "main.pdf").exists():
    PDF_PATH = PROJECT_ROOT / "build" / "main.pdf"



def test_grammar_rules_ingestion() -> Dict[str, Any]:
    raw_path = ASSETS_DIR / "raw_training" / "grammar_rules.json"
    tex_path = CHAPTERS_DIR / "part2_syntax.tex"
    with open(raw_path, encoding="utf-8") as f:
        gr_raw = json.load(f)
    tex_content = tex_path.read_text(encoding="utf-8")
    
    expected_ids = [item["grammar_id"] for item in gr_raw]
    missing_subsections = []
    missing_labels = []
    
    for gid in expected_ids:
        if not re.search(r"\\subsection\{" + re.escape(gid) + r":", tex_content):
            missing_subsections.append(gid)
        if f"\\label{{sec:rule:{gid}}}" not in tex_content:
            missing_labels.append(gid)
            
    passed = len(missing_subsections) == 0 and len(missing_labels) == 0 and len(expected_ids) == 36
    return {
        "name": "Grammar Rules Ingestion (G001–G036)",
        "expected_count": 36,
        "found_subsections": len(expected_ids) - len(missing_subsections),
        "found_labels": len(expected_ids) - len(missing_labels),
        "missing_subsections": missing_subsections,
        "missing_labels": missing_labels,
        "passed": passed
    }


def test_expression_patterns_ingestion() -> Dict[str, Any]:
    raw_path = ASSETS_DIR / "raw_training" / "expression_patterns.json"
    tex_path = CHAPTERS_DIR / "part2_syntax.tex"
    with open(raw_path, encoding="utf-8") as f:
        ep_raw = json.load(f)
    tex_content = tex_path.read_text(encoding="utf-8")
    
    expected_ids = [item["pattern_id"] for item in ep_raw]
    missing_subsections = []
    missing_labels = []
    
    for epid in expected_ids:
        if not re.search(r"\\subsection\{" + re.escape(epid) + r":", tex_content):
            missing_subsections.append(epid)
        if f"\\label{{sec:ep:{epid}}}" not in tex_content:
            missing_labels.append(epid)
            
    passed = len(missing_subsections) == 0 and len(missing_labels) == 0 and len(expected_ids) == 24
    return {
        "name": "Expression Patterns Ingestion (EP001–EP024)",
        "expected_count": 24,
        "found_subsections": len(expected_ids) - len(missing_subsections),
        "found_labels": len(expected_ids) - len(missing_labels),
        "missing_subsections": missing_subsections,
        "missing_labels": missing_labels,
        "passed": passed
    }


def test_logic_rules_ingestion() -> Dict[str, Any]:
    raw_path = ASSETS_DIR / "raw_mastery" / "blueprints" / "logic_and_argumentation_engine.json"
    tex_path = CHAPTERS_DIR / "part3_discourse.tex"
    with open(raw_path, encoding="utf-8") as f:
        la_raw = json.load(f)
    tex_content = tex_path.read_text(encoding="utf-8")
    
    expected_ids = [item["logic_id"] for item in la_raw]
    missing_subsections = []
    missing_labels = []
    
    for lid in expected_ids:
        if not re.search(r"\\subsection\{" + re.escape(lid) + r":", tex_content):
            missing_subsections.append(lid)
        if f"\\label{{sec:logic:{lid}}}" not in tex_content:
            missing_labels.append(lid)
            
    passed = len(missing_subsections) == 0 and len(missing_labels) == 0 and len(expected_ids) == 30
    return {
        "name": "Logic Rules Ingestion (L001–L030)",
        "expected_count": 30,
        "found_subsections": len(expected_ids) - len(missing_subsections),
        "found_labels": len(expected_ids) - len(missing_labels),
        "missing_subsections": missing_subsections,
        "missing_labels": missing_labels,
        "passed": passed
    }


def test_paragraph_blueprints_ingestion() -> Dict[str, Any]:
    raw_path = ASSETS_DIR / "raw_mastery" / "blueprints" / "intent_to_paragraph_blueprints.json"
    tex_path = CHAPTERS_DIR / "part4_blueprints.tex"
    with open(raw_path, encoding="utf-8") as f:
        bp_raw = json.load(f)
    tex_content = tex_path.read_text(encoding="utf-8")
    
    expected_ids = [item["blueprint_id"] for item in bp_raw]
    missing_subsections = []
    missing_labels = []
    
    for bpid in expected_ids:
        if not re.search(r"\\subsection\{" + re.escape(bpid) + r":", tex_content):
            missing_subsections.append(bpid)
        if f"\\label{{sec:bp:{bpid}}}" not in tex_content:
            missing_labels.append(bpid)
            
    passed = len(missing_subsections) == 0 and len(missing_labels) == 0 and len(expected_ids) == 48
    return {
        "name": "Paragraph Blueprints Ingestion (BP01–BP48)",
        "expected_count": 48,
        "found_subsections": len(expected_ids) - len(missing_subsections),
        "found_labels": len(expected_ids) - len(missing_labels),
        "missing_subsections": missing_subsections,
        "missing_labels": missing_labels,
        "passed": passed
    }


def test_revision_clinic_ingestion() -> Dict[str, Any]:
    raw_path = ASSETS_DIR / "raw_mastery" / "blueprints" / "revision_clinic_atlas.json"
    tex_path = CHAPTERS_DIR / "part5_revision_clinic.tex"
    with open(raw_path, encoding="utf-8") as f:
        rc_raw = json.load(f)
    tex_content = tex_path.read_text(encoding="utf-8")
    
    expected_ids = [item["case_id"] for item in rc_raw]
    missing_subsections = []
    missing_labels = []
    
    for rcid in expected_ids:
        if not re.search(r"\\subsection\{Case " + re.escape(rcid) + r":", tex_content):
            missing_subsections.append(rcid)
        if f"\\label{{case:{rcid}}}" not in tex_content:
            missing_labels.append(rcid)
            
    passed = len(missing_subsections) == 0 and len(missing_labels) == 0 and len(expected_ids) == 60
    return {
        "name": "Revision Clinic Cases Ingestion (RC01–RC60)",
        "expected_count": 60,
        "found_subsections": len(expected_ids) - len(missing_subsections),
        "found_labels": len(expected_ids) - len(missing_labels),
        "missing_subsections": missing_subsections,
        "missing_labels": missing_labels,
        "passed": passed
    }


def test_full_text_anthology_ingestion() -> Dict[str, Any]:
    tex_path = CHAPTERS_DIR / "part6_anthology.tex"
    tex_content = tex_path.read_text(encoding="utf-8")
    expected_ids = [f"FT{i:02d}" for i in range(1, 25)]
    missing_sections = []
    missing_labels = []
    
    for ftid in expected_ids:
        if not re.search(r"\\section\{" + re.escape(ftid) + r":", tex_content):
            missing_sections.append(ftid)
        if f"\\label{{comp:{ftid}}}" not in tex_content:
            missing_labels.append(ftid)
            
    passed = len(missing_sections) == 0 and len(missing_labels) == 0 and len(expected_ids) == 24
    return {
        "name": "Full Text Anthology Ingestion (FT01–FT24)",
        "expected_count": 24,
        "found_sections": len(expected_ids) - len(missing_sections),
        "found_labels": len(expected_ids) - len(missing_labels),
        "missing_sections": missing_sections,
        "missing_labels": missing_labels,
        "passed": passed
    }


def test_circled_numbers_hygiene() -> Dict[str, Any]:
    violations = []
    for tex_file in sorted(CHAPTERS_DIR.glob("*.tex")):
        lines = tex_file.read_text(encoding="utf-8").splitlines()
        for line_no, line in enumerate(lines, start=1):
            for ch in line:
                code = ord(ch)
                if (0x2460 <= code <= 0x24FF or 
                    0x3251 <= code <= 0x32BF or 
                    0x2776 <= code <= 0x2793):
                    violations.append({
                        "file": tex_file.name,
                        "line": line_no,
                        "char": ch,
                        "codepoint": f"U+{code:04X}"
                    })
    return {
        "name": "Unicode Circled Numbers Hygiene (①–⑳)",
        "violations_count": len(violations),
        "violations": violations,
        "passed": len(violations) == 0
    }


def test_unescaped_special_chars() -> Dict[str, Any]:
    violations_pct = []
    violations_amp = []
    violations_und = []
    violations_hash = []
    violations_curr = []
    
    align_envs = ["tabular", "tabularx", "longtable", "align", "align*", "matrix", "bmatrix", "pmatrix", "cases", "split"]
    
    for tex_file in sorted(CHAPTERS_DIR.glob("*.tex")):
        lines = tex_file.read_text(encoding="utf-8").splitlines()
        in_align = 0
        for line_no, line in enumerate(lines, start=1):
            # Check unescaped %
            for m in re.finditer(r"(?<!\\)(?:\\\\)*%", line):
                idx = m.end() - 1
                before = line[:idx]
                if before.strip():  # inline %
                    violations_pct.append({
                        "file": tex_file.name,
                        "line": line_no,
                        "col": idx,
                        "snippet": line[max(0, idx - 25):min(len(line), idx + 35)]
                    })
            
            # Check comment for stripping subsequent syntax checks
            comment_idx = -1
            for i, ch in enumerate(line):
                if ch == "%" and (i == 0 or line[i-1] != "\\"):
                    comment_idx = i
                    break
            code_part = line[:comment_idx] if comment_idx >= 0 else line
            
            # Check & outside alignment
            for env in align_envs:
                if f"\\begin{{{env}}}" in code_part:
                    in_align += 1
                if f"\\end{{{env}}}" in code_part:
                    in_align = max(0, in_align - 1)
            if in_align == 0:
                s_amp = re.sub(r"\\&", "", code_part)
                if "&" in s_amp:
                    violations_amp.append({
                        "file": tex_file.name,
                        "line": line_no,
                        "snippet": line.strip()[:80]
                    })
            
            # Check _ outside math and label/ref
            s_und = re.sub(r"\\_", "", code_part)
            s_und = re.sub(r"\$[^$]+\$", "", s_und)
            s_und = re.sub(r"\\(label|ref|pageref|input|include)\{[^}]*\}", "", s_und)
            if "_" in s_und:
                violations_und.append({
                    "file": tex_file.name,
                    "line": line_no,
                    "snippet": line.strip()[:80]
                })
                
            # Check # outside \#
            s_hash = re.sub(r"\\#", "", code_part)
            if "#" in s_hash:
                violations_hash.append({
                    "file": tex_file.name,
                    "line": line_no,
                    "snippet": line.strip()[:80]
                })
                
            # Check currency $ e.g. $40 million instead of \$40 million
            for m in re.finditer(r"(?<!\\)\$(?:\s*)(\d+(?:\.\d+)?\s*(?:million|billion|trillion|USD|dollars?))", code_part, re.IGNORECASE):
                violations_curr.append({
                    "file": tex_file.name,
                    "line": line_no,
                    "match": m.group(0),
                    "snippet": line.strip()[:80]
                })
                
    return {
        "name": "Special Character Escaping Hygiene",
        "violations_pct": violations_pct,
        "violations_amp": violations_amp,
        "violations_und": violations_und,
        "violations_hash": violations_hash,
        "violations_curr": violations_curr,
        "passed": (
            len(violations_pct) == 0 and
            len(violations_amp) == 0 and
            len(violations_und) == 0 and
            len(violations_hash) == 0 and
            len(violations_curr) == 0
        )
    }


def test_empirical_pdf_truncation() -> Dict[str, Any]:
    try:
        import fitz
    except ImportError:
        return {
            "name": "Empirical PDF Truncation Check",
            "error": "PyMuPDF not installed in current python environment",
            "passed": False
        }

    # 1. Isolated snippet empirical test
    sys.path.insert(0, str(PROJECT_ROOT / "tests"))
    from test_helpers import compile_tex_snippet, STYLE_FILE
    
    # Extract verbatim line 1165 from part4_blueprints.tex
    p4_lines = (CHAPTERS_DIR / "part4_blueprints.tex").read_text(encoding="utf-8").splitlines()
    target_line = p4_lines[1164]  # 0-indexed line 1165
    
    snippet_code = f"""\\documentclass[11pt,a4paper,openany]{{book}}
\\input{{{STYLE_FILE}}}
\\begin{{document}}
\\begin{{ExampleBox}}{{Model Paragraph Test}}
{target_line}
\\end{{ExampleBox}}
\\end{{document}}"""
    
    snippet_res = compile_tex_snippet(snippet_code)
    snippet_truncated = False
    snippet_text = ""
    if snippet_res.pdf_path:
        sdoc = fitz.open(str(snippet_res.pdf_path))
        snippet_text = sdoc[0].get_text()
        if "from 4.8" in snippet_text and "Plant D" not in snippet_text and "0.9%" not in snippet_text:
            snippet_truncated = True

    # 2. Deliverable PDF check if available
    truncated_pages = []
    total_pages = 0
    if PDF_PATH.exists():
        doc = fitz.open(PDF_PATH)
        total_pages = len(doc)
        for pno in range(len(doc)):
            page = doc[pno]
            text = page.get_text()
            if "from 4.8" in text and "surface defect incidence" in text:
                for line in text.splitlines():
                    if "from 4.8" in line and "to 0.9" not in line and "to 0.9%" not in line:
                        truncated_pages.append({
                            "page_number": pno + 1,
                            "truncated_line": line.strip()
                        })
                        break

    has_defect = snippet_truncated or len(truncated_pages) > 0
    return {
        "name": "Empirical PDF Truncation Check",
        "snippet_truncated": snippet_truncated,
        "snippet_extracted_sample": snippet_text.strip()[:200],
        "deliverable_total_pages": total_pages,
        "deliverable_truncated_pages_count": len(truncated_pages),
        "deliverable_truncated_pages": truncated_pages,
        "passed": not has_defect
    }



def main():
    print("================================================================================")
    print(" EMPIRICAL ADVERSARIAL STRESS SUITE: M2 INGESTION & CHARACTER HYGIENE")
    print("================================================================================")
    
    suite_results = []
    
    tests = [
        test_grammar_rules_ingestion,
        test_expression_patterns_ingestion,
        test_logic_rules_ingestion,
        test_paragraph_blueprints_ingestion,
        test_revision_clinic_ingestion,
        test_full_text_anthology_ingestion,
        test_circled_numbers_hygiene,
        test_unescaped_special_chars,
        test_empirical_pdf_truncation
    ]
    
    all_passed = True
    for t in tests:
        res = t()
        suite_results.append(res)
        status = "✔ PASS" if res["passed"] else "✘ FAIL"
        print(f"[{status}] {res['name']}")
        if not res["passed"]:
            all_passed = False
            for k, v in res.items():
                if k not in ["name", "passed"] and v:
                    print(f"       -> {k}: {v}")
                    
    print("================================================================================")
    verdict = "APPROVE" if all_passed else "REQUEST_CHANGES"
    print(f"FINAL VERDICT: {verdict}")
    print("================================================================================")
    
    out_file = PROJECT_ROOT / "tests" / "adversarial_m2_hygiene_report.json"
    out_file.write_text(json.dumps({
        "verdict": verdict,
        "results": suite_results
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report saved to {out_file}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
