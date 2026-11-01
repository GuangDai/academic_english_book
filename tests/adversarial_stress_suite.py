#!/usr/bin/env python3
r"""Adversarial Empirical Stress Testing Suite for Academic English Book LaTeX Styling Engine.

Executed by teamwork_challenger_m1_1.
Validates:
1. Extreme line counts (0, 1, 50 lines) in \writinglines, alone and in ExerciseBox/ParagraphRevision.
2. Massive paragraphs (>1,000 words) inside ConceptBox, ExampleBox, TipBox, ExerciseBox across page breaks.
3. Deep nesting of boxes, SentenceRewriteItem, writing lines, and fillblank.
4. Special LaTeX characters in prompts, box titles, fillblank, and section headings.
5. Typographic stress: long unhyphenated words, mixed CJK/Latin typography, punctuation, unicode.
6. Build convergence log analysis (Overfull \hbox, Underfull, missing glyphs, bookmark integrity).
"""

import os
import sys
import re
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

sys.path.append(str(Path(__file__).parent))
from test_helpers import (
    PROJECT_ROOT, STYLE_FILE, MAIN_TEX, BUILD_SCRIPT,
    compile_tex_snippet, inspect_pdf, get_tex_env, CompilationResult
)

# Shared preamble using actual project style package
PREAMBLE = r"""\documentclass[11pt,a4paper,openany]{book}
\input{""" + str(STYLE_FILE) + r"""}
"""

class AdversarialStressSuite:
    def __init__(self):
        self.results = []
        self.start_time = 0.0

    def record(self, test_id: str, name: str, status: str, details: Dict[str, Any], duration: float):
        self.results.append({
            "id": test_id,
            "name": name,
            "status": status,
            "details": details,
            "duration": round(duration, 3)
        })

    # =========================================================================
    # Category 1: Extreme Ruled Lines (0, 1, 50 lines)
    # =========================================================================

    def test_adv_wl_01_zero_lines(self):
        """Test \\writinglines[11mm]{0} in standalone flow, ExerciseBox, and SentenceRewriteItem."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Zero Ruled Lines Stress Test}
Testing standalone 0 lines:
\writinglines{0}

\begin{ExerciseBox}{Exercise with Zero Lines}
Prompt with zero lines:
\writinglines[11mm]{0}
\end{ExerciseBox}

\SentenceRewriteItem[0]{Item 1}{Original text with zero lines requested.}

\begin{ParagraphRevision}[0]{1}{Zero Line Revision Case}
Paragraph text to revise.
\end{ParagraphRevision}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_wl_01")
        status = "PASS" if (res.pdf_exists and not res.fatal_error and res.overfull_count == 0) else "FAIL"
        self.record("ADV-WL-01", "Zero Ruled Lines (0 lines across macros)", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count,
            "fatal_error": res.fatal_error
        }, time.time() - t0)

    def test_adv_wl_02_single_line(self):
        """Test \\writinglines[11mm]{1} inside ExerciseBox and SentenceRewriteItem."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Single Ruled Line Stress Test}
Standalone 1 line:
\writinglines{1}

\begin{ExerciseBox}{Exercise with 1 Line}
Single line prompt:
\writinglines[11mm]{1}
\end{ExerciseBox}

