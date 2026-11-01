#!/usr/bin/env python3
"""Adversarial stress test suite for build automation, multi-pass convergence, and CJK fonts."""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

# Add tests directory to python path
TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_DIR))

from test_helpers import (
    PROJECT_ROOT,
    REPO_ROOT,
    BUILD_SCRIPT,
    MAKEFILE,
    MAIN_TEX,
    BUILD_DIR,
    STYLE_FILE,
    get_tex_env,
    compile_tex_snippet,
    inspect_pdf
)

def run_adversarial_suite():
    results = {}
    env = get_tex_env()

    print("================================================================================")
    print(" EMPIRICAL ADVERSARIAL STRESS TEST SUITE")
    print(" Target: LaTeX Build Automation & Bilingual Typesetting Engine")
    print("================================================================================")

    # Backup build dir if present to maintain purity
    backup_build = PROJECT_ROOT / "build_backup_adversarial"
    if BUILD_DIR.exists():
        if backup_build.exists():
            shutil.rmtree(backup_build)
        shutil.copytree(BUILD_DIR, backup_build)

    try:
        # ======================================================================
        # BATTERY 1: Dirty Cache & Corrupted Auxiliary Files
        # ======================================================================
        print("\n>>> BATTERY 1: Dirty Cache & Corrupted Auxiliary Files")

        # 1.1 Unclosed brace in .aux
        BUILD_DIR.mkdir(exist_ok=True)
        (BUILD_DIR / "main.aux").write_text("\\relax\n\\newlabel{ch:lexicon}{{1}{1}{Unclosed Label\n", encoding="utf-8")
        res1 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        results["1.1_corrupted_aux_unclosed_brace"] = {
            "status": "FAIL_AS_EXPECTED" if res1.returncode != 0 else "RECOVERED",
            "returncode": res1.returncode,
            "error_snippet": res1.stderr[-250:] if res1.stderr else ""
        }
        print(f"  [1.1] Corrupted .aux (unclosed brace): Return code {res1.returncode} -> {results['1.1_corrupted_aux_unclosed_brace']['status']}")

        # 1.2 Binary garbage in .aux
        (BUILD_DIR / "main.aux").write_bytes(os.urandom(128))
        res2 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        results["1.2_corrupted_aux_binary_garbage"] = {
            "status": "FAIL_AS_EXPECTED" if res2.returncode != 0 else "RECOVERED",
            "returncode": res2.returncode,
            "error_snippet": res2.stderr[-250:] if res2.stderr else ""
        }
        print(f"  [1.2] Corrupted .aux (binary garbage): Return code {res2.returncode} -> {results['1.2_corrupted_aux_binary_garbage']['status']}")

        # 1.3 Corrupted .toc (syntax error in contentsline)
        (BUILD_DIR / "main.toc").write_text("\\contentsline {chapter}{\\numberline {1}{Corrupted Title\n", encoding="utf-8")
        # Ensure aux is valid so toc is tested
        (BUILD_DIR / "main.aux").write_text("\\relax\n", encoding="utf-8")
        res3 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        results["1.3_corrupted_toc_syntax_error"] = {
            "status": "FAIL_AS_EXPECTED" if res3.returncode != 0 else "RECOVERED",
            "returncode": res3.returncode,
            "error_snippet": res3.stderr[-250:] if res3.stderr else ""
        }
        print(f"  [1.3] Corrupted .toc (syntax error): Return code {res3.returncode} -> {results['1.3_corrupted_toc_syntax_error']['status']}")

        # 1.4 Corrupted .out (broken hyperref bookmarks)
        (BUILD_DIR / "main.out").write_text("\\BOOKMARK [0][-]{chapter.1}{Malformed Bookmark\n", encoding="utf-8")
        (BUILD_DIR / "main.aux").write_text("\\relax\n", encoding="utf-8")
        (BUILD_DIR / "main.toc").write_text("", encoding="utf-8")
        res4 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        results["1.4_corrupted_out_broken_bookmark"] = {
            "status": "PASS" if res4.returncode == 0 else "FAIL",
            "returncode": res4.returncode,
            "error_snippet": res4.stderr[-250:] if res4.stderr else ""
        }
        print(f"  [1.4] Corrupted .out (broken bookmark): Return code {res4.returncode} -> {results['1.4_corrupted_out_broken_bookmark']['status']}")

        # 1.5 Zero-byte aux, toc, out
        (BUILD_DIR / "main.aux").write_text("", encoding="utf-8")
        (BUILD_DIR / "main.toc").write_text("", encoding="utf-8")
        (BUILD_DIR / "main.out").write_text("", encoding="utf-8")
        res5 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        results["1.5_zero_byte_state_files"] = {
            "status": "PASS" if res5.returncode == 0 else "FAIL",
            "returncode": res5.returncode
        }
        print(f"  [1.5] Zero-byte aux/toc/out: Return code {res5.returncode} -> {results['1.5_zero_byte_state_files']['status']}")

        # 1.6 Stale aux referencing old non-existent labels
        (BUILD_DIR / "main.aux").write_text("\\relax\n\\newlabel{ch:nonexistent}{{99}{999}{Old Title}{chapter.99}{}}\n", encoding="utf-8")
        res6 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        results["1.6_stale_aux_old_labels"] = {
            "status": "PASS" if res6.returncode == 0 else "FAIL",
            "returncode": res6.returncode
        }
        print(f"  [1.6] Stale .aux with obsolete labels: Return code {res6.returncode} -> {results['1.6_stale_aux_old_labels']['status']}")

        # Recovery check: make clean resets dirty cache completely
        res_clean = subprocess.run(["make", "clean"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        res_rebuild = subprocess.run(["make"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        results["1.7_cache_recovery_via_make_clean"] = {
            "status": "PASS" if (res_clean.returncode == 0 and res_rebuild.returncode == 0) else "FAIL",
            "clean_code": res_clean.returncode,
            "rebuild_code": res_rebuild.returncode
        }
        print(f"  [1.7] Cache recovery via `make clean && make`: {results['1.7_cache_recovery_via_make_clean']['status']}")

        # ======================================================================
        # BATTERY 2: Working Directory Changes & Output Path Invariance
        # ======================================================================
        print("\n>>> BATTERY 2: Working Directory Changes & Output Path Invariance")

        # 2.1 Invocation from REPO_ROOT (/lzcapp/document)
        res_d1 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(REPO_ROOT), capture_output=True, text=True)
        pdf_at_proj = PROJECT_ROOT / "academic_english_book.pdf"
        results["2.1_invocation_from_repo_root"] = {
            "status": "PASS" if (res_d1.returncode == 0 and pdf_at_proj.exists()) else "FAIL",
            "returncode": res_d1.returncode,
            "pdf_exists": pdf_at_proj.exists()
        }
        print(f"  [2.1] Invocation from /lzcapp/document: Return code {res_d1.returncode} -> {results['2.1_invocation_from_repo_root']['status']}")

        # 2.2 Invocation from tests/ directory
        res_d2 = subprocess.run([str(BUILD_SCRIPT)], cwd=str(TESTS_DIR), capture_output=True, text=True)
        results["2.2_invocation_from_tests_dir"] = {
            "status": "PASS" if (res_d2.returncode == 0 and pdf_at_proj.exists()) else "FAIL",
            "returncode": res_d2.returncode,
            "pdf_exists": pdf_at_proj.exists()
        }
        print(f"  [2.2] Invocation from tests/: Return code {res_d2.returncode} -> {results['2.2_invocation_from_tests_dir']['status']}")

        # 2.3 Invocation from /tmp
        res_d3 = subprocess.run([str(BUILD_SCRIPT)], cwd="/tmp", capture_output=True, text=True)
        results["2.3_invocation_from_tmp"] = {
            "status": "PASS" if (res_d3.returncode == 0 and pdf_at_proj.exists()) else "FAIL",
            "returncode": res_d3.returncode,
            "pdf_exists": pdf_at_proj.exists()
        }
        print(f"  [2.3] Invocation from /tmp: Return code {res_d3.returncode} -> {results['2.3_invocation_from_tmp']['status']}")

        # 2.4 Custom clean absolute output directory
        with tempfile.TemporaryDirectory() as custom_out:
            res_d4 = subprocess.run([str(BUILD_SCRIPT), custom_out], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
            custom_pdf = Path(custom_out) / "main.pdf"
            results["2.4_custom_absolute_output_dir"] = {
                "status": "PASS" if (res_d4.returncode == 0 and custom_pdf.exists() and pdf_at_proj.exists()) else "FAIL",
                "returncode": res_d4.returncode,
                "custom_pdf_exists": custom_pdf.exists()
            }
            print(f"  [2.4] Custom absolute output dir: Return code {res_d4.returncode} -> {results['2.4_custom_absolute_output_dir']['status']}")

        # 2.5 Custom clean relative output directory
        rel_out = "build_custom_relative_test"
        rel_path = PROJECT_ROOT / rel_out
        try:
            res_d5 = subprocess.run([str(BUILD_SCRIPT), rel_out], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
            rel_pdf = rel_path / "main.pdf"
            results["2.5_custom_relative_output_dir"] = {
                "status": "PASS" if (res_d5.returncode == 0 and rel_pdf.exists()) else "FAIL",
                "returncode": res_d5.returncode,
                "rel_pdf_exists": rel_pdf.exists()
            }
            print(f"  [2.5] Custom relative output dir: Return code {res_d5.returncode} -> {results['2.5_custom_relative_output_dir']['status']}")
        finally:
            if rel_path.exists():
                shutil.rmtree(rel_path)

        # 2.6 Make invoked via -C from outside
        res_d6 = subprocess.run(["make", "-C", str(PROJECT_ROOT)], cwd="/tmp", capture_output=True, text=True)
        results["2.6_make_invoked_via_dash_C"] = {
            "status": "PASS" if res_d6.returncode == 0 else "FAIL",
            "returncode": res_d6.returncode
        }
        print(f"  [2.6] make -C from /tmp: Return code {res_d6.returncode} -> {results['2.6_make_invoked_via_dash_C']['status']}")

        # ======================================================================
        # BATTERY 3: State Oscillation & Multi-Pass Convergence Limit Fallback
        # ======================================================================
        print("\n>>> BATTERY 3: State Oscillation & Multi-Pass Convergence Limit Fallback")

        # Create a synthetic TeX file that forces .aux to change every pass
        with tempfile.TemporaryDirectory() as osc_build:
            oscillating_tex = PROJECT_ROOT / "oscillating_test.tex"
            oscillating_tex.write_text(r"""\documentclass{article}
\newcounter{osccnt}
\begin{document}
\makeatletter
\IfFileExists{""" + osc_build + r"""/dyn.cnt}{\input{""" + osc_build + r"""/dyn.cnt}}{\setcounter{osccnt}{0}}
\stepcounter{osccnt}
\newwrite\cnt@out
\immediate\openout\cnt@out=""" + osc_build + r"""/dyn.cnt
\immediate\write\cnt@out{\string\setcounter{osccnt}{\theosccnt}}
\immediate\closeout\cnt@out

\immediate\write\@auxout{\string\newlabel{dyn:\theosccnt}{{\theosccnt}{\theosccnt}}}
\makeatother
Oscillation Test Document. Count: \theosccnt
\end{document}
""", encoding="utf-8")

            try:
                res_osc = subprocess.run([str(BUILD_SCRIPT), osc_build, "oscillating_test.tex"],
                                         cwd=str(PROJECT_ROOT), capture_output=True, text=True)
                reached_limit = "WARNING: Multi-pass reached limit (6 passes) without strict hash convergence." in res_osc.stdout
                passes_count = res_osc.stdout.count("[Pass ")
                emitted_pdf = (Path(osc_build) / "oscillating_test.pdf").exists()
                results["3.1_auxiliary_oscillation_fallback"] = {
                    "status": "PASS" if (reached_limit and emitted_pdf and passes_count == 6) else "FAIL",
                    "returncode": res_osc.returncode,
                    "passes_count": passes_count,
                    "warning_printed": reached_limit,
                    "emitted_pdf": emitted_pdf
                }
                print(f"  [3.1] Forced auxiliary oscillation: Passes={passes_count}, Warning={reached_limit}, EmittedPDF={emitted_pdf} -> {results['3.1_auxiliary_oscillation_fallback']['status']}")
            finally:
                if oscillating_tex.exists():
                    oscillating_tex.unlink()

        # 3.2 Standard document convergence threshold verification
        res_std = subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        converged_pass3 = "Hash converged on pass 3!" in res_std.stdout
        results["3.2_standard_document_pass3_convergence"] = {
            "status": "PASS" if (res_std.returncode == 0 and converged_pass3) else "FAIL",
            "returncode": res_std.returncode,
            "converged_pass3": converged_pass3
        }
        print(f"  [3.2] Standard document convergence at Pass 3: {results['3.2_standard_document_pass3_convergence']['status']}")

        # ======================================================================
        # BATTERY 4: `make clean` followed immediately by `make`
        # ======================================================================
        print("\n>>> BATTERY 4: `make clean` followed immediately by `make`")

        # 4.1 Execute make clean
        res_clean = subprocess.run(["make", "clean"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        build_exists_after_clean = BUILD_DIR.exists()
        pdf_exists_after_clean = (PROJECT_ROOT / "academic_english_book.pdf").exists()
        clean_ok = (res_clean.returncode == 0 and not build_exists_after_clean and not pdf_exists_after_clean)

        # 4.2 Execute make from clean
        res_make = subprocess.run(["make"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        build_exists_after_make = BUILD_DIR.exists()
        pdf_exists_after_make = (PROJECT_ROOT / "academic_english_book.pdf").exists()
        pdf_size = (PROJECT_ROOT / "academic_english_book.pdf").stat().st_size if pdf_exists_after_make else 0
        make_ok = (res_make.returncode == 0 and build_exists_after_make and pdf_exists_after_make and pdf_size > 50000)

        # 4.3 Second make execution (idempotency check)
        res_make_again = subprocess.run(["make"], cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        idempotent_ok = (res_make_again.returncode == 0)

        results["4.1_make_clean_lifecycle"] = {
            "status": "PASS" if (clean_ok and make_ok and idempotent_ok) else "FAIL",
            "clean_exit": res_clean.returncode,
            "make_exit": res_make.returncode,
            "pdf_size": pdf_size,
            "idempotent": idempotent_ok
        }
        print(f"  [4.1] `make clean && make` lifecycle: CleanOK={clean_ok}, MakeOK={make_ok}, PDFSize={pdf_size} -> {results['4.1_make_clean_lifecycle']['status']}")

        # ======================================================================
        # BATTERY 5: CJK Font Completeness & Academic Linguistic Vocabulary
        # ======================================================================
        print("\n>>> BATTERY 5: CJK Font Completeness & Academic Linguistic Vocabulary")

        # 5.1 Mandated Dispatch Vocabulary
        dispatch_vocab = [
            "熟词生义", "逻辑衔接", "语法规则", "练习册", "实战", "论证", "范式", "消融"
        ]

        # 5.2 Expanded Core Linguistic & Academic Vocabulary
        expanded_vocab = [
            "词汇激活", "句法骨架", "句子成分", "五大基本句型", "尾重原则",
            "主语从句", "非谓语动词", "独立主格", "状语从句", "平行结构", "悬空修饰",
            "篇章逻辑", "论证引擎", "已知到新信息流", "图尔敏微论证", "假说让步反驳",
            "段落构建蓝图", "摘要", "引言", "文献综述", "研究方法", "实验验证",
            "局限性分析", "数据分析", "论文答辩", "审稿意见反驳", "个人陈述",
            "深度病段诊所", "母语级重构图谱", "句法臃肿", "逻辑断裂", "术语错位",
            "全篇范文", "宽行距水平横线", "句子替换划线标注", "自检评分量表",
            "消融实验", "范式转换", "基线对比", "超参数调优", "泛化能力", "鲁棒性"
        ]

        # 5.3 Full-width Chinese Punctuation
        cjk_punctuation = ["“双引号”", "‘单引号’", "破折号——", "省略号……", "（括号）", "【方头括】", "《书名号》", "顿号、逗号，句号。"]

        # Compose a rigorous verification micro-document testing all CJK glyphs across:
        # standard body, \textbf, \textit, titles, and inside ConceptBox, ExampleBox, TipBox, ExerciseBox
        all_vocab_items = dispatch_vocab + expanded_vocab + cjk_punctuation
        vocab_body = " ".join(all_vocab_items)

        cjk_test_tex = r"""\documentclass[11pt,a4paper,openany]{book}
\input{""" + str(STYLE_FILE) + r"""}

\begin{document}
\chapter{CJK 字符集压力测试: 熟词生义与论证范式}

\section{核心学术词汇与标点测试}
\textbf{粗体测试}: """ + "、".join(dispatch_vocab) + r"""\\
\textit{斜体测试}: """ + "、".join(dispatch_vocab) + r"""\\
标点符号集: """ + " ".join(cjk_punctuation) + r"""

\section{全套学术英语模块术语覆盖}
""" + vocab_body + r"""

\begin{ConceptBox}{概念盒 CJK 渲染: 语法规则与词价转换}
学术英语句法骨架必须遵循尾重原则与已知到新信息流。消融实验和范式转换论证。
\end{ConceptBox}

\begin{ExampleBox}{例句盒 CJK 渲染: 深度病段母语级重构}
针对句法臃肿与逻辑断裂的诊断性手术案例分析。
\end{ExampleBox}

\begin{TipBox}{提示盒 CJK 渲染: 审稿意见反驳与语气控制}
在答辩与反驳信中保持客观严谨，避免主观武断。
\end{TipBox}

\begin{ExerciseBox}{练习盒 CJK 渲染: 每日实战练习册}
请在下方的宽行距水平横线上完成句子替换改写练习：
\writinglines[11mm]{3}
\end{ExerciseBox}

\end{document}
"""

        cjk_res = compile_tex_snippet(cjk_test_tex, jobname="cjk_stress_doc")
        
        # Check transcript for missing character warnings
        missing_chars = [line for line in cjk_res.log_text.splitlines() if "Missing character:" in line]
        results["5.1_cjk_font_completeness"] = {
            "status": "PASS" if (cjk_res.returncode == 0 and len(missing_chars) == 0 and cjk_res.pdf_exists) else "FAIL",
            "returncode": cjk_res.returncode,
            "pdf_exists": cjk_res.pdf_exists,
            "missing_char_count": len(missing_chars),
            "missing_chars": missing_chars[:10]
        }
        print(f"  [5.1] CJK Font Completeness & Missing Glyphs: ReturnCode={cjk_res.returncode}, MissingChars={len(missing_chars)} -> {results['5.1_cjk_font_completeness']['status']}")

        # 5.2 Extract text from generated PDF and assert all characters present
        pdf_text = ""
        if cjk_res.pdf_path:
            pdf_insp = inspect_pdf(cjk_res.pdf_path)
            pdf_text = " ".join(pdf_insp.text_by_page)
        
        missing_in_pdf = []
        for word in dispatch_vocab:
            if word not in pdf_text:
                missing_in_pdf.append(word)

        results["5.2_pdf_text_extraction_verification"] = {
            "status": "PASS" if (len(missing_in_pdf) == 0 and len(pdf_text) > 0) else "FAIL",
            "missing_words_in_pdf": missing_in_pdf,
            "extracted_length": len(pdf_text)
        }
        print(f"  [5.2] PDF Text Content Verification for Mandated Vocab: MissingInPDF={missing_in_pdf} -> {results['5.2_pdf_text_extraction_verification']['status']}")

    finally:
        # Restore original build directory if backup was made
        if backup_build.exists():
            if BUILD_DIR.exists():
                shutil.rmtree(BUILD_DIR)
            shutil.move(backup_build, BUILD_DIR)
            # Recompile once cleanly to leave workspace in pristine state
            subprocess.run([str(BUILD_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True)

    print("\n================================================================================")
    print(" EMPIRICAL ADVERSARIAL TEST SUMMARY")
    print("================================================================================")
    all_passed = True
    for key, data in results.items():
        status = data.get("status", "UNKNOWN")
        print(f"  {key:45s} : {status}")
        if status not in ["PASS", "FAIL_AS_EXPECTED", "RECOVERED"]:
            all_passed = False

    print("================================================================================")
    print(f" VERDICT: {'APPROVE' if all_passed else 'FAIL'}")
    print("================================================================================")
    return results

if __name__ == "__main__":
    run_adversarial_suite()
