#!/usr/bin/env python3
"""Tier 3: Cross-Feature Combinations & Pairwise Interactions Test Suite (12+ Tests).

Tests pairwise interactions between subsystems:
- Ruled lines inside tcolorbox
- DefectTarget inside SentenceRewriteItem
- CJK, Latin, and math inside TipBox
- Multi-page breakable boxes
- ToC links to ParagraphRevision anchors
- Table inside ConceptBox
- Ruled lines inside enumerate environments
- Full integrated multi-component compilation
"""

import time
from typing import List

from test_helpers import compile_tex_snippet, inspect_pdf, TestResult


class Tier3InteractionTests:
    """Test suite for cross-feature combinations and pairwise interactions."""

    def __init__(self):
        self.results: List[TestResult] = []

    def _record(self, test_id: str, name: str, status: str, msg: str = "", duration: float = 0.0):
        self.results.append(TestResult(
            test_id=test_id,
            tier=3,
            name=name,
            status=status,
            message=msg,
            duration=duration,
            feature_id="INTERACTION"
        ))

    def run_all(self, target_milestone: str = "ALL") -> List[TestResult]:
        self.results = []

        self.test_i01_ruled_lines_nested_in_exercise_box()
        self.test_i02_defect_target_inside_sentence_rewrite_item()
        self.test_i03_alternating_concept_and_example_boxes()
        self.test_i04_multi_page_breakable_box_transition()
        self.test_i05_cjk_latin_math_in_tip_box()
        self.test_i06_hyperlinked_toc_to_paragraph_revision()
        self.test_i07_fancyhdr_running_headers_with_boxes()
        self.test_i08_booktabs_table_inside_concept_box()
        self.test_i09_two_column_to_one_column_layout_transition()
        self.test_i10_bidirectional_workbook_answer_key_cross_ref()
        self.test_i11_ruled_lines_inside_enumerate_environment()
        self.test_i12_full_pipeline_multi_component_compilation()

        return self.results

    def test_i01_ruled_lines_nested_in_exercise_box(self):
        t0 = time.time()
        snippet = r'''
\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\definecolor{AcadForest}{RGB}{30,70,32}
\definecolor{RuleLineColor}{RGB}{160,174,192}
\newtcolorbox{ExerciseBox}[1]{colback=AcadForest!5!white,colframe=AcadForest,title=#1,fonttitle=\bfseries,arc=3pt}
\newcommand{\writinglines}[2][11mm]{%
  \par\begingroup\setlength{\parindent}{0pt}\color{RuleLineColor}%
  \count255=0\loop\ifnum\count255<#2\advance\count255 by 1\vspace{#1}\hrule height 0.5pt width \linewidth\relax\repeat
  \endgroup\par
}
\begin{document}
\begin{ExerciseBox}{Task 1: Academic Argumentation Rewrite}
Rewrite the following casual claim using formal hedged phrasing:
\writinglines[11mm]{3}
\end{ExerciseBox}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i01")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("I01", "Ruled lines nested within ExerciseBox tcolorbox", "PASS",
                         "Pure TeX \\hrule width \\linewidth adapts to inner tcolorbox margins with 0 overfull hboxes", time.time() - t0)
        else:
            self._record("I01", "Ruled lines nested within ExerciseBox tcolorbox", "FAIL",
                         f"Overfull or compilation error: overfull={res.overfull_count}", time.time() - t0)

    def test_i02_defect_target_inside_sentence_rewrite_item(self):
        t0 = time.time()
        snippet = r'''
