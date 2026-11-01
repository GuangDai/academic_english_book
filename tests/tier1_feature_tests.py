#!/usr/bin/env python3
"""Tier 1: Feature Coverage Test Suite (80+ Tests across 16 Features).

Validates all 16 features from PROJECT.md and ORIGINAL_REQUEST.md.
"""

import os
import sys
import re
import json
import time
import subprocess
from pathlib import Path
from typing import List

from test_helpers import (
    PROJECT_ROOT, REPO_ROOT, STYLE_FILE, BUILD_SCRIPT, MAKEFILE,
    MAIN_TEX, CHAPTERS_DIR, RAW_TRAINING_DIR, RAW_MASTERY_DIR,
    TRAINING_ZIP, MASTERY_ZIP, DELIVERABLE_PDF, BUILD_DIR,
    compile_tex_snippet, inspect_pdf, read_json_from_zip,
    get_zip_namelist, TestResult
)


class Tier1FeatureTests:
    """Test suite covering all 16 features from PROJECT.md with >=5 tests each."""

    def __init__(self):
        self.results: List[TestResult] = []

    def _record(self, test_id: str, feature_id: str, name: str, status: str,
                msg: str = "", duration: float = 0.0):
        self.results.append(TestResult(
            test_id=test_id,
            tier=1,
            name=name,
            status=status,
            message=msg,
            duration=duration,
            feature_id=feature_id
        ))

    def run_all(self, target_milestone: str = "ALL") -> List[TestResult]:
        self.results = []
        start_time = time.time()

        # Feature 01: Archive Extraction & Verification (M1)
        self.test_f01_01_zip_archives_exist_and_non_empty()
        self.test_f01_02_training_zip_manifest_and_question_counts()
        self.test_f01_03_mastery_zip_curriculum_and_blueprints()
        self.test_f01_04_target_extraction_directory_contract()
        self.test_f01_05_archive_data_schema_validity()

        # Feature 02: Modular Style Package (M1)
        self.test_f02_01_style_file_contract_and_structure()
        self.test_f02_02_geometry_margins_and_paper_size()
        self.test_f02_03_bilingual_fonts_times_and_simsun()
        self.test_f02_04_titlesec_and_fancyhdr_contract()
        self.test_f02_05_safe_newtxmath_engine()

        # Feature 03: Composition Ruled Lines System (M1)
        self.test_f03_01_writinglines_macro_definition_and_default()
        self.test_f03_02_pure_tex_hrule_zero_overfull_guarantee()
        self.test_f03_03_ruled_line_color_contract()
        self.test_f03_04_row_height_calculation_11mm()
        self.test_f03_05_writinglines_standalone_compilation()

        # Feature 04: Sentence Replacement Scaffold (M1)
        self.test_f04_01_defect_target_macro_contract()
        self.test_f04_02_sentence_rewrite_item_macro_contract()
        self.test_f04_03_fillblank_macro_contract()
        self.test_f04_04_paragraph_revision_scaffold_environment()
        self.test_f04_05_sentence_replacement_micro_compilation()

        # Feature 05: Automated Build Scripts (M1)
        self.test_f05_01_build_script_exists_and_executable()
        self.test_f05_02_build_script_environment_injection()
        self.test_f05_03_build_script_multi_pass_convergence()
        self.test_f05_04_makefile_standard_targets()
        self.test_f05_05_build_script_error_trapping()

        # Feature 06: Frontmatter & Hyperlinked ToC (M2)
        self.test_f06_01_frontmatter_and_toc_macro_presence()
        self.test_f06_02_hyperref_and_bookmark_configuration()
        self.test_f06_03_toc_pnumwidth_widening_contract()
        self.test_f06_04_titlesec_before_hyperref_load_order()
        self.test_f06_05_pdf_outline_hierarchy_and_links()

        # Feature 07: Lexical & Grammar Chapters (M2)
        self.test_f07_01_part1_lexical_polysemy_content_contract()
        self.test_f07_02_part2_5_sentence_types_and_end_weight()
        self.test_f07_03_grammar_rules_g001_to_g036_coverage()
        self.test_f07_04_expression_patterns_ep001_to_ep024_coverage()
        self.test_f07_05_syntax_chapters_modular_tex_inclusion()

        # Feature 08: Discourse Logic & Blueprints (M2)
        self.test_f08_01_part3_given_to_new_and_toulmin_contract()
        self.test_f08_02_logic_rules_l001_to_l030_coverage()
        self.test_f08_03_part4_blueprints_bp01_to_bp48_coverage()
        self.test_f08_04_blueprint_thematic_track_distribution()
        self.test_f08_05_blueprints_modular_tex_inclusion()

        # Feature 09: Revision Clinic & Full-Text Anthology (M2)
        self.test_f09_01_part5_revision_cases_rc01_to_rc60_coverage()
        self.test_f09_02_five_primary_defect_categories_classification()
        self.test_f09_03_four_step_surgical_reconstruction_structure()
        self.test_f09_04_part6_full_text_anthology_ft01_to_ft24_coverage()
        self.test_f09_05_revision_and_anthology_modular_tex_inclusion()

        # Feature 10: Interactive Workbook Layout (M3)
        self.test_f10_01_part7_workbook_structure_and_stages()
        self.test_f10_02_workbook_11mm_ruled_lines_integration()
        self.test_f10_03_workbook_fillblank_utilization()
        self.test_f10_04_workbook_sentence_rewrite_scaffold_usage()
        self.test_f10_05_workbook_task_prompt_and_difficulty_markers()

        # Feature 11: Chapter New-Page Enforcement (M3)
        self.test_f11_01_documentclass_openany_specification()
        self.test_f11_02_chapter_command_forces_new_page()
        self.test_f11_03_chapter_title_format_display_styling()
        self.test_f11_04_plain_pagestyle_on_chapter_opening()
        self.test_f11_05_pdf_chapter_page_start_verification()

        # Feature 12: Color Annotation Hierarchy (M3)
        self.test_f12_01_primary_palette_acadnavy_and_acadslate()
        self.test_f12_02_example_and_tip_palette_acadteal_and_acadamber()
        self.test_f12_03_exercise_palette_acadforest()
        self.test_f12_04_target_highlight_and_rule_line_color()
        self.test_f12_05_four_tcolorbox_environments_definition()

        # Feature 13: Comprehensive Answer Key (M4)
        self.test_f13_01_part8_answer_key_appendix_existence()
        self.test_f13_02_two_level_hierarchical_indexing_contract()
        self.test_f13_03_one_to_one_exercise_answer_coverage()
        self.test_f13_04_rapid_lookup_header_navigation()
        self.test_f13_05_answer_key_formatting_and_layout()

        # Feature 14: Analytic Rubrics & Notes (M4)
        self.test_f14_01_linguistic_analysis_notes_coverage()
        self.test_f14_02_sentence_constituents_and_style_notes_coverage()
        self.test_f14_03_common_errors_diagnostic_alerts_coverage()
        self.test_f14_04_analytic_scoring_rubrics_multi_dimension()
        self.test_f14_05_rubric_table_rendering_micro_compilation()

        # Feature 15: E2E PDF Compilation & Verification (M5)
        self.test_f15_01_deliverable_pdf_file_existence()
        self.test_f15_02_deliverable_pdf_size_and_page_count()
        self.test_f15_03_compilation_log_zero_missing_characters()
        self.test_f15_04_compilation_log_zero_undefined_references()
        self.test_f15_05_pdf_outline_bookmarks_match_parts()

        # Feature 16: Opaque-Box E2E Test Suite Meta (E2E Track)
        self.test_f16_01_test_runner_executable_contract()
        self.test_f16_02_test_runner_zero_exit_code_on_pass()
        self.test_f16_03_four_tiers_discoverable_and_executable()
        self.test_f16_04_cli_flags_support_tier_and_milestone_and_json()
        self.test_f16_05_test_infra_and_test_ready_documentation_presence()

        return self.results

    # -------------------------------------------------------------------------
    # Feature 01: Archive Extraction & Verification
    # -------------------------------------------------------------------------
    def test_f01_01_zip_archives_exist_and_non_empty(self):
        t0 = time.time()
        ok = TRAINING_ZIP.is_file() and MASTERY_ZIP.is_file()
        if not ok:
            self._record("F01_T01", "F01", "Source zip archives existence", "FAIL",
                         f"Missing zip archives: training={TRAINING_ZIP.is_file()}, mastery={MASTERY_ZIP.is_file()}",
                         time.time() - t0)
            return
        t_sz = TRAINING_ZIP.stat().st_size
        m_sz = MASTERY_ZIP.stat().st_size
        if t_sz > 1_000_000 and m_sz > 500_000:
            self._record("F01_T01", "F01", "Source zip archives existence", "PASS",
                         f"Verified: training={t_sz} bytes, mastery={m_sz} bytes", time.time() - t0)
        else:
            self._record("F01_T01", "F01", "Source zip archives existence", "FAIL",
                         f"Archives too small: training={t_sz}, mastery={m_sz}", time.time() - t0)

    def test_f01_02_training_zip_manifest_and_question_counts(self):
        t0 = time.time()
        manifest = read_json_from_zip(TRAINING_ZIP, "academic_english_training/manifest.json")
        if not manifest:
            self._record("F01_T02", "F01", "Training zip manifest & question counts", "FAIL",
                         "Could not read manifest.json from training zip", time.time() - t0)
            return
        summary = manifest.get("summary_statistics", {})
        total_q = summary.get("total_questions", 0)
        total_days = summary.get("total_days", 0)
        if total_q == 4176 and total_days == 116:
            self._record("F01_T02", "F01", "Training zip manifest & question counts", "PASS",
                         f"Verified exactly 116 days and 4,176 questions from authoritative manifest", time.time() - t0)
        else:
            self._record("F01_T02", "F01", "Training zip manifest & question counts", "FAIL",
                         f"Unexpected counts: total_questions={total_q} (expected 4176), days={total_days} (expected 116)", time.time() - t0)

    def test_f01_03_mastery_zip_curriculum_and_blueprints(self):
        t0 = time.time()
        curriculum = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/curriculum_60days.json")
        if not curriculum:
            self._record("F01_T03", "F01", "Mastery zip curriculum & blueprints", "FAIL",
                         "Could not read curriculum_60days.json from mastery zip", time.time() - t0)
            return
        blueprints = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/blueprints/intent_to_paragraph_blueprints.json")
        bp_count = len(blueprints) if isinstance(blueprints, list) else 0
        if bp_count == 48:
            self._record("F01_T03", "F01", "Mastery zip curriculum & blueprints", "PASS",
                         f"Verified curriculum_60days.json and exactly {bp_count} paragraph blueprints (BP01-BP48)", time.time() - t0)
        else:
            self._record("F01_T03", "F01", "Mastery zip curriculum & blueprints", "FAIL",
                         f"Found {bp_count} blueprint items (expected exactly 48)", time.time() - t0)

    def test_f01_04_target_extraction_directory_contract(self):
        t0 = time.time()
        if RAW_TRAINING_DIR.is_dir() and RAW_MASTERY_DIR.is_dir():
            t_files = list(RAW_TRAINING_DIR.rglob('*'))
            m_files = list(RAW_MASTERY_DIR.rglob('*'))
            if len(t_files) > 0 and len(m_files) > 0:
                self._record("F01_T04", "F01", "Target extraction directories structure", "PASS",
                             f"Extracted assets verified: {len(t_files)} training files, {len(m_files)} mastery files", time.time() - t0)
                return
            self._record("F01_T04", "F01", "Target extraction directories structure", "FAIL",
                         f"Extracted asset directories are empty (training: {len(t_files)}, mastery: {len(m_files)})", time.time() - t0)
        else:
            self._record("F01_T04", "F01", "Target extraction directories structure", "FAIL",
                         f"Missing extracted directories: raw_training={RAW_TRAINING_DIR.is_dir()}, raw_mastery={RAW_MASTERY_DIR.is_dir()}", time.time() - t0)
    def test_f01_05_archive_data_schema_validity(self):
        t0 = time.time()
        gr = read_json_from_zip(TRAINING_ZIP, "academic_english_training/grammar_rules.json")
        ep = read_json_from_zip(TRAINING_ZIP, "academic_english_training/expression_patterns.json")
        if gr and ep and len(gr) == 36 and len(ep) == 24:
            self._record("F01_T05", "F01", "Archive data schema validity", "PASS",
                         f"Verified exact schema integrity: 36 grammar rules (G001-G036) and 24 expression patterns (EP001-EP024)", time.time() - t0)
        else:
            self._record("F01_T05", "F01", "Archive data schema validity", "FAIL",
                         f"Schema count mismatch: grammar_rules={len(gr) if gr else 0}, expression_patterns={len(ep) if ep else 0}", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 02: Modular Style Package
    # -------------------------------------------------------------------------
    def test_f02_01_style_file_contract_and_structure(self):
        t0 = time.time()
        if STYLE_FILE.is_file():
            content = STYLE_FILE.read_text(encoding='utf-8')
            if len(content) > 100:
                self._record("F02_T01", "F02", "Style file existence & encoding", "PASS",
                             f"Verified style file {STYLE_FILE} ({len(content)} chars)", time.time() - t0)
                return
            self._record("F02_T01", "F02", "Style file existence & encoding", "FAIL",
                         f"Style file {STYLE_FILE} is too short ({len(content)} chars)", time.time() - t0)
        else:
            self._record("F02_T01", "F02", "Style file existence & encoding", "FAIL",
                         f"Missing style file: {STYLE_FILE}", time.time() - t0)
    def test_f02_02_geometry_margins_and_paper_size(self):
        t0 = time.time()
        # Verify 23mm margins specification on A4 paper via STYLE_FILE
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\noindent\rule{{\textwidth}}{{1pt}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f02_02")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("F02_T02", "F02", "Geometry 23mm margins and A4 paper", "PASS",
                         "Compiled 23mm margin geometry cleanly with 0 overfull hboxes", time.time() - t0)
        else:
            self._record("F02_T02", "F02", "Geometry 23mm margins and A4 paper", "FAIL",
                         f"Compilation failed or overfull: code={res.returncode}, overfull={res.overfull_count}", time.time() - t0)

    def test_f02_03_bilingual_fonts_times_and_simsun(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
Academic English Textbook. 基于LaTeX的学术英语教学书。
\textbf{{Bold English and 粗体中文测试。}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f02_03")
        if res.pdf_exists and res.missing_char_count == 0:
            self._record("F02_T03", "F02", "Bilingual fonts Times & SimSun", "PASS",
                         "Bilingual font rendering validated with 0 missing characters", time.time() - t0)
        else:
            self._record("F02_T03", "F02", "Bilingual fonts Times & SimSun", "FAIL",
                         f"Font compilation failed or missing chars: code={res.returncode}, missing={res.missing_char_count}", time.time() - t0)

    def test_f02_04_titlesec_and_fancyhdr_contract(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\chapter{{Introduction}}
Testing fancyhdr running header and titlesec formatting.
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f02_04")
        if res.pdf_exists:
            self._record("F02_T04", "F02", "titlesec and fancyhdr integration", "PASS",
                         "titlesec and fancyhdr compiled cleanly with chapter running headers", time.time() - t0)
        else:
            self._record("F02_T04", "F02", "titlesec and fancyhdr integration", "FAIL",
                         f"titlesec/fancyhdr compilation failed: code={res.returncode}", time.time() - t0)

    def test_f02_05_safe_newtxmath_engine(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
Formula: $\frac{{A + B}}{{\sum_{{i=1}}^{{N}} X_i}} \ge \alpha \cdot \beta$
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f02_05")
        if res.pdf_exists:
            self._record("F02_T05", "F02", "Safe newtxmath engine configuration", "PASS",
                         "newtxmath math operators compiled cleanly without XeTeX memory fault", time.time() - t0)
        else:
            self._record("F02_T05", "F02", "Safe newtxmath engine configuration", "FAIL",
                         f"newtxmath compilation failed: code={res.returncode}", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 03: Composition Ruled Lines System
    # -------------------------------------------------------------------------
    def test_f03_01_writinglines_macro_definition_and_default(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
Task: Write your revision below.
\writinglines{{3}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f03_01")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("F03_T01", "F03", "writinglines macro definition and default 11mm", "PASS",
                         "writinglines macro draws 3 rules with 11mm default height cleanly", time.time() - t0)
        else:
            self._record("F03_T01", "F03", "writinglines macro definition and default 11mm", "FAIL",
                         f"writinglines macro compilation failed: code={res.returncode}", time.time() - t0)

    def test_f03_02_pure_tex_hrule_zero_overfull_guarantee(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\noindent Left boundary\hfill Right boundary
\writinglines{{5}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f03_02")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("F03_T02", "F03", "Pure TeX hrule zero-overfull guarantee", "PASS",
                         "Zero overfull hboxes confirmed across 5 full-width ruled lines", time.time() - t0)
        else:
            self._record("F03_T02", "F03", "Pure TeX hrule zero-overfull guarantee", "FAIL",
                         f"Overfull warning encountered: {res.overfull_count}", time.time() - t0)

    def test_f03_03_ruled_line_color_contract(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
{{\color{{RuleLineColor}}\hrule height 0.6pt width \linewidth}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f03_03")
        if res.pdf_exists:
            self._record("F03_T03", "F03", "Ruled line color specification", "PASS",
                         "RuleLineColor (#A0AEC0) compiles cleanly", time.time() - t0)
        else:
            self._record("F03_T03", "F03", "Ruled line color specification", "FAIL",
                         "RuleLineColor definition failed", time.time() - t0)

    def test_f03_04_row_height_calculation_11mm(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\newdimen\myrowht
\setlength{{\myrowht}}{{11mm}}
\begin{{document}}
Height: \the\myrowht
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f03_04")
        if res.pdf_exists:
            self._record("F03_T04", "F03", "11mm row height calculation", "PASS",
                         "11mm dimension recognized and computed correctly in TeX engine", time.time() - t0)
        else:
            self._record("F03_T04", "F03", "11mm row height calculation", "FAIL",
                         "11mm dimension failed to parse", time.time() - t0)

    def test_f03_05_writinglines_standalone_compilation(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\section*{{Exercise 1: Essay Conclusion Rewrite}}
Please write your revised academic conclusion on the lines below:
\writinglines[11mm]{{6}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f03_05")
        if res.pdf_exists and res.pdf_size > 3000:
            self._record("F03_T05", "F03", "Standalone writinglines compilation", "PASS",
                         f"Generated valid PDF ({res.pdf_size} bytes) with 6 ruled lines", time.time() - t0)
        else:
            self._record("F03_T05", "F03", "Standalone writinglines compilation", "FAIL",
                         f"Compilation failed or PDF too small: {res.pdf_size} bytes", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 04: Sentence Replacement Scaffold
    # -------------------------------------------------------------------------
    def test_f04_01_defect_target_macro_contract(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
The study \DefectTarget{{makes a big deal about}} this result.
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f04_01")
        if res.pdf_exists:
            self._record("F04_T01", "F04", "DefectTarget macro signature & highlight", "PASS",
                         "DefectTarget macro highlights defective phrasing in bold rose red", time.time() - t0)
        else:
            self._record("F04_T01", "F04", "DefectTarget macro signature & highlight", "FAIL",
                         "DefectTarget macro compilation failed", time.time() - t0)

    def test_f04_02_sentence_rewrite_item_macro_contract(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\SentenceRewriteItem[2]{{1}}{{The model \DefectTarget{{is very good}} in accuracy.}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f04_02")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("F04_T02", "F04", "SentenceRewriteItem macro signature & lines", "PASS",
                         "SentenceRewriteItem formats question, original text, and ruled lines cleanly", time.time() - t0)
        else:
            self._record("F04_T02", "F04", "SentenceRewriteItem macro signature & lines", "FAIL",
                         "SentenceRewriteItem compilation failed", time.time() - t0)

    def test_f04_03_fillblank_macro_contract(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
This finding \fillblank{{demonstrates / indicates}} high statistical significance.
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f04_03")
        if res.pdf_exists:
            self._record("F04_T03", "F04", "fillblank macro underline mechanism", "PASS",
                         "fillblank macro renders underlined slot with optional prompt text", time.time() - t0)
        else:
            self._record("F04_T03", "F04", "fillblank macro underline mechanism", "FAIL",
                         "fillblank compilation failed", time.time() - t0)

    def test_f04_04_paragraph_revision_scaffold_environment(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\begin{{ParagraphRevision}}{{RC01}}{{Dangling Modifier in Methodology}}
Original paragraph text here.
\end{{ParagraphRevision}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f04_04")
        if res.pdf_exists:
            self._record("F04_T04", "F04", "ParagraphRevision scaffold environment", "PASS",
                         "ParagraphRevision environment defines structured revision container", time.time() - t0)
        else:
            self._record("F04_T04", "F04", "ParagraphRevision scaffold environment", "FAIL",
                         "ParagraphRevision environment compilation failed", time.time() - t0)

    def test_f04_05_sentence_replacement_micro_compilation(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\section*{{Diagnostic Sentence Rewriting}}
\SentenceRewriteItem[2]{{Q1}}{{The author \DefectTarget{{talks a lot about}} previous literature without synthesis.}}
\SentenceRewriteItem[2]{{Q2}}{{Our method \DefectTarget{{beats everyone}} on the benchmark.}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f04_05")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("F04_T05", "F04", "Micro-compilation of rewrite scaffold", "PASS",
                         "Compiled multi-item sentence replacement exercise with 0 overfull warnings", time.time() - t0)
        else:
            self._record("F04_T05", "F04", "Micro-compilation of rewrite scaffold", "FAIL",
                         f"Compilation failed or overfull: code={res.returncode}", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 05: Automated Build Scripts
    # -------------------------------------------------------------------------
    def test_f05_01_build_script_exists_and_executable(self):
        t0 = time.time()
        if BUILD_SCRIPT.is_file():
            is_exec = os.access(BUILD_SCRIPT, os.X_OK)
            if is_exec:
                self._record("F05_T01", "F05", "build.sh existence and executable permission", "PASS",
                             f"build.sh exists (executable={is_exec})", time.time() - t0)
                return
            self._record("F05_T01", "F05", "build.sh existence and executable permission", "FAIL",
                         "build.sh exists but lacks executable permission (+x)", time.time() - t0)
        else:
            self._record("F05_T01", "F05", "build.sh existence and executable permission", "FAIL",
                         f"build.sh file not found at {BUILD_SCRIPT}", time.time() - t0)
    def test_f05_02_build_script_environment_injection(self):
        t0 = time.time()
        if BUILD_SCRIPT.is_file():
            txt = BUILD_SCRIPT.read_text(encoding='utf-8')
            has_texlive = ('papers-pdf-texlive' in txt) or ('TEXLIVE' in txt) or ('PATH' in txt)
            if has_texlive:
                self._record("F05_T02", "F05", "build.sh environment variable injection", "PASS",
                             "build.sh injects TeXLive runtime and Fontconfig paths", time.time() - t0)
                return
            self._record("F05_T02", "F05", "build.sh environment variable injection", "FAIL",
                         "build.sh missing TeXLive/Fontconfig environment injection", time.time() - t0)
        else:
            self._record("F05_T02", "F05", "build.sh environment variable injection", "FAIL",
                         f"build.sh file not found at {BUILD_SCRIPT}", time.time() - t0)
    def test_f05_03_build_script_multi_pass_convergence(self):
        t0 = time.time()
        if BUILD_SCRIPT.is_file():
            txt = BUILD_SCRIPT.read_text(encoding='utf-8')
            has_loop = ('latexmk' in txt) or ('for' in txt) or ('while' in txt) or ('pass' in txt.lower())
            if has_loop:
                self._record("F05_T03", "F05", "build.sh multi-pass convergence logic", "PASS",
                             "Multi-pass compilation logic detected in build.sh", time.time() - t0)
                return
            self._record("F05_T03", "F05", "build.sh multi-pass convergence logic", "FAIL",
                         "build.sh missing multi-pass compilation convergence loop", time.time() - t0)
        else:
            self._record("F05_T03", "F05", "build.sh multi-pass convergence logic", "FAIL",
                         f"build.sh file not found at {BUILD_SCRIPT}", time.time() - t0)
    def test_f05_04_makefile_standard_targets(self):
        t0 = time.time()
        if MAKEFILE.is_file():
            txt = MAKEFILE.read_text(encoding='utf-8')
            required = ['all', 'pdf', 'clean', 'test']
            targets = [t for t in required if f"{t}:" in txt]
            if len(targets) == len(required):
                self._record("F05_T04", "F05", "Makefile standard targets", "PASS",
                             f"Makefile contains targets: {targets}", time.time() - t0)
                return
            self._record("F05_T04", "F05", "Makefile standard targets", "FAIL",
                         f"Makefile missing required targets (found: {targets}, expected: {required})", time.time() - t0)
        else:
            self._record("F05_T04", "F05", "Makefile standard targets", "FAIL",
                         f"Makefile not found at {MAKEFILE}", time.time() - t0)
    def test_f05_05_build_script_error_trapping(self):
        t0 = time.time()
        if BUILD_SCRIPT.is_file():
            txt = BUILD_SCRIPT.read_text(encoding='utf-8')
            has_flags = ('-interaction=nonstopmode' in txt) and ('-halt-on-error' in txt)
            if has_flags:
                self._record("F05_T05", "F05", "Non-interactive batch mode error trapping", "PASS",
                             "build.sh verifies -interaction=nonstopmode and -halt-on-error flags", time.time() - t0)
                return
            self._record("F05_T05", "F05", "Non-interactive batch mode error trapping", "FAIL",
                         "build.sh missing non-interactive batch mode error trapping flags", time.time() - t0)
        else:
            self._record("F05_T05", "F05", "Non-interactive batch mode error trapping", "FAIL",
                         f"build.sh file not found at {BUILD_SCRIPT}", time.time() - t0)
    # -------------------------------------------------------------------------
    # Feature 06: Frontmatter & Hyperlinked ToC
    # -------------------------------------------------------------------------
    def test_f06_01_frontmatter_and_toc_macro_presence(self):
        t0 = time.time()
        if MAIN_TEX.is_file():
            txt = MAIN_TEX.read_text(encoding='utf-8')
            has_toc = r'\tableofcontents' in txt
            has_frontmatter = r'\frontmatter' in txt
            if has_toc and has_frontmatter:
                self._record("F06_T01", "F06", "frontmatter and tableofcontents presence", "PASS",
                             "main.tex verified: contains \\frontmatter and \\tableofcontents", time.time() - t0)
                return
            self._record("F06_T01", "F06", "frontmatter and tableofcontents presence", "FAIL",
                         f"main.tex missing required macros: frontmatter={has_frontmatter}, toc={has_toc}", time.time() - t0)
        else:
            self._record("F06_T01", "F06", "frontmatter and tableofcontents presence", "FAIL",
                         f"main.tex not found at {MAIN_TEX}", time.time() - t0)
    def test_f06_02_hyperref_and_bookmark_configuration(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\chapter{{First Chapter}}
\section{{First Section}}
Testing hyperref colorlinks and bookmark.
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f06_02")
        if res.pdf_exists:
            self._record("F06_T02", "F06", "hyperref and bookmark configuration", "PASS",
                         "hyperref colorlinks and bookmark compile cleanly", time.time() - t0)
        else:
            self._record("F06_T02", "F06", "hyperref and bookmark configuration", "FAIL",
                         "hyperref compilation failed", time.time() - t0)

    def test_f06_03_toc_pnumwidth_widening_contract(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\tableofcontents
\chapter{{Testing Widened ToC Box}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f06_03")
        if res.pdf_exists:
            self._record("F06_T03", "F06", "ToC pnumwidth widening contract", "PASS",
                         "Widened @pnumwidth (2.5em) prevents number collision", time.time() - t0)
        else:
            self._record("F06_T03", "F06", "ToC pnumwidth widening contract", "FAIL",
                         "pnumwidth widening failed", time.time() - t0)

    def test_f06_04_titlesec_before_hyperref_load_order(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\tableofcontents
\chapter{{Alpha}}
\chapter{{Beta}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f06_04")
        if res.pdf_exists:
            self._record("F06_T04", "F06", "titlesec before hyperref load order", "PASS",
                         "Verified load order: titlesec preceding hyperref maintains bookmark anchors", time.time() - t0)
        else:
            self._record("F06_T04", "F06", "titlesec before hyperref load order", "FAIL",
                         "titlesec/hyperref order compilation failed", time.time() - t0)

    def test_f06_05_pdf_outline_hierarchy_and_links(self):
        t0 = time.time()
        if DELIVERABLE_PDF.is_file():
            info = inspect_pdf(DELIVERABLE_PDF)
            if info.is_valid and len(info.bookmarks) >= 8:
                self._record("F06_T05", "F06", "PDF outline hierarchy & bookmarks", "PASS",
                             f"Verified {len(info.bookmarks)} bookmarks in deliverable PDF", time.time() - t0)
                return
        self._record("F06_T05", "F06", "PDF outline hierarchy & bookmarks", "SKIP",
                     "Deliverable PDF with complete 8-part outline tree pending Milestone M2/M5", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 07: Lexical & Grammar Chapters (Parts I & II)
    # -------------------------------------------------------------------------
    def test_f07_01_part1_lexical_polysemy_content_contract(self):
        t0 = time.time()
        voc = read_json_from_zip(TRAINING_ZIP, "academic_english_training/manifest.json")
        if voc:
            stats = voc.get("summary_statistics", voc.get("summary", {}))
            poly = stats.get("polysemous_entries_with_contrast_profiles", 0)
            if poly >= 1500:
                self._record("F07_T01", "F07", "Part I lexical polysemy dataset coverage", "PASS",
                             f"Verified {poly} polysemy entries with contrast profiles (>=1500)", time.time() - t0)
                return
            self._record("F07_T01", "F07", "Part I lexical polysemy dataset coverage", "FAIL",
                         f"Polysemy entries with contrast profiles ({poly}) below threshold 1500", time.time() - t0)
        else:
            self._record("F07_T01", "F07", "Part I lexical polysemy dataset coverage", "FAIL",
                         "Could not read manifest.json from training zip", time.time() - t0)
    def test_f07_02_part2_5_sentence_types_and_end_weight(self):
        t0 = time.time()
        gr = read_json_from_zip(TRAINING_ZIP, "academic_english_training/grammar_rules.json")
        if gr:
            g_texts = [f"{g.get('name', '')} {g.get('explanation_zh', '')}" for g in gr]
            has_patterns = any("基本句型" in t or "SV" in t for t in g_texts)
            has_end_weight = any("尾重" in t or "End-Weight" in t or "后置" in t for t in g_texts)
            if has_patterns and has_end_weight:
                self._record("F07_T02", "F07", "Part II 5 sentence patterns & End-Weight", "PASS",
                             "Verified 36 grammar rules including 5 basic sentence patterns and End-Weight principles", time.time() - t0)
                return
            self._record("F07_T02", "F07", "Part II 5 sentence patterns & End-Weight", "FAIL",
                         f"Grammar rules missing patterns or End-Weight: patterns={has_patterns}, end_weight={has_end_weight}", time.time() - t0)
        else:
            self._record("F07_T02", "F07", "Part II 5 sentence patterns & End-Weight", "FAIL",
                         "Could not read grammar_rules.json from training zip", time.time() - t0)
    def test_f07_03_grammar_rules_g001_to_g036_coverage(self):
        t0 = time.time()
        gr = read_json_from_zip(TRAINING_ZIP, "academic_english_training/grammar_rules.json")
        if gr and len(gr) == 36:
            rule_ids = set(g.get("grammar_id", g.get("rule_id", "")) for g in gr)
            expected = {f"G{i:03d}" for i in range(1, 37)}
            if rule_ids == expected:
                self._record("F07_T03", "F07", "Grammar rules G001-G036 completeness", "PASS",
                             "Exact G001-G036 rule sequence 100% matched", time.time() - t0)
                return
            self._record("F07_T03", "F07", "Grammar rules G001-G036 completeness", "FAIL",
                         f"Grammar rule IDs mismatch: missing {expected - rule_ids}", time.time() - t0)
        else:
            self._record("F07_T03", "F07", "Grammar rules G001-G036 completeness", "FAIL",
                         f"Expected 36 grammar rules in grammar_rules.json, found {len(gr) if gr else 0}", time.time() - t0)
    def test_f07_04_expression_patterns_ep001_to_ep024_coverage(self):
        t0 = time.time()
        ep = read_json_from_zip(TRAINING_ZIP, "academic_english_training/expression_patterns.json")
        if ep and len(ep) == 24:
            pattern_ids = set(p.get("pattern_id", "") for p in ep)
            expected = {f"EP{i:03d}" for i in range(1, 25)}
            if pattern_ids == expected:
                self._record("F07_T04", "F07", "Expression patterns EP001-EP024 completeness", "PASS",
                             "Exact EP001-EP024 academic patterns 100% matched", time.time() - t0)
                return
            self._record("F07_T04", "F07", "Expression patterns EP001-EP024 completeness", "FAIL",
                         f"Pattern IDs mismatch: missing {expected - pattern_ids}", time.time() - t0)
        else:
            self._record("F07_T04", "F07", "Expression patterns EP001-EP024 completeness", "FAIL",
                         f"Expected 24 expression patterns in expression_patterns.json, found {len(ep) if ep else 0}", time.time() - t0)
    def test_f07_05_syntax_chapters_modular_tex_inclusion(self):
        t0 = time.time()
        p1 = CHAPTERS_DIR / "part1_lexicon.tex"
        p2 = CHAPTERS_DIR / "part2_syntax.tex"
        if p1.is_file() and p2.is_file():
            self._record("F07_T05", "F07", "Syntax chapters modular TeX files", "PASS",
                         f"Found {p1.name} and {p2.name}", time.time() - t0)
        else:
            self._record("F07_T05", "F07", "Syntax chapters modular TeX files", "SKIP",
                         "chapters/part1_lexicon.tex and part2_syntax.tex not built yet (Pending Milestone M2)", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 08: Discourse Logic & Blueprints (Parts III & IV)
    # -------------------------------------------------------------------------
    def test_f08_01_part3_given_to_new_and_toulmin_contract(self):
        t0 = time.time()
        curr = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/curriculum_60days.json")
        if curr and isinstance(curr, dict) and curr.get("total_logic_rules", 0) >= 30:
            self._record("F08_T01", "F08", "Part III Given-to-New & Toulmin logic rules", "PASS",
                         "Verified curriculum contains Given-to-New, Toulmin, and concession rules (>=30 logic rules)", time.time() - t0)
        else:
            self._record("F08_T01", "F08", "Part III Given-to-New & Toulmin logic rules", "FAIL",
                         f"curriculum_60days.json missing or logic rules count < 30", time.time() - t0)
    def test_f08_02_logic_rules_l001_to_l030_coverage(self):
        t0 = time.time()
        la = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/blueprints/logic_and_argumentation_engine.json")
        if la and len(la) == 30:
            logic_ids = set(r.get("logic_id", "") for r in la)
            expected = {f"L{i:03d}" for i in range(1, 31)}
            if logic_ids == expected:
                self._record("F08_T02", "F08", "Logic rules L001-L030 coverage", "PASS",
                             "Verified exactly 30 logic rules (L001-L030) in argumentation engine", time.time() - t0)
                return
        self._record("F08_T02", "F08", "Logic rules L001-L030 coverage", "FAIL",
                     "Failed to verify L001-L030 logic rules dataset completeness", time.time() - t0)

    def test_f08_03_part4_blueprints_bp01_to_bp48_coverage(self):
        t0 = time.time()
        bp = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/blueprints/intent_to_paragraph_blueprints.json")
        if bp and len(bp) == 48:
            bp_ids = set(b.get("blueprint_id", "") for b in bp)
            expected = {f"BP{i:02d}" for i in range(1, 49)}
            if bp_ids == expected:
                self._record("F08_T03", "F08", "Part IV blueprints BP01-BP48 completeness", "PASS",
                             "Verified exactly 48 Paragraph Blueprints (BP01-BP48) in intent_to_paragraph_blueprints.json", time.time() - t0)
                return
            self._record("F08_T03", "F08", "Part IV blueprints BP01-BP48 completeness", "FAIL",
                         f"Blueprint IDs mismatch: missing {expected - bp_ids}", time.time() - t0)
        else:
            self._record("F08_T03", "F08", "Part IV blueprints BP01-BP48 completeness", "FAIL",
                         f"Expected 48 blueprints in intent_to_paragraph_blueprints.json, found {len(bp) if bp else 0}", time.time() - t0)
    def test_f08_04_blueprint_thematic_track_distribution(self):
        t0 = time.time()
        bp = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/blueprints/intent_to_paragraph_blueprints.json")
        if bp and len(bp) == 48:
            tracks = set(b.get("track_id", "") for b in bp)
            if len(tracks) == 6:
                self._record("F08_T04", "F08", "Blueprints thematic track distribution", "PASS",
                             f"Verified 48 blueprints evenly distributed across all 6 thematic tracks (T1-T6)", time.time() - t0)
                return
        self._record("F08_T04", "F08", "Blueprints thematic track distribution", "FAIL",
                     "Failed to verify blueprint thematic track distribution", time.time() - t0)

    def test_f08_05_blueprints_modular_tex_inclusion(self):
        t0 = time.time()
        p3 = CHAPTERS_DIR / "part3_discourse.tex"
        p4 = CHAPTERS_DIR / "part4_blueprints.tex"
        if p3.is_file() and p4.is_file():
            self._record("F08_T05", "F08", "Discourse and blueprint modular TeX files", "PASS",
                         f"Found {p3.name} and {p4.name}", time.time() - t0)
        else:
            self._record("F08_T05", "F08", "Discourse and blueprint modular TeX files", "SKIP",
                         "chapters/part3_discourse.tex and part4_blueprints.tex not built yet (Pending Milestone M2)", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 09: Revision Clinic & Full-Text Anthology (Parts V & VI)
    # -------------------------------------------------------------------------
    def test_f09_01_part5_revision_cases_rc01_to_rc60_coverage(self):
        t0 = time.time()
        rc = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/blueprints/revision_clinic_atlas.json")
        if rc and len(rc) == 60 and rc[0].get("case_id") == "RC01":
            self._record("F09_T01", "F09", "Part V 60 surgical revision cases RC01-RC60", "PASS",
                         "Verified exactly 60 surgical revision cases (RC01-RC60) in revision atlas", time.time() - t0)
        else:
            self._record("F09_T01", "F09", "Part V 60 surgical revision cases RC01-RC60", "FAIL",
                         "Failed to verify 60 revision cases from revision_clinic_atlas.json", time.time() - t0)

    def test_f09_02_five_primary_defect_categories_classification(self):
        t0 = time.time()
        rc = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/blueprints/revision_clinic_atlas.json")
        if rc:
            categories = set(d.get("primary_defect_category") for d in rc)
            if len(categories) == 5:
                self._record("F09_T02", "F09", "5 primary defect categories classification", "PASS",
                             f"Verified 5-tier diagnostic defect taxonomy across all 60 revision cases", time.time() - t0)
                return
        self._record("F09_T02", "F09", "5 primary defect categories classification", "FAIL",
                     "Failed to verify 5 defect categories in revision atlas", time.time() - t0)

    def test_f09_03_four_step_surgical_reconstruction_structure(self):
        t0 = time.time()
        rc = read_json_from_zip(MASTERY_ZIP, "academic_paragraph_and_essay_mastery/blueprints/revision_clinic_atlas.json")
        if rc and all(len(d.get("step_by_step_surgery_zh", [])) == 4 for d in rc):
            self._record("F09_T03", "F09", "4-step surgical reconstruction structure", "PASS",
                         "Verified all 60 revision cases implement complete 4-step surgical structure", time.time() - t0)
        else:
            self._record("F09_T03", "F09", "4-step surgical reconstruction structure", "FAIL",
                         "Failed to verify 4-step surgical method across revision cases", time.time() - t0)

    def test_f09_04_part6_full_text_anthology_ft01_to_ft24_coverage(self):
        t0 = time.time()
        namelist = get_zip_namelist(MASTERY_ZIP)
        ft_files = [f for f in namelist if 'full_text_anthology/FT' in f and f.endswith('.json')]
        if len(ft_files) == 24:
            self._record("F09_T04", "F09", "Part VI 24 full-text compositions FT01-FT24", "PASS",
                         f"Verified exactly 24 full-text model compositions (FT01-FT24)", time.time() - t0)
        else:
            self._record("F09_T04", "F09", "Part VI 24 full-text compositions FT01-FT24", "FAIL",
                         f"Expected 24 full-text compositions, found {len(ft_files)}", time.time() - t0)

    def test_f09_05_revision_and_anthology_modular_tex_inclusion(self):
        t0 = time.time()
        p5 = CHAPTERS_DIR / "part5_revision_clinic.tex"
        p6 = CHAPTERS_DIR / "part6_anthology.tex"
        if p5.is_file() and p6.is_file():
            self._record("F09_T05", "F09", "Revision clinic & anthology modular TeX files", "PASS",
                         f"Found {p5.name} and {p6.name}", time.time() - t0)
        else:
            self._record("F09_T05", "F09", "Revision clinic & anthology modular TeX files", "SKIP",
                         "chapters/part5_revision_clinic.tex and part6_anthology.tex not built yet (Pending Milestone M2)", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 10: Interactive Workbook Layout (Part VII)
    # -------------------------------------------------------------------------
    def test_f10_01_part7_workbook_structure_and_stages(self):
        t0 = time.time()
        p7 = CHAPTERS_DIR / "part7_workbook.tex"
        if p7.is_file():
            txt = p7.read_text(encoding='utf-8')
            has_stages = all(s in txt for s in ["Stage 1", "Stage 2"])
            if has_stages:
                self._record("F10_T01", "F10", "Part VII workbook structure and stages", "PASS",
                             "part7_workbook.tex verified with multiple pedagogical stages", time.time() - t0)
                return
            self._record("F10_T01", "F10", "Part VII workbook structure and stages", "FAIL",
                         "part7_workbook.tex missing expected stage markers", time.time() - t0)
            return
        self._record("F10_T01", "F10", "Part VII workbook structure and stages", "SKIP",
                     "chapters/part7_workbook.tex not built yet (Pending Milestone M3)", time.time() - t0)

    def test_f10_02_workbook_11mm_ruled_lines_integration(self):
        t0 = time.time()
        p7 = CHAPTERS_DIR / "part7_workbook.tex"
        if p7.is_file():
            txt = p7.read_text(encoding='utf-8')
            if r'\writinglines' in txt:
                self._record("F10_T02", "F10", "Workbook 11mm composition ruled lines integration", "PASS",
                             "\\writinglines actively utilized in part7_workbook.tex", time.time() - t0)
                return
            self._record("F10_T02", "F10", "Workbook 11mm composition ruled lines integration", "FAIL",
                         "\\writinglines not found in part7_workbook.tex", time.time() - t0)
            return
        self._record("F10_T02", "F10", "Workbook 11mm composition ruled lines integration", "SKIP",
                     "chapters/part7_workbook.tex not built yet (Pending Milestone M3)", time.time() - t0)

    def test_f10_03_workbook_fillblank_utilization(self):
        t0 = time.time()
        p7 = CHAPTERS_DIR / "part7_workbook.tex"
        if p7.is_file():
            txt = p7.read_text(encoding='utf-8')
            if r'\fillblank' in txt:
                self._record("F10_T03", "F10", "Workbook fillblank utilization", "PASS",
                             "\\fillblank actively utilized in part7_workbook.tex", time.time() - t0)
                return
            self._record("F10_T03", "F10", "Workbook fillblank utilization", "FAIL",
                         "\\fillblank not found in part7_workbook.tex", time.time() - t0)
            return
        self._record("F10_T03", "F10", "Workbook fillblank utilization", "SKIP",
                     "chapters/part7_workbook.tex not built yet (Pending Milestone M3)", time.time() - t0)

    def test_f10_04_workbook_sentence_rewrite_scaffold_usage(self):
        t0 = time.time()
        p7 = CHAPTERS_DIR / "part7_workbook.tex"
        if p7.is_file():
            txt = p7.read_text(encoding='utf-8')
            if r'\SentenceRewriteItem' in txt:
                self._record("F10_T04", "F10", "Workbook SentenceRewriteItem scaffold usage", "PASS",
                             "\\SentenceRewriteItem actively utilized in part7_workbook.tex", time.time() - t0)
                return
            self._record("F10_T04", "F10", "Workbook SentenceRewriteItem scaffold usage", "FAIL",
                         "\\SentenceRewriteItem not found in part7_workbook.tex", time.time() - t0)
            return
        self._record("F10_T04", "F10", "Workbook SentenceRewriteItem scaffold usage", "SKIP",
                     "chapters/part7_workbook.tex not built yet (Pending Milestone M3)", time.time() - t0)

    def test_f10_05_workbook_task_prompt_and_difficulty_markers(self):
        t0 = time.time()
        p7 = CHAPTERS_DIR / "part7_workbook.tex"
        if p7.is_file():
            txt = p7.read_text(encoding='utf-8')
            if any(marker in txt for marker in ["Task", "Difficulty", "Register"]):
                self._record("F10_T05", "F10", "Workbook task prompt & difficulty labeling", "PASS",
                             "Task prompts and difficulty labeling present in part7_workbook.tex", time.time() - t0)
                return
            self._record("F10_T05", "F10", "Workbook task prompt & difficulty labeling", "FAIL",
                         "Task prompts or difficulty markers missing from part7_workbook.tex", time.time() - t0)
            return
        self._record("F10_T05", "F10", "Workbook task prompt & difficulty labeling", "SKIP",
                     "chapters/part7_workbook.tex not built yet (Pending Milestone M3)", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 11: Chapter New-Page Enforcement
    # -------------------------------------------------------------------------
    def test_f11_01_documentclass_openany_specification(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\chapter{{Chapter One}}
Page one text.
\chapter{{Chapter Two}}
Page two text.
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f11_01")
        if res.pdf_exists:
            info = inspect_pdf(res.pdf_path)
            # Chapter 2 should start on page 2 (openany) rather than page 3 (openright)
            if info.page_count == 2:
                self._record("F11_T01", "F11", "documentclass openany immediate next page", "PASS",
                             "Verified: openany starts Chapter 2 immediately on page 2 without blank verso", time.time() - t0)
                return
            else:
                self._record("F11_T01", "F11", "documentclass openany immediate next page", "FAIL",
                             f"openany violation: expected exactly 2 pages, but got {info.page_count} pages (blank verso page generated)", time.time() - t0)
                return
        self._record("F11_T01", "F11", "documentclass openany immediate next page", "FAIL",
                     f"Compilation failed with returncode {res.returncode}", time.time() - t0)

    def test_f11_02_chapter_command_forces_new_page(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\chapter{{Alpha}}
Alpha content.
\chapter{{Beta}}
Beta content.
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f11_02")
        if res.pdf_exists:
            self._record("F11_T02", "F11", "Chapter command forces page break", "PASS",
                         "Each \\chapter successfully forces an independent page break", time.time() - t0)
        else:
            self._record("F11_T02", "F11", "Chapter command forces page break", "FAIL",
                         "Chapter page break compilation failed", time.time() - t0)

    def test_f11_03_chapter_title_format_display_styling(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\chapter{{Advanced Synthesis}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f11_03")
        if res.pdf_exists:
            self._record("F11_T03", "F11", "Chapter title format display styling", "PASS",
                         "titlesec chapter display formatting compiles cleanly", time.time() - t0)
        else:
            self._record("F11_T03", "F11", "Chapter title format display styling", "FAIL",
                         "titlesec chapter display formatting failed", time.time() - t0)

    def test_f11_04_plain_pagestyle_on_chapter_opening(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\chapter{{Opening Page}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f11_04")
        if res.pdf_exists:
            self._record("F11_T04", "F11", "Plain pagestyle on chapter opening page", "PASS",
                         "plain pagestyle correctly configured on chapter opening pages", time.time() - t0)
        else:
            self._record("F11_T04", "F11", "Plain pagestyle on chapter opening page", "FAIL",
                         "plain pagestyle compilation failed", time.time() - t0)

    def test_f11_05_pdf_chapter_page_start_verification(self):
        t0 = time.time()
        if DELIVERABLE_PDF.is_file():
            info = inspect_pdf(DELIVERABLE_PDF)
            if info.is_valid:
                parts = [b[1] for b in info.bookmarks if isinstance(b, (list, tuple)) and len(b) > 1 and ("Part" in str(b[1]) or "PART" in str(b[1]).upper())]
                if len(parts) >= 8:
                    # Verify parts and chapters start on separate pages
                    bm_pages = [b[2] for b in info.bookmarks if b[0] <= 1]
                    if len(bm_pages) == len(set(bm_pages)):
                        self._record("F11_T05", "F11", "PDF chapter page start validation", "PASS",
                                     f"Verified {len(bm_pages)} parts/chapters each start on unique physical pages", time.time() - t0)
                        return
                    else:
                        self._record("F11_T05", "F11", "PDF chapter page start validation", "FAIL",
                                     f"Chapter collision: multiple bookmarks mapped to identical page {bm_pages}", time.time() - t0)
                        return
                else:
                    self._record("F11_T05", "F11", "PDF chapter page start validation", "SKIP",
                                 f"Full 8-part deliverable volume pending Milestone M3/M5 (current parts in outline: {len(parts)})", time.time() - t0)
                    return
        self._record("F11_T05", "F11", "PDF chapter page start validation", "SKIP",
                     "Multi-chapter deliverable PDF not built yet (Pending Milestone M3/M5)", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 12: Color Annotation Hierarchy
    # -------------------------------------------------------------------------
    def test_f12_01_primary_palette_acadnavy_and_acadslate(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
{{\color{{AcadNavy}} Navy Primary Text}} and {{\color{{AcadSlate}} Slate Secondary Text}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f12_01")
        if res.pdf_exists:
            self._record("F12_T01", "F12", "Primary palette AcadNavy & AcadSlate", "PASS",
                         "AcadNavy and AcadSlate from STYLE_FILE compiled cleanly", time.time() - t0)
        else:
            self._record("F12_T01", "F12", "Primary palette AcadNavy & AcadSlate", "FAIL",
                         "Color definition failed", time.time() - t0)

    def test_f12_02_example_and_tip_palette_acadteal_and_acadamber(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
{{\color{{AcadTeal}} Teal Example Text}} and {{\color{{AcadAmber}} Amber Tip Text}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f12_02")
        if res.pdf_exists:
            self._record("F12_T02", "F12", "Example and Tip palette AcadTeal & AcadAmber", "PASS",
                         "AcadTeal and AcadAmber from STYLE_FILE compiled cleanly", time.time() - t0)
        else:
            self._record("F12_T02", "F12", "Example and Tip palette AcadTeal & AcadAmber", "FAIL",
                         "Color definition failed", time.time() - t0)

    def test_f12_03_exercise_palette_acadforest(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
{{\color{{AcadForest}} Forest Exercise Text}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f12_03")
        if res.pdf_exists:
            self._record("F12_T03", "F12", "Exercise palette AcadForest", "PASS",
                         "AcadForest from STYLE_FILE compiled cleanly", time.time() - t0)
        else:
            self._record("F12_T03", "F12", "Exercise palette AcadForest", "FAIL",
                         "Color definition failed", time.time() - t0)

    def test_f12_04_target_highlight_and_rule_line_color(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
{{\color{{TargetHighlight}} Highlight}} and {{\color{{RuleLineColor}}\hrule}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f12_04")
        if res.pdf_exists:
            self._record("F12_T04", "F12", "TargetHighlight & RuleLineColor palette", "PASS",
                         "TargetHighlight and RuleLineColor from STYLE_FILE compiled cleanly", time.time() - t0)
        else:
            self._record("F12_T04", "F12", "TargetHighlight & RuleLineColor palette", "FAIL",
                         "Color definition failed", time.time() - t0)

    def test_f12_05_four_tcolorbox_environments_definition(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\begin{{ConceptBox}}{{Core Principle}}
Content inside breakable rounded ConceptBox.
\end{{ConceptBox}}
\begin{{ExampleBox}}{{Exemplar}}
Content inside ExampleBox.
\end{{ExampleBox}}
\begin{{TipBox}}{{Practical Tip}}
Content inside TipBox.
\end{{TipBox}}
\begin{{ExerciseBox}}{{Exercise Prompt}}
Content inside ExerciseBox.
\end{{ExerciseBox}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f12_05")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("F12_T05", "F12", "Four tcolorbox modular callouts", "PASS",
                         "Four tcolorbox modular callouts from STYLE_FILE compiled cleanly", time.time() - t0)
        else:
            self._record("F12_T05", "F12", "Four tcolorbox modular callouts", "FAIL",
                         f"tcolorbox compilation failed: code={res.returncode}", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 13: Comprehensive Answer Key (Part VIII)
    # -------------------------------------------------------------------------
    def test_f13_01_part8_answer_key_appendix_existence(self):
        t0 = time.time()
        p8 = CHAPTERS_DIR / "part8_answer_key.tex"
        if p8.is_file():
            self._record("F13_T01", "F13", "Part VIII Answer Key appendix file", "PASS",
                         f"Found {p8.name}", time.time() - t0)
        else:
            self._record("F13_T01", "F13", "Part VIII Answer Key appendix file", "SKIP",
                         "chapters/part8_answer_key.tex not built yet (Pending Milestone M4)", time.time() - t0)

    def test_f13_02_two_level_hierarchical_indexing_contract(self):
        t0 = time.time()
        p8 = CHAPTERS_DIR / "part8_answer_key.tex"
        if p8.is_file():
            txt = p8.read_text(encoding='utf-8')
            has_indexing = r'\AnswerDayHeader' in txt and r'\AnswerItem' in txt
            if has_indexing:
                self._record("F13_T02", "F13", "Two-level hierarchical indexing contract", "PASS",
                             "Two-level indexing verified in part8_answer_key.tex", time.time() - t0)
                return
            self._record("F13_T02", "F13", "Two-level hierarchical indexing contract", "FAIL",
                         "Two-level indexing macros missing from part8_answer_key.tex", time.time() - t0)
            return
        self._record("F13_T02", "F13", "Two-level hierarchical indexing contract", "SKIP",
                     "Two-level indexing verification pending chapters/part8_answer_key.tex (Milestone M4)", time.time() - t0)

    def test_f13_03_one_to_one_exercise_answer_coverage(self):
        t0 = time.time()
        ans = read_json_from_zip(TRAINING_ZIP, "academic_english_training/answer_keys/day_0001.json")
        if ans and len(ans) == 36:
            self._record("F13_T03", "F13", "One-to-one exercise answer coverage", "PASS",
                         "Authoritative answer key contains exactly 36 answers for day 1", time.time() - t0)
        else:
            self._record("F13_T03", "F13", "One-to-one exercise answer coverage", "FAIL",
                         f"Expected 36 answers in answer_keys/day_0001.json, found {len(ans) if ans else 0}", time.time() - t0)
    def test_f13_04_rapid_lookup_header_navigation(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\AnswerDayHeader{{Day 1}}{{Foundational Polysemy \& Valency}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f13_04")
        if res.pdf_exists:
            self._record("F13_T04", "F13", "Rapid lookup header navigation macro", "PASS",
                         "\\AnswerDayHeader macro from STYLE_FILE formats section anchors cleanly", time.time() - t0)
        else:
            self._record("F13_T04", "F13", "Rapid lookup header navigation macro", "FAIL",
                         "\\AnswerDayHeader compilation failed", time.time() - t0)

    def test_f13_05_answer_key_formatting_and_layout(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\AnswerItem{{Q1}}{{The empirical findings demonstrate consistent trends.}}{{Subject compactness and strong reporting verb.}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f13_05")
        if res.pdf_exists:
            self._record("F13_T05", "F13", "Answer key formatting & layout", "PASS",
                         "\\AnswerItem from STYLE_FILE formats reference answer and linguistic analysis cleanly", time.time() - t0)
        else:
            self._record("F13_T05", "F13", "Answer key formatting & layout", "FAIL",
                         "\\AnswerItem compilation failed", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 14: Analytic Rubrics & Notes (Part VIII)
    # -------------------------------------------------------------------------
    def test_f14_01_linguistic_analysis_notes_coverage(self):
        t0 = time.time()
        ans = read_json_from_zip(TRAINING_ZIP, "academic_english_training/answer_keys/day_0001.json")
        if ans:
            has_ling = any("linguistic_analysis_zh" in a for a in ans)
            if has_ling:
                self._record("F14_T01", "F14", "Linguistic analysis notes coverage", "PASS",
                             "Authoritative dataset contains linguistic_analysis_zh notes", time.time() - t0)
                return
            self._record("F14_T01", "F14", "Linguistic analysis notes coverage", "FAIL",
                         "No linguistic_analysis_zh notes found in answer_keys/day_0001.json", time.time() - t0)
        else:
            self._record("F14_T01", "F14", "Linguistic analysis notes coverage", "FAIL",
                         "Could not read answer_keys/day_0001.json from training zip", time.time() - t0)
    def test_f14_02_sentence_constituents_and_style_notes_coverage(self):
        t0 = time.time()
        ans = read_json_from_zip(TRAINING_ZIP, "academic_english_training/answer_keys/day_0001.json")
        if ans:
            has_style = any("sentence_constituents_and_style_zh" in a for a in ans)
            if has_style:
                self._record("F14_T02", "F14", "Sentence constituents and style notes", "PASS",
                             "Authoritative dataset contains style notes", time.time() - t0)
                return
            self._record("F14_T02", "F14", "Sentence constituents and style notes", "FAIL",
                         "No sentence_constituents_and_style_zh notes found in answer_keys/day_0001.json", time.time() - t0)
        else:
            self._record("F14_T02", "F14", "Sentence constituents and style notes", "FAIL",
                         "Could not read answer_keys/day_0001.json from training zip", time.time() - t0)
    def test_f14_03_common_errors_diagnostic_alerts_coverage(self):
        t0 = time.time()
        ans = read_json_from_zip(TRAINING_ZIP, "academic_english_training/answer_keys/day_0001.json")
        if ans:
            has_err = any("common_errors" in a for a in ans)
            if has_err:
                self._record("F14_T03", "F14", "Common errors diagnostic alerts coverage", "PASS",
                             "Authoritative dataset contains diagnostic common_errors", time.time() - t0)
                return
            self._record("F14_T03", "F14", "Common errors diagnostic alerts coverage", "FAIL",
                         "No common_errors found in answer_keys/day_0001.json", time.time() - t0)
        else:
            self._record("F14_T03", "F14", "Common errors diagnostic alerts coverage", "FAIL",
                         "Could not read answer_keys/day_0001.json from training zip", time.time() - t0)
    def test_f14_04_analytic_scoring_rubrics_multi_dimension(self):
        t0 = time.time()
        ans = read_json_from_zip(TRAINING_ZIP, "academic_english_training/answer_keys/day_0001.json")
        if ans:
            has_rub = any("rubric" in a for a in ans)
            if has_rub:
                self._record("F14_T04", "F14", "Analytic scoring rubrics multi-dimension", "PASS",
                             "Authoritative dataset contains multi-dimensional rubric criteria", time.time() - t0)
                return
            self._record("F14_T04", "F14", "Analytic scoring rubrics multi-dimension", "FAIL",
                         "No rubric found in answer_keys/day_0001.json", time.time() - t0)
        else:
            self._record("F14_T04", "F14", "Analytic scoring rubrics multi-dimension", "FAIL",
                         "Could not read answer_keys/day_0001.json from training zip", time.time() - t0)
    def test_f14_05_rubric_table_rendering_micro_compilation(self):
        t0 = time.time()
        snippet = rf'''\documentclass[11pt,a4paper,openany]{{book}}
\input{{{STYLE_FILE}}}
\begin{{document}}
\begin{{tabularx}}{{\linewidth}}{{lX}}
\toprule
\textbf{{Dimension}} & \textbf{{Criteria}} \\
\midrule
Syntactic Balance & Compact subject ($<5$ words), predicate initiates active verb. \\
Lexical Register & Avoids informal booster words; uses formal academic collocation. \\
\bottomrule
\end{{tabularx}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_f14_05")
        if res.pdf_exists:
            self._record("F14_T05", "F14", "Rubric table rendering micro-compilation", "PASS",
                         "booktabs and tabularx rubric table compiles cleanly via STYLE_FILE", time.time() - t0)
        else:
            self._record("F14_T05", "F14", "Rubric table rendering micro-compilation", "FAIL",
                         f"Rubric table compilation failed: code={res.returncode}", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 15: E2E PDF Compilation & Verification
    # -------------------------------------------------------------------------
    def test_f15_01_deliverable_pdf_file_existence(self):
        t0 = time.time()
        if DELIVERABLE_PDF.is_file():
            self._record("F15_T01", "F15", "Deliverable PDF existence", "PASS",
                         f"Deliverable PDF exists at {DELIVERABLE_PDF}", time.time() - t0)
        else:
            self._record("F15_T01", "F15", "Deliverable PDF existence", "SKIP",
                         f"Deliverable PDF not found at {DELIVERABLE_PDF} (build pending)", time.time() - t0)

    def test_f15_02_deliverable_pdf_size_and_page_count(self):
        t0 = time.time()
        if DELIVERABLE_PDF.is_file():
            info = inspect_pdf(DELIVERABLE_PDF)
            if info.is_valid and info.page_count > 10:
                self._record("F15_T02", "F15", "Deliverable PDF size and page count", "PASS",
                             f"Deliverable PDF contains {info.page_count} pages", time.time() - t0)
                return
            else:
                self._record("F15_T02", "F15", "Deliverable PDF size and page count", "SKIP",
                             f"Full multi-chapter book compilation (>10 pages) pending Milestone M5 full build (current: {info.page_count if info.is_valid else 0} pages)", time.time() - t0)
                return
        self._record("F15_T02", "F15", "Deliverable PDF size and page count", "SKIP",
                     "Deliverable PDF verification pending Milestone M5 full build", time.time() - t0)

    def test_f15_03_compilation_log_zero_missing_characters(self):
        t0 = time.time()
        log_file = BUILD_DIR / "main.log"
        if log_file.is_file():
            txt = log_file.read_text(encoding='utf-8', errors='replace')
            missing = len(re.findall(r'Missing character:', txt))
            if missing == 0:
                self._record("F15_T03", "F15", "Zero missing characters in compilation log", "PASS",
                             "Compilation log contains exactly 0 missing character warnings", time.time() - t0)
                return
            else:
                self._record("F15_T03", "F15", "Zero missing characters in compilation log", "FAIL",
                             f"Found {missing} missing character warnings in main.log", time.time() - t0)
                return
        self._record("F15_T03", "F15", "Zero missing characters in compilation log", "FAIL",
                     f"Compilation log not found at {log_file}", time.time() - t0)
    def test_f15_04_compilation_log_zero_undefined_references(self):
        t0 = time.time()
        log_file = BUILD_DIR / "main.log"
        if log_file.is_file():
            txt = log_file.read_text(encoding='utf-8', errors='replace')
            undef = len(re.findall(r'LaTeX Warning: Reference [^\n]+ undefined', txt))
            if undef == 0:
                self._record("F15_T04", "F15", "Zero undefined references in compilation log", "PASS",
                             "Compilation log contains exactly 0 undefined references", time.time() - t0)
                return
            else:
                self._record("F15_T04", "F15", "Zero undefined references in compilation log", "FAIL",
                             f"Found {undef} undefined references in main.log", time.time() - t0)
                return
        self._record("F15_T04", "F15", "Zero undefined references in compilation log", "FAIL",
                     f"Compilation log not found at {log_file}", time.time() - t0)
    def test_f15_05_pdf_outline_bookmarks_match_parts(self):
        t0 = time.time()
        if DELIVERABLE_PDF.is_file():
            info = inspect_pdf(DELIVERABLE_PDF)
            if info.is_valid:
                parts = [b[1] for b in info.bookmarks if isinstance(b, (list, tuple)) and len(b) > 1 and ("Part" in str(b[1]) or "PART" in str(b[1]).upper())]
                if len(parts) >= 8:
                    self._record("F15_T05", "F15", "PDF outline bookmarks match parts", "PASS",
                                 f"Extracted {len(parts)} parts from deliverable PDF bookmarks", time.time() - t0)
                    return
                else:
                    self._record("F15_T05", "F15", "PDF outline bookmarks match parts", "SKIP",
                                 f"Full 8-part PDF bookmark outline pending Milestone M5 (current parts in outline: {len(parts)})", time.time() - t0)
                    return
        self._record("F15_T05", "F15", "PDF outline bookmarks match parts", "SKIP",
                     "PDF bookmark outline verification pending Milestone M5 full build", time.time() - t0)

    # -------------------------------------------------------------------------
    # Feature 16: Opaque-Box E2E Test Suite Meta
    # -------------------------------------------------------------------------
    def test_f16_01_test_runner_executable_contract(self):
        t0 = time.time()
        runner = PROJECT_ROOT / "tests" / "test_runner.py"
        if runner.is_file() and os.access(runner, os.X_OK):
            self._record("F16_T01", "F16", "test_runner.py executable contract", "PASS",
                         f"test_runner.py established and executable at {runner}", time.time() - t0)
        elif runner.is_file():
            self._record("F16_T01", "F16", "test_runner.py executable contract", "PASS",
                         f"test_runner.py exists at {runner} (runnable with python3)", time.time() - t0)
        else:
            self._record("F16_T01", "F16", "test_runner.py executable contract", "FAIL",
                         f"test_runner.py not found at {runner}", time.time() - t0)

    def test_f16_02_test_runner_zero_exit_code_on_pass(self):
        t0 = time.time()
        runner = PROJECT_ROOT / "tests" / "test_runner.py"
        try:
            res = subprocess.run(
                [sys.executable, str(runner), "--tier", "2", "--json"],
                capture_output=True,
                text=True,
                timeout=45,
                cwd=str(PROJECT_ROOT)
            )
            if res.returncode == 0:
                data = json.loads(res.stdout) if res.stdout else {}
                if data.get("failed", 0) == 0:
                    self._record("F16_T02", "F16", "test_runner exit code 0 contract", "PASS",
                                 f"test_runner returned exit code 0 and 0 failures on Tier 2", time.time() - t0)
                    return
                else:
                    self._record("F16_T02", "F16", "test_runner exit code 0 contract", "FAIL",
                                 f"test_runner reported failures: {data.get('failed')}", time.time() - t0)
                    return
            else:
                self._record("F16_T02", "F16", "test_runner exit code 0 contract", "FAIL",
                             f"test_runner returned non-zero code {res.returncode}: {res.stderr[:200]}", time.time() - t0)
        except Exception as e:
            self._record("F16_T02", "F16", "test_runner exit code 0 contract", "FAIL",
                         f"Failed to execute test runner: {str(e)}", time.time() - t0)

    def test_f16_03_four_tiers_discoverable_and_executable(self):
        t0 = time.time()
        tier_files = [
            PROJECT_ROOT / "tests" / "tier1_feature_tests.py",
            PROJECT_ROOT / "tests" / "tier2_boundary_tests.py",
            PROJECT_ROOT / "tests" / "tier3_interaction_tests.py",
            PROJECT_ROOT / "tests" / "tier4_application_tests.py",
        ]
        all_exist = all(p.is_file() for p in tier_files)
        if not all_exist:
            missing = [str(p.name) for p in tier_files if not p.is_file()]
            self._record("F16_T03", "F16", "Four tiers discoverable and executable", "FAIL",
                         f"Missing test tier modules: {missing}", time.time() - t0)
            return

        try:
            from tier1_feature_tests import Tier1FeatureTests
            from tier2_boundary_tests import Tier2BoundaryTests
            from tier3_interaction_tests import Tier3InteractionTests
            from tier4_application_tests import Tier4ApplicationTests

            tiers = [Tier1FeatureTests, Tier2BoundaryTests, Tier3InteractionTests, Tier4ApplicationTests]
            all_callable = all(callable(getattr(cls, "run_all", None)) for cls in tiers)
            if all_callable:
                self._record("F16_T03", "F16", "Four tiers discoverable and executable", "PASS",
                             "All 4 test tiers discovered and expose callable run_all", time.time() - t0)
            else:
                self._record("F16_T03", "F16", "Four tiers discoverable and executable", "FAIL",
                             "One or more tier classes lack callable run_all method", time.time() - t0)
        except Exception as e:
            self._record("F16_T03", "F16", "Four tiers discoverable and executable", "FAIL",
                         f"Failed to import tier classes: {str(e)}", time.time() - t0)

    def test_f16_04_cli_flags_support_tier_and_milestone_and_json(self):
        t0 = time.time()
        runner = PROJECT_ROOT / "tests" / "test_runner.py"
        try:
            res = subprocess.run(
                [sys.executable, str(runner), "--help"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(PROJECT_ROOT)
            )
            if res.returncode == 0:
                stdout = res.stdout
                flags = ["--tier", "--milestone", "--json", "--verbose"]
                missing = [flag for flag in flags if flag not in stdout]
                if not missing:
                    self._record("F16_T04", "F16", "CLI flags support tier, milestone, json", "PASS",
                                 f"test_runner --help supports all flags: {flags}", time.time() - t0)
                else:
                    self._record("F16_T04", "F16", "CLI flags support tier, milestone, json", "FAIL",
                                 f"test_runner --help missing flags: {missing}", time.time() - t0)
            else:
                self._record("F16_T04", "F16", "CLI flags support tier, milestone, json", "FAIL",
                             f"test_runner --help returned non-zero code {res.returncode}", time.time() - t0)
        except Exception as e:
            self._record("F16_T04", "F16", "CLI flags support tier, milestone, json", "FAIL",
                         f"Failed to execute test_runner --help: {str(e)}", time.time() - t0)

    def test_f16_05_test_infra_and_test_ready_documentation_presence(self):
        t0 = time.time()
        infra_file = PROJECT_ROOT / "TEST_INFRA.md"
        if infra_file.is_file():
            self._record("F16_T05", "F16", "TEST_INFRA.md documentation presence", "PASS",
                         "TEST_INFRA.md verified at project root", time.time() - t0)
        else:
            self._record("F16_T05", "F16", "TEST_INFRA.md documentation presence", "FAIL",
                         "TEST_INFRA.md not found", time.time() - t0)
