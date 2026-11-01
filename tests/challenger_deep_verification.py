#!/usr/bin/env python3
r"""Challenger Deep Verification Script for \writinglines breakable box pagination.

Executed by teamwork_challenger_m1_it2_1.
Empirically tests:
1. Deep check on ADV-WL-04: N=50 writing lines inside ExerciseBox with preceding text.
   - Assert document spans >= 3 pages.
   - Assert all 50 ruled lines are drawn across pages.
   - Assert 0 lines dropped.
   - Assert 0 overfull hboxes in XeLaTeX compilation log.
2. Boundary stress sweep across N in [0, 1, 20, 21, 35, 50, 75].
   - Validates the N=20 -> N=21 pagination cliff where lines previously vanished.
   - Validates exact drawn count == N.
   - Validates 0 overfull hboxes.
3. Near-boundary page split test (preceding text fills ~90% of page 1, forcing split mid-macro).
4. Extreme line count stress (N=100 lines inside ExerciseBox).
5. Consecutive ExerciseBoxes with writing lines (re-entrancy and counter scoping).
6. Non-default line spacing sweeps (8mm and 15mm spacing).
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
import fitz

sys.path.append(str(Path(__file__).parent))
from test_helpers import compile_tex_snippet, STYLE_FILE

PREAMBLE = r"""\documentclass[11pt,a4paper,openany]{book}
\input{""" + str(STYLE_FILE) + r"""}
"""

def is_writing_line(drawing: Dict[str, Any]) -> bool:
    """Determine whether a vector drawing corresponds to an authentic handwriting ruled line."""
    color = drawing.get("color")
    if not color or len(color) != 3:
        return False
    r, g, b = color
    # RuleLineColor is #BAC7D5 -> (0.729, 0.780, 0.835)
    if not (abs(r - 0.729) < 0.05 and abs(g - 0.780) < 0.05 and abs(b - 0.835) < 0.05):
        return False
    items = drawing.get("items", [])
    if len(items) != 1:
        return False
    cmd = items[0]
    if cmd[0] != 'l':
        return False
    p1, p2 = cmd[1], cmd[2]
    # Must be horizontal line
    if abs(p1.y - p2.y) > 0.5:
        return False
    # Must span text width (> 300 pt)
    line_len = abs(p2.x - p1.x)
    if line_len < 300.0:
        return False
    return True

def inspect_drawn_writing_lines(pdf_path: Path) -> Tuple[int, List[int], int]:
    """Inspect PDF and return (total_writing_lines, lines_per_page, page_count)."""
    doc = fitz.open(str(pdf_path))
    page_count = len(doc)
    lines_per_page = []
    total = 0
    for page in doc:
        page_lines = 0
        for d in page.get_drawings():
            if is_writing_line(d):
                page_lines += 1
        lines_per_page.append(page_lines)
        total += page_lines
    doc.close()
    return total, lines_per_page, page_count


def run_deep_verification() -> Dict[str, Any]:
    print("=" * 80)
    print(" EMPIRICAL ADVERSARIAL CHALLENGER VERIFICATION — \\writinglines PAGINATION")
    print("=" * 80)

    all_passed = True
    results = {}

    # -------------------------------------------------------------------------
    # TEST 1: ADV-WL-04 Deep Empirical Check (N=50 with preceding text)
    # -------------------------------------------------------------------------
    print("\n[*] TEST 1: ADV-WL-04 Deep Check (N=50 in ExerciseBox with preceding prompt text)...")
    tex_50 = PREAMBLE + r"""
\begin{document}
\chapter{Advanced Composition Section}
\begin{ExerciseBox}{Exercise 4.2: Comprehensive Literature Review Proposal}
Please provide an in-depth, structured proposal for your academic research project.
Include the epistemological justification, methodological framework, data collection
procedures, and anticipated limitations. Ensure that all arguments are rigorously
articulated and supported by appropriate academic discourse markers.
\writinglines[11mm]{50}
\end{ExerciseBox}
\end{document}
"""
    t0 = time.time()
    res = compile_tex_snippet(tex_50, "challenger_deep_50")
    d1 = time.time() - t0

    if not res.pdf_exists or res.fatal_error:
        print(f"    ❌ COMPILATION FAILED: returncode={res.returncode}, fatal={res.fatal_error}")
        all_passed = False
        t1_status = "FAIL"
        t1_details = {"error": "Compilation failed", "log": res.stderr}
    else:
        total_lines, lines_per_page, page_count = inspect_drawn_writing_lines(res.pdf_path)
        print(f"    PDF compiled successfully in {d1:.2f}s.")
        print(f"    Page count: {page_count} (Requirement: >= 3)")
        print(f"    Lines per page: {lines_per_page} (Total lines drawn: {total_lines}, Expected: 50)")
        print(f"    Overfull hboxes: {res.overfull_count} (Requirement: 0)")

        passed = (
            page_count >= 3 and
            total_lines == 50 and
            res.overfull_count == 0 and
            not res.fatal_error
        )
        t1_status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"    Verdict: {'✔ PASS' if passed else '❌ FAIL'}")
        t1_details = {
            "page_count": page_count,
            "lines_per_page": lines_per_page,
            "total_lines_drawn": total_lines,
            "expected_lines": 50,
            "overfull_hboxes": res.overfull_count,
            "duration": round(d1, 3)
        }
    results["TEST_1_ADV_WL_04_DEEP"] = {"status": t1_status, "details": t1_details}

    # -------------------------------------------------------------------------
    # TEST 2: Boundary Sweeps Across Line Counts (N = 0, 1, 20, 21, 35, 50, 75)
    # -------------------------------------------------------------------------
    print("\n[*] TEST 2: Boundary Sweeps Across Line Counts N in [0, 1, 20, 21, 35, 50, 75]...")
    sweep_counts = [0, 1, 20, 21, 35, 50, 75]
    sweep_results = {}

    for n in sweep_counts:
        t0 = time.time()
        tex_n = PREAMBLE + rf"""