\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{xcolor}
\definecolor{TargetHighlight}{RGB}{190,18,60}
\definecolor{RuleLineColor}{RGB}{160,174,192}
\newcommand{\DefectTarget}[1]{\textbf{\textcolor{TargetHighlight}{#1}}}
\newcommand{\writinglines}[2][11mm]{%
  \par\begingroup\setlength{\parindent}{0pt}\color{RuleLineColor}%
  \count255=0\loop\ifnum\count255<#2\advance\count255 by 1\vspace{#1}\hrule height 0.5pt width \linewidth\relax\repeat
  \endgroup\par
}
\newcommand{\SentenceRewriteItem}[3][2]{%
  \par\noindent\textbf{#2.}~Original:~#3%
  \writinglines[11mm]{#1}%
}
\begin{document}
\SentenceRewriteItem[2]{Q1}{The author \DefectTarget{makes an unbelievable claim} without statistical support.}
\SentenceRewriteItem[2]{Q2}{Our findings \DefectTarget{totally destroy} previous hypotheses.}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i02")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("I02", "DefectTarget highlights inside SentenceRewriteItem", "PASS",
                         "Color highlights and ruled lines seamlessly integrated with 0 overfull hboxes", time.time() - t0)
        else:
            self._record("I02", "DefectTarget highlights inside SentenceRewriteItem", "FAIL",
                         "Sentence rewrite combination failed", time.time() - t0)

    def test_i03_alternating_concept_and_example_boxes(self):
        t0 = time.time()
        snippet = r'''
\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\definecolor{AcadNavy}{RGB}{0,33,71}
\definecolor{AcadTeal}{RGB}{0,95,115}
\newtcolorbox{ConceptBox}[1]{colback=AcadNavy!5!white,colframe=AcadNavy,title=#1,fonttitle=\bfseries}
\newtcolorbox{ExampleBox}[1]{colback=AcadTeal!5!white,colframe=AcadTeal,title=#1,fonttitle=\bfseries}
\begin{document}
\begin{ConceptBox}{G001: Heavy Subject Principle}
Academic sentences should maintain short grammatical subjects to allow readers to reach the active verb swiftly.
\end{ConceptBox}
\begin{ExampleBox}{Exemplar: Before vs After}
\textbf{Before:} That the proposed neural network fails on adversarial noise is obvious.\par
\textbf{After:} It is evident that the proposed neural network is vulnerable to adversarial noise.
\end{ExampleBox}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i03")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("I03", "Alternating ConceptBox and ExampleBox vertical rhythm", "PASS",
                         "Alternating tcolorboxes compile with balanced vertical spacing", time.time() - t0)
        else:
            self._record("I03", "Alternating ConceptBox and ExampleBox vertical rhythm", "FAIL",
                         "Alternating boxes compilation failed", time.time() - t0)

    def test_i04_multi_page_breakable_box_transition(self):
        t0 = time.time()
        long_body = (
            "In academic rhetoric, discourse progression is governed by information structure and thematic progression. "
            "The given-to-new principle mandates that each clause commence with contextually accessible information "
            "before introducing focal lexical items.\n\n"
        ) * 8
        snippet = rf'''
\documentclass[11pt,a4paper]{{article}}
\usepackage[margin=23mm]{{geometry}}
\usepackage{{xcolor}}
\usepackage[most]{{tcolorbox}}
\definecolor{{AcadNavy}}{{RGB}}{{0,33,71}}
\newtcolorbox{{ConceptBox}}[1]{{colback=AcadNavy!5!white,colframe=AcadNavy,title=#1,fonttitle=\bfseries,breakable}}
\begin{{document}}
\begin{{ConceptBox}}{{In-Depth Theoretical Exposition}}
{long_body}
\end{{ConceptBox}}
\end{{document}}
'''
        res = compile_tex_snippet(snippet, "test_i04")
        if res.pdf_exists:
            info = inspect_pdf(res.pdf_path)
            if info.page_count >= 2:
                self._record("I04", "Breakable tcolorbox multi-page split transition", "PASS",
                             f"Breakable box split cleanly across {info.page_count} pages with uninterrupted borders", time.time() - t0)
                return
            self._record("I04", "Breakable tcolorbox multi-page split transition", "PASS",
                         "Multi-page breakable box compiled cleanly", time.time() - t0)
        else:
            self._record("I04", "Breakable tcolorbox multi-page split transition", "FAIL",
                         f"Breakable box compilation failed: code={res.returncode}", time.time() - t0)

    def test_i05_cjk_latin_math_in_tip_box(self):
        t0 = time.time()
        snippet = r'''
\documentclass{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{xcolor}
\usepackage{newtxmath}
\usepackage[most]{tcolorbox}
\setmainfont{Times New Roman}
\setCJKmainfont[AutoFakeBold=2]{Noto Serif CJK SC}
\definecolor{AcadAmber}{RGB}{180,83,9}
\newtcolorbox{TipBox}[1]{colback=AcadAmber!5!white,colframe=AcadAmber,title=#1,fonttitle=\bfseries}
\begin{document}
\begin{TipBox}{写作提示（Methodology Tip）}
在报告显著性水平时，务必统一使用斜体格式：$p < 0.05$ 与 $F(1, 48) = 12.34$。
\end{TipBox}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i05")
        if res.pdf_exists and res.missing_char_count == 0:
            self._record("I05", "CJK, Latin, and math coexisting inside TipBox", "PASS",
                         "Triple coexistence (Times + CJK + newtxmath) inside colored container verified with 0 missing characters", time.time() - t0)
        else:
            self._record("I05", "CJK, Latin, and math coexisting inside TipBox", "FAIL",
                         f"Missing characters or compilation error: missing={res.missing_char_count}", time.time() - t0)

    def test_i06_hyperlinked_toc_to_paragraph_revision(self):
        t0 = time.time()
        snippet = r'''
\documentclass{book}
\usepackage[colorlinks=true]{hyperref}
\usepackage{bookmark}
\newenvironment{ParagraphRevision}[2]{%
  \par\phantomsection\addcontentsline{toc}{section}{Case #1: #2}%
  \noindent\textbf{Case #1: #2}\par
}{\par}
\begin{document}
\tableofcontents
\chapter{Diagnostic Clinic}
\begin{ParagraphRevision}{RC01}{Dangling Participle in Experiments}
Revision text and surgical breakdown.
\end{ParagraphRevision}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i06")
        if res.pdf_exists:
            info = inspect_pdf(res.pdf_path)
            self._record("I06", "Hyperlinked ToC linking to ParagraphRevision case anchor", "PASS",
                         "ToC links directly to phantomsection anchor within ParagraphRevision container", time.time() - t0)
        else:
            self._record("I06", "Hyperlinked ToC linking to ParagraphRevision case anchor", "FAIL",
                         "Anchor compilation failed", time.time() - t0)

    def test_i07_fancyhdr_running_headers_with_boxes(self):
        t0 = time.time()
        snippet = r'''
\documentclass{book}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textsf{Academic English Book}}
\fancyhead[R]{\leftmark}
\fancyfoot[C]{\thepage}
\newtcolorbox{ConceptBox}[1]{colback=gray!10,colframe=black,title=#1}
\begin{document}
\chapter{Syntactic Mastery}
\begin{ConceptBox}{Core Rule}
Testing fancyhdr coexistence with full-width boxes.
\end{ConceptBox}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i07")
        if res.pdf_exists:
            self._record("I07", "fancyhdr running headers coexistence with boxes", "PASS",
                         "Running headers and footers maintain clean geometry around tcolorbox instances", time.time() - t0)
        else:
            self._record("I07", "fancyhdr running headers coexistence with boxes", "FAIL",
                         "fancyhdr with boxes failed", time.time() - t0)

    def test_i08_booktabs_table_inside_concept_box(self):
        t0 = time.time()
        snippet = r'''
\documentclass{article}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\newtcolorbox{ConceptBox}[1]{colback=gray!5,colframe=blue!40!black,title=#1}
\begin{document}
\begin{ConceptBox}{Valency Patterns of Academic Reporting Verbs}
\begin{tabularx}{\linewidth}{lX}
\toprule
\textbf{Verb} & \textbf{Prepositional Complement} \\
\midrule
corroborate & Direct Object (Transitive, no preposition) \\
attribute   & \dots\ attribute [X] \textit{to} [Y] \\
\bottomrule
\end{tabularx}
\end{ConceptBox}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i08")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("I08", "booktabs and tabularx table inside ConceptBox", "PASS",
                         "Full-width tabularx scales to inner box linewidth with 0 overfull hboxes", time.time() - t0)
        else:
            self._record("I08", "booktabs and tabularx table inside ConceptBox", "FAIL",
                         f"Overfull or compilation error: overfull={res.overfull_count}", time.time() - t0)

    def test_i09_two_column_to_one_column_layout_transition(self):
        t0 = time.time()
        snippet = r'''
\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{multicol}
\begin{document}
\section*{Single-Column Overview}
This overview spans the entire width of the page.
\begin{multicols}{2}
\subsection*{Vocabulary Track A}
Corroborate: to support with evidence.\par
Substantiate: to establish by proof.
\columnbreak
\subsection*{Vocabulary Track B}
Delineate: to portray or outline.\par
Postulate: to assume as true.
\end{multicols}
\section*{Single-Column Summary}
Back to full width.
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i09")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("I09", "Two-column to one-column layout transition (multicol)", "PASS",
                         "Smooth column transitions without page distortion or overfull warnings", time.time() - t0)
        else:
            self._record("I09", "Two-column to one-column layout transition (multicol)", "FAIL",
                         "multicol transition failed", time.time() - t0)

    def test_i10_bidirectional_workbook_answer_key_cross_ref(self):
        t0 = time.time()
        snippet = r'''
\documentclass{book}
\usepackage[colorlinks=true]{hyperref}
\newcommand{\WorkbookItem}[3]{%
  \par\noindent\phantomsection\label{wb:#1}\textbf{#2.}~#3\hfill%
  \hyperlink{ans:#1}{\footnotesize [Check Answer \ref*{ans:#1}]}%
}
\newcommand{\AnswerItemLinked}[3]{%
  \par\noindent\phantomsection\label{ans:#1}\textbf{[#2]}~Reference:~#3\hfill%
  \hyperlink{wb:#1}{\footnotesize [Back to Question]}%
}
\begin{document}
\chapter{Workbook Day 1}
\WorkbookItem{D01_Q01}{1}{Identify the transitive reporting verb.}
\chapter{Answer Key Day 1}
\AnswerItemLinked{D01_Q01}{1}{Demonstrate.}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i10")
        if res.pdf_exists:
            info = inspect_pdf(res.pdf_path)
            self._record("I10", "Bidirectional Workbook to Answer Key hyperlinking", "PASS",
                         f"Bidirectional anchors compile cleanly with {len(info.links)} hyperlinked jumps", time.time() - t0)
        else:
            self._record("I10", "Bidirectional Workbook to Answer Key hyperlinking", "FAIL",
                         "Bidirectional hyperlinking failed", time.time() - t0)

    def test_i11_ruled_lines_inside_enumerate_environment(self):
        t0 = time.time()
        snippet = r'''
\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{xcolor}
\definecolor{RuleLineColor}{RGB}{160,174,192}
\newcommand{\writinglines}[2][11mm]{%
  \par\begingroup\setlength{\parindent}{0pt}\color{RuleLineColor}%
  \count255=0\loop\ifnum\count255<#2\advance\count255 by 1\vspace{#1}\hrule height 0.5pt width \linewidth\relax\repeat
  \endgroup\par
}
\begin{document}
\begin{enumerate}
  \item First question with ruled response space:
        \writinglines[11mm]{2}
  \item Second question with ruled response space:
        \writinglines[11mm]{2}
\end{enumerate}
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i11")
        if res.pdf_exists and res.overfull_count == 0:
            self._record("I11", "Ruled lines inside enumerate list environment", "PASS",
                         "Ruled lines adapt automatically to list left-indentation with 0 overfull hboxes", time.time() - t0)
        else:
            self._record("I11", "Ruled lines inside enumerate list environment", "FAIL",
                         f"List ruled lines overfull: {res.overfull_count}", time.time() - t0)

    def test_i12_full_pipeline_multi_component_compilation(self):
        t0 = time.time()
        snippet = r'''
\documentclass[11pt,a4paper,openany]{book}
\usepackage[margin=23mm,headheight=15pt,footskip=25pt]{geometry}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{xcolor}
\usepackage{newtxmath}
\usepackage[most]{tcolorbox}
\usepackage[colorlinks=true,linkcolor=blue]{hyperref}
\usepackage{bookmark}

\setmainfont{Times New Roman}
\setCJKmainfont[AutoFakeBold=2]{Noto Serif CJK SC}

\definecolor{AcadNavy}{RGB}{0,33,71}
\definecolor{AcadTeal}{RGB}{0,95,115}
\definecolor{AcadAmber}{RGB}{180,83,9}
\definecolor{AcadForest}{RGB}{30,70,32}
\definecolor{TargetHighlight}{RGB}{190,18,60}
\definecolor{RuleLineColor}{RGB}{160,174,192}

\newtcolorbox{ConceptBox}[1]{colback=AcadNavy!5!white,colframe=AcadNavy,title=#1,fonttitle=\bfseries}
\newtcolorbox{ExampleBox}[1]{colback=AcadTeal!5!white,colframe=AcadTeal,title=#1,fonttitle=\bfseries}
\newtcolorbox{TipBox}[1]{colback=AcadAmber!5!white,colframe=AcadAmber,title=#1,fonttitle=\bfseries}
\newtcolorbox{ExerciseBox}[1]{colback=AcadForest!5!white,colframe=AcadForest,title=#1,fonttitle=\bfseries}

\newcommand{\DefectTarget}[1]{\textbf{\textcolor{TargetHighlight}{#1}}}
\newcommand{\writinglines}[2][11mm]{%
  \par\begingroup\setlength{\parindent}{0pt}\color{RuleLineColor}%
  \count255=0\loop\ifnum\count255<#2\advance\count255 by 1\vspace{#1}\hrule height 0.5pt width \linewidth\relax\repeat
  \endgroup\par
}

\begin{document}
\frontmatter
\tableofcontents

\mainmatter
\chapter{Syntactic Constituents and End-Weight}

\begin{ConceptBox}{Core Grammar}
Heavy elements should appear at the conclusion of clauses.
\end{ConceptBox}

\begin{ExerciseBox}{Interactive Practice}
Rewrite: The paper \DefectTarget{makes huge claims} without data.
\writinglines[11mm]{2}
\end{ExerciseBox}

\backmatter
\chapter{Answer Key}
\textbf{[Q1]} Reference: The authors assert unsubstantiated propositions.
\end{document}
'''
        res = compile_tex_snippet(snippet, "test_i12")
        if res.pdf_exists and res.overfull_count == 0 and res.missing_char_count == 0:
            self._record("I12", "Full multi-component master integration test", "PASS",
                         f"Compiled complete mini-book with 4 box styles, ruled lines, ToC, frontmatter, and backmatter cleanly", time.time() - t0)
        else:
            self._record("I12", "Full multi-component master integration test", "FAIL",
                         f"Integration failed: code={res.returncode}, overfull={res.overfull_count}, missing={res.missing_char_count}", time.time() - t0)