\SentenceRewriteItem[1]{Item 1}{Original sentence to rewrite with 1 line.}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_wl_02")
        status = "PASS" if (res.pdf_exists and not res.fatal_error and res.overfull_count == 0) else "FAIL"
        self.record("ADV-WL-02", "Single Ruled Line (1 line)", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_wl_03_massive_50_lines_standalone(self):
        """Test \\writinglines[11mm]{50} standalone: 550mm height must cleanly break across >=3 pages."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Massive Ruled Lines: 50 Lines Standalone}
Start of composition zone:
\writinglines[11mm]{50}
End of composition zone.
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_wl_03")
        page_count = 0
        if res.pdf_exists:
            info = inspect_pdf(res.pdf_path)
            page_count = info.page_count
        # 50 lines at 11mm = 550mm. Printable height per A4 page ~250mm. Must be >= 3 pages.
        passed = (res.pdf_exists and not res.fatal_error and page_count >= 3)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-WL-03", "Massive Ruled Lines (50 lines standalone pagination)", status, {
            "pdf_exists": res.pdf_exists,
            "page_count": page_count,
            "expected_min_pages": 3,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_wl_04_massive_50_lines_inside_exercisebox(self):
        """Test \\writinglines[11mm]{50} INSIDE breakable ExerciseBox: must split across multiple pages."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Massive Ruled Lines Inside Breakable ExerciseBox}
\begin{ExerciseBox}{Extended Composition Worksheet (50 Lines)}
Please draft your complete research proposal below. Ensure rigorous argumentation.
\writinglines[11mm]{50}
\end{ExerciseBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_wl_04")
        page_count = 0
        if res.pdf_exists:
            info = inspect_pdf(res.pdf_path)
            page_count = info.page_count
        passed = (res.pdf_exists and not res.fatal_error and page_count >= 3)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-WL-04", "Massive Ruled Lines (50 lines inside breakable ExerciseBox)", status, {
            "pdf_exists": res.pdf_exists,
            "page_count": page_count,
            "expected_min_pages": 3,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    # =========================================================================
    # Category 2: Massive Multi-Page Paragraphs (>1,000 words) inside Boxes
    # =========================================================================

    def _generate_massive_academic_text(self, word_target: int = 1200) -> str:
        """Generate cohesive academic English prose of specified word count."""
        base_paragraph = (
            "Empirical investigation in contemporary epistemological frameworks necessitates a rigorous "
            "demarcation between correlational observations and causal mechanisms. In scholarly discourse, "
            "researchers frequently encounter methodological ambiguities when synthesizing qualitative narratives "
            "with quantitative metrics. To mitigate confounding covariates, the experimental architecture must "
            "incorporate orthogonal control paradigms, double-blind randomization protocols, and longitudinal tracking. "
            "Furthermore, syntactic economy dictates that passive constructions should not be multiplied beyond necessity, "
            "lest topical topicality be obscured by extraneous nominalizations. By aligning discourse markers with the "
            "Given-to-New information hierarchy, academic manuscripts maintain cohesive rhetorical momentum while preventing "
            "cognitive friction for domain specialists and cross-disciplinary evaluators alike. Consequently, systematic "
            "refinement of introductory contextualization, literature demarcation, and hypothesis formulation constitutes an "
            "indispensable prerequisite for reproducible scientific dissemination.\n\n"
        )
        words_per_para = len(base_paragraph.split())
        repeats = (word_target // words_per_para) + 2
        full_text = (base_paragraph * repeats)
        actual_words = len(full_text.split())
        return full_text

    def test_adv_box_01_conceptbox_massive(self):
        """Test ConceptBox with >1,200 words spanning 2-3 page breaks."""
        t0 = time.time()
        text = self._generate_massive_academic_text(1200)
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Massive ConceptBox Stress Test}
\begin{ConceptBox}{Comprehensive Theoretical Foundation: Epistemological Architecture}
""" + text + r"""
\end{ConceptBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_box_01")
        page_count = inspect_pdf(res.pdf_path).page_count if res.pdf_exists else 0
        passed = (res.pdf_exists and not res.fatal_error and page_count >= 2)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-BOX-01", "Massive Paragraph in ConceptBox (>1,200 words spanning pages)", status, {
            "pdf_exists": res.pdf_exists,
            "page_count": page_count,
            "word_count": len(text.split()),
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_box_02_examplebox_massive(self):
        """Test ExampleBox with >1,200 words spanning 2-3 page breaks."""
        t0 = time.time()
        text = self._generate_massive_academic_text(1200)
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Massive ExampleBox Stress Test}
\begin{ExampleBox}{Exemplary Corpus Analysis: Extended Case Study}
""" + text + r"""
\end{ExampleBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_box_02")
        page_count = inspect_pdf(res.pdf_path).page_count if res.pdf_exists else 0
        passed = (res.pdf_exists and not res.fatal_error and page_count >= 2)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-BOX-02", "Massive Paragraph in ExampleBox (>1,200 words spanning pages)", status, {
            "pdf_exists": res.pdf_exists,
            "page_count": page_count,
            "word_count": len(text.split()),
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_box_03_tipbox_massive(self):
        """Test TipBox with >1,200 words spanning 2-3 page breaks."""
        t0 = time.time()
        text = self._generate_massive_academic_text(1200)
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Massive TipBox Stress Test}
\begin{TipBox}{Critical Stylistic Warnings: Diagnostic Catalog of Scholarly Pitfalls}
""" + text + r"""
\end{TipBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_box_03")
        page_count = inspect_pdf(res.pdf_path).page_count if res.pdf_exists else 0
        passed = (res.pdf_exists and not res.fatal_error and page_count >= 2)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-BOX-03", "Massive Paragraph in TipBox (>1,200 words spanning pages)", status, {
            "pdf_exists": res.pdf_exists,
            "page_count": page_count,
            "word_count": len(text.split()),
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_box_04_exercisebox_massive(self):
        """Test ExerciseBox with >1,200 words spanning 2-3 page breaks."""
        t0 = time.time()
        text = self._generate_massive_academic_text(1200)
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Massive ExerciseBox Stress Test}
\begin{ExerciseBox}{Multi-Section Intensive Diagnostic Worksheet}
""" + text + r"""
\end{ExerciseBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_box_04")
        page_count = inspect_pdf(res.pdf_path).page_count if res.pdf_exists else 0
        passed = (res.pdf_exists and not res.fatal_error and page_count >= 2)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-BOX-04", "Massive Paragraph in ExerciseBox (>1,200 words spanning pages)", status, {
            "pdf_exists": res.pdf_exists,
            "page_count": page_count,
            "word_count": len(text.split()),
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    # =========================================================================
    # Category 3: Deep Nesting & Compound Combinations
    # =========================================================================

    def test_adv_nest_01_exercisebox_with_rewrites_and_fillblanks(self):
        """ExerciseBox containing 8 SentenceRewriteItems each with fillblank and writing lines across page breaks."""
        t0 = time.time()
        items = ""
        for i in range(1, 9):
            items += f"""
\\SentenceRewriteItem[3]{{Task {i}}}{{The experiment was \\fillblank[4.5cm]{{failed by the researchers}} because they did not \\DefectTarget{{take into consideration}} the temperature fluctuations.}}
"""
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Compound Nesting: ExerciseBox with Sentence Rewrites}
\begin{ExerciseBox}{Compound Interactive Practice Zone}
Transform the following 8 sentences into concise academic prose. Use the designated 11mm writing lines:
""" + items + r"""
\end{ExerciseBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_nest_01")
        page_count = inspect_pdf(res.pdf_path).page_count if res.pdf_exists else 0
        passed = (res.pdf_exists and not res.fatal_error and page_count >= 2)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-NEST-01", "ExerciseBox + 8 SentenceRewriteItems + fillblank + writing lines (Multi-page)", status, {
            "pdf_exists": res.pdf_exists,
            "page_count": page_count,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_nest_02_box_inside_box(self):
        """Adversarial challenge: Nesting a TipBox inside a ConceptBox, and ExampleBox inside ExerciseBox."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Box-in-Box Nesting Stress Test}
\begin{ConceptBox}{Outer Concept Box}
This is the outer theoretical container.
\begin{TipBox}{Inner Tip Box Inside Concept}
This is a nested tip box inside an outer concept box.
\end{TipBox}
Continuing the outer container narrative.
\end{ConceptBox}

\begin{ExerciseBox}{Outer Exercise Box}
This is the outer exercise worksheet.
\begin{ExampleBox}{Inner Example Box Inside Exercise}
This is a model exemplar inside the worksheet.
\end{ExampleBox}
\writinglines{3}
\end{ExerciseBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_nest_02")
        # In tcolorbox, breakable inside breakable can fail unless inner is unbreakable.
        # Let's see what happens empirically!
        passed = (res.pdf_exists and not res.fatal_error)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-NEST-02", "Box-in-Box Nesting (TipBox in ConceptBox, ExampleBox in ExerciseBox)", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count,
            "fatal_error": res.fatal_error,
            "log_snippet": "\n".join([line for line in res.log_text.splitlines() if "Error" in line or "Warning" in line][:5])
        }, time.time() - t0)

    def test_adv_nest_03_paragraph_revision_state_leakage(self):
        """Test ParagraphRevision scoping with varying lines (4 lines then 12 lines then 2 lines)."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{ParagraphRevision Scoping Test}
\begin{ParagraphRevision}[4]{1}{First Revision Block (4 lines)}
First test original paragraph text.
\end{ParagraphRevision}

\begin{ParagraphRevision}[12]{2}{Second Revision Block (12 lines)}
Second test original paragraph text with large response zone.
\end{ParagraphRevision}

\begin{ParagraphRevision}[2]{3}{Third Revision Block (2 lines)}
Third test original paragraph text.
\end{ParagraphRevision}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_nest_03")
        passed = (res.pdf_exists and not res.fatal_error)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-WL-05", "ParagraphRevision Scoping & State Isolation (4, 12, 2 lines)", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_wl_06_physical_vector_pitch_assertion(self):
        """Strict physical vector pitch measurement: must measure 10.5mm - 11.5mm (29.8pt - 32.6pt)."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Physical Line Pitch Precision Test}
Standalone 10 lines:
\writinglines[11mm]{10}

\begin{ExerciseBox}{ExerciseBox Ruled Line Pitch}
Prompt with 10 lines:
\writinglines[11mm]{10}
\end{ExerciseBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_wl_06_pitch")
        if not res.pdf_exists or res.fatal_error:
            self.record("ADV-WL-06", "Ruled Line Physical Pitch Calibration (10.5mm-11.5mm)", "FAIL", {
                "error": "Compilation failed", "log": res.stderr
            }, time.time() - t0)
            return

        try:
            import fitz
        except ImportError:
            site_packages = '/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/.venv-toolkit-20261025/lib/python3.14/site-packages'
            if site_packages not in sys.path:
                sys.path.append(site_packages)
            import fitz

        doc = fitz.open(res.pdf_path)
        all_pitches_mm = []
        all_pitches_pt = []
        for page in doc:
            rules = [d for d in page.get_drawings()
                     if d.get('color') and len(d['color']) == 3 and
                     abs(d['color'][0] - 0.729) < 0.05 and d['rect'].width > 300]
            rules.sort(key=lambda x: x['rect'].y0)
            for i in range(1, len(rules)):
                dy_pt = rules[i]['rect'].y0 - rules[i-1]['rect'].y0
                dy_mm = dy_pt * 25.4 / 72.0
                if dy_mm < 20.0:  # Intra-block consecutive lines
                    all_pitches_pt.append(round(dy_pt, 2))
                    all_pitches_mm.append(round(dy_mm, 2))
        doc.close()

        min_mm = min(all_pitches_mm) if all_pitches_mm else 0.0
        max_mm = max(all_pitches_mm) if all_pitches_mm else 0.0
        mean_mm = sum(all_pitches_mm) / len(all_pitches_mm) if all_pitches_mm else 0.0

        # Strict acceptance criteria: 10.5mm <= pitch <= 11.5mm
        # Fatal rejection: pitch > 12.0mm or pitch < 10.0mm
        in_range = all(10.5 <= p <= 11.5 for p in all_pitches_mm)
        no_extreme = not any(p > 12.0 or p < 10.0 for p in all_pitches_mm)
        passed = (len(all_pitches_mm) >= 16 and in_range and no_extreme and res.overfull_count == 0)

        status = "PASS" if passed else "FAIL"
        self.record("ADV-WL-06", "Ruled Line Physical Pitch Calibration (10.5mm-11.5mm)", status, {
            "total_pairs_measured": len(all_pitches_mm),
            "min_pitch_mm": min_mm,
            "max_pitch_mm": max_mm,
            "mean_pitch_mm": round(mean_mm, 2),
            "pitch_samples_pt": all_pitches_pt[:5],
            "in_nominal_range (10.5-11.5mm)": in_range,
            "zero_extreme_deviations (<10mm or >12mm)": no_extreme,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    # =========================================================================
    # Category 4: Special Characters Stress
    # =========================================================================

    def test_adv_char_01_special_characters_everywhere(self):
        """Stress test special LaTeX characters (%, $, &, _, #, {, }, ^, ~, backslash) in text, titles, fillblank."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Special Characters: 100\% Coverage \& \$50M Funding \#1 \_Core\_}

\section{Testing Escapes in Headings: 99.9\% \& \$100K \_Var\_ \#2}

\begin{ConceptBox}{Title With Specials: 95\% CI \& \$2.5M \_Sub\_ \#3}
Body text with special characters:
The model achieved 98.5\% accuracy on Dataset \#1 under \$5,000 budget constraints \& reduced loss by 12\%.
Variables \_alpha\_ and \_beta\_ satisfy condition $X_i \le Y_j$.
Tilde: 50 \textasciitilde{} 100 samples. Caret: 10\textasciicircum 5 iterations.
Backslash: Path separator \textbackslash{}usr\textbackslash{}bin.
Braces: Grouping \{item\_a, item\_b\}.
\end{ConceptBox}

\SentenceRewriteItem[2]{Item 1.1}{Rewrite 50\% of the data \& verify that \$p < 0.05\$ for parameter \#1.}

\begin{ExerciseBox}{Fillblank with Specials}
Fill in with specials:
The result was \fillblank[5cm]{95\% confidence \& $p < 0.01$} under test condition \fillblank[4cm]{\#4 \_verified\_}.
\end{ExerciseBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_char_01")
        # Check if bookmarks or titles have token errors
        corrupt_tokens = [line for line in res.log_text.splitlines() if "Token not allowed in a PDF string" in line]
        passed = (res.pdf_exists and not res.fatal_error)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-CHAR-01", "Special Characters (%, $, &, _, #, {}, ^, ~, backslash in macros/titles)", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count,
            "corrupt_pdf_tokens_count": len(corrupt_tokens),
            "corrupt_tokens": corrupt_tokens[:3]
        }, time.time() - t0)

    def test_adv_char_02_math_and_symbols_in_fillblank(self):
        """Stress test complex inline math mode and greek characters inside fillblank."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Math Mode in Interactive Blanks}
Test math in fillblank:
According to the derivation, $\sum_{i=1}^n x_i = \fillblank[4cm]{$\frac{n(n+1)}{2}$}$ and the complexity is $\fillblank[5cm]{$\mathcal{O}(n \log n)$}$.
Also matrix dimensions: $\fillblank[4.5cm]{$\mathbf{W} \in \mathbb{R}^{d \times k}$}$.
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_char_02")
        passed = (res.pdf_exists and not res.fatal_error and res.overfull_count == 0)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-CHAR-02", "Complex Math Expressions inside fillblank", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    # =========================================================================
    # Category 5: Typography, Line Breaking & Chinese/English Text
    # =========================================================================

    def test_adv_typo_01_long_unhyphenated_words(self):
        """Stress test long unhyphenated academic words near margins to test emergency stretch."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Typographic Stress: Unhyphenated Words}
The clinical diagnostic pathway demonstrated extensive
Supercalifragilisticexpialidocious manifestations alongside
Electroencephalographically documented oscillations. Furthermore,
Pseudopseudohypoparathyroidism was systematically differentiated from
Immunohistochemically verified anomalies and
Deoxyribonucleic modifications in longitudinal trials.
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_typo_01")
        # Extract overfull hbox details
        overfull_lines = [l for l in res.log_text.splitlines() if "Overfull \\hbox" in l]
        passed = (res.pdf_exists and not res.fatal_error)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-TYPO-01", "Long Unhyphenated Academic Words & Margin Stretch", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": len(overfull_lines),
            "overfull_lines": overfull_lines
        }, time.time() - t0)

    def test_adv_typo_02_dense_cjk_latin_mixed_typography(self):
        """Stress test dense CJK/Latin mixed typography, quotation marks, and ratio colon (U+2236)."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Bilingual Typography \& Unicode Punctuation / 双语排版与标点符号}

\section{Dense Mixed Text / 密集混排}
本研究基于Transformer深度学习架构，针对BERT-Large模型在Natural Language Processing（NLP）任务中的Cross-Entropy Loss进行了优化。实验证明，其F1-Score提高了3.42个百分点（$p < 0.01$）。

\section{Punctuation Tests / 标点与比例号}
比例关系测试：输入与输出之比为 16∶9（采用Unicode比例号 U+2236）。
中文冒号：注意：此方法需严格控制超参数。
英文冒号: Note: this method requires rigorous hyperparameter calibration.
中文双引号：“学术英语核心写作规范”。
英文双引号: ``Academic English Writing Conventions''.

\begin{ConceptBox}{核心概念：Given-to-New 信息流原则}
在学术语篇中，旧信息（Given Information）置于句首作为主语（Subject/Theme），新信息（New Information）置于句末谓语后（Rheme）。
\end{ConceptBox}
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_typo_02")
        missing_chars = [l for l in res.log_text.splitlines() if "Missing character:" in l]
        passed = (res.pdf_exists and not res.fatal_error and len(missing_chars) == 0)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-TYPO-02", "Dense CJK/Latin Mixed Typography & Unicode Punctuation", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "missing_chars_count": len(missing_chars),
            "missing_chars": missing_chars,
            "overfull_count": res.overfull_count
        }, time.time() - t0)

    def test_adv_typo_03_fillblank_overflow_boundary(self):
        """Adversarial stress: fillblank with prompt longer than default width and placed near margin."""
        t0 = time.time()
        tex = PREAMBLE + r"""
\begin{document}
\chapter{Fillblank Margin Overflow Stress Test}
Standard fillblank:
The participant demonstrated \fillblank{unprecedented resilience} during the trial.

Extremely wide fillblank (exceeding line width or placed at end of sentence):
In our primary experimental evaluation, we observed that \fillblank[12cm]{an extraordinarily extensive and comprehensive explanatory phrase that pushes margins} was present.
\end{document}
"""
        res = compile_tex_snippet(tex, "adv_typo_03")
        overfull_lines = [l for l in res.log_text.splitlines() if "Overfull \\hbox" in l]
        passed = (res.pdf_exists and not res.fatal_error)
        status = "PASS" if passed else "FAIL"
        self.record("ADV-TYPO-03", "Fillblank Overflow Boundary (adaptive sizing check)", status, {
            "pdf_exists": res.pdf_exists,
            "returncode": res.returncode,
            "overfull_count": len(overfull_lines),
            "overfull_lines": overfull_lines
        }, time.time() - t0)

    # =========================================================================
    # Category 6: Master Deliverable Multi-Pass Compilation Audit
    # =========================================================================

    def test_adv_audit_master_document(self):
        """Audit full academic_english_book build and parse all pass logs."""
        t0 = time.time()
        import subprocess
        env = get_tex_env()
        build_dir = PROJECT_ROOT / "build"
        
        proc = subprocess.run([str(BUILD_SCRIPT), str(build_dir), "main.tex"],
                              cwd=str(PROJECT_ROOT), env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Parse pass 1-3 logs
        pass_logs = list(build_dir.glob("build_pass_*.log"))
        pass_logs.sort()
        last_log = pass_logs[-1].read_text(encoding='utf-8', errors='replace') if pass_logs else ""
        xdv_log = (build_dir / "xdvipdfmx.log").read_text(encoding='utf-8', errors='replace') if (build_dir / "xdvipdfmx.log").exists() else ""
        
        overfull_hboxes = [l for l in last_log.splitlines() if "Overfull \\hbox" in l]
        underfull_hboxes = [l for l in last_log.splitlines() if "Underfull \\hbox" in l]
        overfull_vboxes = [l for l in last_log.splitlines() if "Overfull \\vbox" in l]
        underfull_vboxes = [l for l in last_log.splitlines() if "Underfull \\vbox" in l]
        missing_chars = [l for l in last_log.splitlines() if "Missing character:" in l]
        undefined_refs = [l for l in last_log.splitlines() if "Reference `" in l and "undefined" in l]
        
        pdf_path = PROJECT_ROOT / "academic_english_book.pdf"
        pdf_exists = pdf_path.is_file() and pdf_path.stat().st_size > 0
        info = inspect_pdf(pdf_path) if pdf_exists else None
        
        passed = (proc.returncode == 0 and pdf_exists and len(missing_chars) == 0 and len(overfull_hboxes) == 0)
        status = "PASS" if passed else "FAIL"
        
        self.record("ADV-AUDIT-01", "Full Master Document Build Audit & Log Diagnostics", status, {
            "returncode": proc.returncode,
            "pdf_exists": pdf_exists,
            "pdf_pages": info.page_count if info else 0,
            "bookmarks_count": len(info.bookmarks) if info else 0,
            "overfull_hboxes_count": len(overfull_hboxes),
            "underfull_hboxes_count": len(underfull_hboxes),
            "overfull_vboxes_count": len(overfull_vboxes),
            "underfull_vboxes_count": len(underfull_vboxes),
            "missing_chars_count": len(missing_chars),
            "undefined_refs_count": len(undefined_refs),
            "overfull_hboxes_samples": overfull_hboxes[:5],
            "underfull_vboxes_samples": underfull_vboxes[:3]
        }, time.time() - t0)

    # =========================================================================
    # Runner
    # =========================================================================

    def run_all(self):
        self.start_time = time.time()
        print("=" * 80)
        print(" EMPIRICAL ADVERSARIAL STRESS TEST SUITE — MILESTONE 1 LATEX STYLING")
        print("=" * 80)

        tests = [
            ("ADV-WL-01", self.test_adv_wl_01_zero_lines),
            ("ADV-WL-02", self.test_adv_wl_02_single_line),
            ("ADV-WL-03", self.test_adv_wl_03_massive_50_lines_standalone),
            ("ADV-WL-04", self.test_adv_wl_04_massive_50_lines_inside_exercisebox),
            ("ADV-BOX-01", self.test_adv_box_01_conceptbox_massive),
            ("ADV-BOX-02", self.test_adv_box_02_examplebox_massive),
            ("ADV-BOX-03", self.test_adv_box_03_tipbox_massive),
            ("ADV-BOX-04", self.test_adv_box_04_exercisebox_massive),
            ("ADV-NEST-01", self.test_adv_nest_01_exercisebox_with_rewrites_and_fillblanks),
            ("ADV-NEST-02", self.test_adv_nest_02_box_inside_box),
            ("ADV-WL-05", self.test_adv_nest_03_paragraph_revision_state_leakage),
            ("ADV-WL-06", self.test_adv_wl_06_physical_vector_pitch_assertion),
            ("ADV-CHAR-01", self.test_adv_char_01_special_characters_everywhere),
            ("ADV-CHAR-02", self.test_adv_char_02_math_and_symbols_in_fillblank),
            ("ADV-TYPO-01", self.test_adv_typo_01_long_unhyphenated_words),
            ("ADV-TYPO-02", self.test_adv_typo_02_dense_cjk_latin_mixed_typography),
            ("ADV-TYPO-03", self.test_adv_typo_03_fillblank_overflow_boundary),
            ("ADV-AUDIT-01", self.test_adv_audit_master_document),
        ]

        for tid, func in tests:
            print(f"[*] Running {tid}: {func.__doc__.splitlines()[0] if func.__doc__ else func.__name__}...")
            try:
                func()
                res = self.results[-1]
                icon = "✔" if res["status"] == "PASS" else "✘"
                print(f"    {icon} {res['status']} ({res['duration']}s)")
            except Exception as e:
                import traceback
                print(f"    ✘ EXCEPTION: {e}")
                self.record(tid, func.__name__, "FAIL", {"exception": str(e), "traceback": traceback.format_exc()}, 0.0)

        total_time = round(time.time() - self.start_time, 2)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")

        print("=" * 80)
        print(f" SUMMARY: {passed} PASSED, {failed} FAILED out of {len(self.results)} tests ({total_time}s)")
        print("=" * 80)

        # Output JSON result
        report_path = PROJECT_ROOT / "tests" / "adversarial_stress_report.json"
        report_path.write_text(json.dumps({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total": len(self.results),
            "passed": passed,
            "failed": failed,
            "total_time_seconds": total_time,
            "tests": self.results
        }, indent=2, ensure_ascii=False))
        print(f"Report written to: {report_path}")

        return 0 if failed == 0 else 1

if __name__ == "__main__":
    suite = AdversarialStressSuite()
    sys.exit(suite.run_all())