\begin{{document}}
\chapter{{Line Count Sweep N={n}}}
\begin{{ExerciseBox}}{{Boundary Test for N={n}}}
Standard prompt text for line sweep test with N={n} lines requested.
\writinglines[11mm]{{{n}}}
\end{{ExerciseBox}}
\end{{document}}
"""
        res_n = compile_tex_snippet(tex_n, f"challenger_sweep_n_{n}")
        d_n = time.time() - t0

        if not res_n.pdf_exists or res_n.fatal_error:
            print(f"    N={n:2d}: ❌ COMPILATION FAILED")
            all_passed = False
            sweep_results[f"N_{n}"] = {"status": "FAIL", "error": "Compilation failed"}
            continue

        total_lines, lines_per_page, page_count = inspect_drawn_writing_lines(res_n.pdf_path)
        overfull = res_n.overfull_count

        n_pass = (total_lines == n and overfull == 0 and not res_n.fatal_error)
        if not n_pass:
            all_passed = False

        print(f"    N={n:2d}: {'✔ PASS' if n_pass else '❌ FAIL'} | pages={page_count} | lines_per_page={lines_per_page} (total={total_lines}/{n}) | overfull={overfull} | time={d_n:.2f}s")
        sweep_results[f"N_{n}"] = {
            "status": "PASS" if n_pass else "FAIL",
            "page_count": page_count,
            "lines_per_page": lines_per_page,
            "total_lines_drawn": total_lines,
            "expected_lines": n,
            "overfull_hboxes": overfull,
            "duration": round(d_n, 3)
        }
    results["TEST_2_BOUNDARY_SWEEPS"] = sweep_results

    # -------------------------------------------------------------------------
    # TEST 3: Near-Boundary Page Split Mid-Macro Stress Test
    # -------------------------------------------------------------------------
    print("\n[*] TEST 3: Preceding text pushing start of writing lines right to page bottom...")
    # Generate ~2100 chars of text so that ExerciseBox starts, prompt occupies almost full page 1,
    # and \writinglines starts with line 1 or 2 at the bottom, breaking to page 2.
    filler = (
        "In scholarly discourse, the articulation of epistemological stances necessitates "
        "carefully calibrated linguistic scaffolding. Researchers must systematically address "
        "potential confounders and demonstrate methodological coherence. Furthermore, textual "
        "organization should adhere to the canonical Given-to-New principle to minimize cognitive load.\n\n"
    ) * 7
    tex_split = PREAMBLE + rf"""
\begin{{document}}
\chapter{{Mid-Macro Break Stress Test}}
\begin{{ExerciseBox}}{{Mid-Macro Split Test}}
{filler}
\writinglines[11mm]{{25}}
\end{{ExerciseBox}}
\end{{document}}
"""
    t0 = time.time()
    res_split = compile_tex_snippet(tex_split, "challenger_mid_break")
    d_split = time.time() - t0
    if not res_split.pdf_exists or res_split.fatal_error:
        print(f"    ❌ COMPILATION FAILED: {res_split.stderr}")
        all_passed = False
        t3_status = "FAIL"
        t3_details = {"error": "Compilation failed"}
    else:
        total_lines, lines_per_page, page_count = inspect_drawn_writing_lines(res_split.pdf_path)
        t3_pass = (total_lines == 25 and res_split.overfull_count == 0 and page_count >= 2)
        if not t3_pass:
            all_passed = False
        t3_status = "PASS" if t3_pass else "FAIL"
        print(f"    Mid-break N=25: {'✔ PASS' if t3_pass else '❌ FAIL'} | pages={page_count} | lines_per_page={lines_per_page} (total={total_lines}/25) | overfull={res_split.overfull_count} | time={d_split:.2f}s")
        t3_details = {
            "page_count": page_count,
            "lines_per_page": lines_per_page,
            "total_lines_drawn": total_lines,
            "expected_lines": 25,
            "overfull_hboxes": res_split.overfull_count,
            "duration": round(d_split, 3)
        }
    results["TEST_3_NEAR_BOUNDARY_SPLIT"] = {"status": t3_status, "details": t3_details}

    # -------------------------------------------------------------------------
    # TEST 4: Extreme Line Count Stress Test (N=100)
    # -------------------------------------------------------------------------
    print("\n[*] TEST 4: Extreme Line Count Stress Test (N=100 inside ExerciseBox)...")
    tex_100 = PREAMBLE + r"""
\begin{document}
\chapter{Extreme Line Count N=100}
\begin{ExerciseBox}{Centennial Line Stress Test}
Please record all observations over the 100-step longitudinal study.
\writinglines[11mm]{100}
\end{ExerciseBox}
\end{document}
"""
    t0 = time.time()
    res_100 = compile_tex_snippet(tex_100, "challenger_extreme_100")
    d_100 = time.time() - t0
    if not res_100.pdf_exists or res_100.fatal_error:
        print(f"    ❌ COMPILATION FAILED: {res_100.stderr}")
        all_passed = False
        t4_status = "FAIL"
        t4_details = {"error": "Compilation failed"}
    else:
        total_lines, lines_per_page, page_count = inspect_drawn_writing_lines(res_100.pdf_path)
        t4_pass = (total_lines == 100 and res_100.overfull_count == 0 and page_count >= 5)
        if not t4_pass:
            all_passed = False
        t4_status = "PASS" if t4_pass else "FAIL"
        print(f"    N=100: {'✔ PASS' if t4_pass else '❌ FAIL'} | pages={page_count} | lines_per_page={lines_per_page} (total={total_lines}/100) | overfull={res_100.overfull_count} | time={d_100:.2f}s")
        t4_details = {
            "page_count": page_count,
            "lines_per_page": lines_per_page,
            "total_lines_drawn": total_lines,
            "expected_lines": 100,
            "overfull_hboxes": res_100.overfull_count,
            "duration": round(d_100, 3)
        }
    results["TEST_4_EXTREME_100"] = {"status": t4_status, "details": t4_details}

    # -------------------------------------------------------------------------
    # TEST 5: Consecutive ExerciseBoxes with Ruled Lines (Re-entrancy & Isolation)
    # -------------------------------------------------------------------------
    print("\n[*] TEST 5: Consecutive ExerciseBoxes with Ruled Lines (Re-entrancy)...")
    tex_multi = PREAMBLE + r"""
\begin{document}
\chapter{Consecutive Boxes}
\begin{ExerciseBox}{Exercise Part A}
Part A response:
\writinglines[11mm]{20}
\end{ExerciseBox}
\begin{ExerciseBox}{Exercise Part B}
Part B response:
\writinglines[11mm]{25}
\end{ExerciseBox}
\end{document}
"""
    t0 = time.time()
    res_multi = compile_tex_snippet(tex_multi, "challenger_consecutive")
    d_multi = time.time() - t0
    if not res_multi.pdf_exists or res_multi.fatal_error:
        print(f"    ❌ COMPILATION FAILED: {res_multi.stderr}")
        all_passed = False
        t5_status = "FAIL"
        t5_details = {"error": "Compilation failed"}
    else:
        total_lines, lines_per_page, page_count = inspect_drawn_writing_lines(res_multi.pdf_path)
        expected_total = 20 + 25  # 45
        t5_pass = (total_lines == expected_total and res_multi.overfull_count == 0)
        if not t5_pass:
            all_passed = False
        t5_status = "PASS" if t5_pass else "FAIL"
        print(f"    Consecutive Boxes (20 + 25 = 45): {'✔ PASS' if t5_pass else '❌ FAIL'} | pages={page_count} | lines_per_page={lines_per_page} (total={total_lines}/45) | overfull={res_multi.overfull_count} | time={d_multi:.2f}s")
        t5_details = {
            "page_count": page_count,
            "lines_per_page": lines_per_page,
            "total_lines_drawn": total_lines,
            "expected_lines": expected_total,
            "overfull_hboxes": res_multi.overfull_count,
            "duration": round(d_multi, 3)
        }
    results["TEST_5_CONSECUTIVE_BOXES"] = {"status": t5_status, "details": t5_details}

    # -------------------------------------------------------------------------
    # TEST 6: Custom Spacing Sweeps (8mm and 15mm Spacing)
    # -------------------------------------------------------------------------
    print("\n[*] TEST 6: Custom Spacing Sweeps (8mm and 15mm Spacing across page breaks)...")
    tex_spacing = PREAMBLE + r"""
\begin{document}
\chapter{Custom Spacing Sweeps}
\begin{ExerciseBox}{Compact 8mm Spacing (35 Lines)}
\writinglines[8mm]{35}
\end{ExerciseBox}
\newpage
\begin{ExerciseBox}{Generous 15mm Spacing (30 Lines)}
\writinglines[15mm]{30}
\end{ExerciseBox}
\end{document}
"""
    t0 = time.time()
    res_spacing = compile_tex_snippet(tex_spacing, "challenger_custom_spacing")
    d_spacing = time.time() - t0
    if not res_spacing.pdf_exists or res_spacing.fatal_error:
        print(f"    ❌ COMPILATION FAILED: {res_spacing.stderr}")
        all_passed = False
        t6_status = "FAIL"
        t6_details = {"error": "Compilation failed"}
    else:
        total_lines, lines_per_page, page_count = inspect_drawn_writing_lines(res_spacing.pdf_path)
        expected_total = 35 + 30  # 65
        t6_pass = (total_lines == expected_total and res_spacing.overfull_count == 0)
        if not t6_pass:
            all_passed = False
        t6_status = "PASS" if t6_pass else "FAIL"
        print(f"    Custom Spacing (35 + 30 = 65): {'✔ PASS' if t6_pass else '❌ FAIL'} | pages={page_count} | lines_per_page={lines_per_page} (total={total_lines}/65) | overfull={res_spacing.overfull_count} | time={d_spacing:.2f}s")
        t6_details = {
            "page_count": page_count,
            "lines_per_page": lines_per_page,
            "total_lines_drawn": total_lines,
            "expected_lines": expected_total,
            "overfull_hboxes": res_spacing.overfull_count,
            "duration": round(d_spacing, 3)
        }
    results["TEST_6_CUSTOM_SPACING"] = {"status": t6_status, "details": t6_details}

    # -------------------------------------------------------------------------
    # TEST 7: ParagraphRevision Scoping Verification
    # -------------------------------------------------------------------------
    print("\n[*] TEST 7: ParagraphRevision Sequential / Scoping Verification...")
    tex_pr = PREAMBLE + r"""
\begin{document}
\chapter{ParagraphRevision Verification}
\begin{ParagraphRevision}[4]{1}{First Case (4 lines)}
First original paragraph.
\end{ParagraphRevision}

\begin{ParagraphRevision}[12]{2}{Second Case (12 lines)}
Second original paragraph.
\end{ParagraphRevision}

\begin{ParagraphRevision}[2]{3}{Third Case (2 lines)}
Third original paragraph.
\end{ParagraphRevision}
\end{document}
"""
    t0 = time.time()
    res_pr = compile_tex_snippet(tex_pr, "challenger_pr_scoping")
    d_pr = time.time() - t0
    if not res_pr.pdf_exists or res_pr.fatal_error:
        print(f"    ❌ COMPILATION FAILED: {res_pr.stderr}")
        all_passed = False
        t7_status = "FAIL"
        t7_details = {"error": "Compilation failed"}
    else:
        total_lines, lines_per_page, page_count = inspect_drawn_writing_lines(res_pr.pdf_path)
        expected_total = 4 + 12 + 2  # 18
        t7_pass = (total_lines == expected_total and res_pr.overfull_count == 0)
        if not t7_pass:
            all_passed = False
        t7_status = "PASS" if t7_pass else "FAIL"
        print(f"    ParagraphRevision (4 + 12 + 2 = 18): {'✔ PASS' if t7_pass else '❌ FAIL'} | pages={page_count} | lines_per_page={lines_per_page} (total={total_lines}/18) | overfull={res_pr.overfull_count} | time={d_pr:.2f}s")
        t7_details = {
            "page_count": page_count,
            "lines_per_page": lines_per_page,
            "total_lines_drawn": total_lines,
            "expected_lines": expected_total,
            "overfull_hboxes": res_pr.overfull_count,
            "duration": round(d_pr, 3)
        }
    results["TEST_7_PARAGRAPH_REVISION_SCOPING"] = {"status": t7_status, "details": t7_details}

    # Final Verdict Summary
    verdict = "APPROVE" if all_passed else "FAIL"
    print("\n" + "=" * 80)
    print(f" EMPIRICAL CHALLENGER VERDICT: {verdict}")
    print("=" * 80)

    report_path = Path("/lzcapp/document/academic_english_book/tests/challenger_verification_report.json")
    report_data = {
        "verdict": verdict,
        "all_passed": all_passed,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": results
    }
    report_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
    print(f"Detailed JSON report saved to: {report_path}")

    return report_data

if __name__ == "__main__":
    run_deep_verification()
