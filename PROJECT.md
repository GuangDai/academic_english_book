# Project: Academic English Textbook and Workbook (基于 LaTeX 的学术英语教学书与实战练习册)

## Architecture
The project unifies two comprehensive academic English training packages (`academic_english_training.zip` and `academic_paragraph_and_essay_mastery.zip`) into an authoritative, beautifully typeset bilingual LaTeX book and interactive workbook.

The book is structured into 8 modular parts with frontmatter and backmatter:
- **Frontmatter**: Title Page, Preface & Methodology, Hyperlinked Table of Contents (`\tableofcontents`).
- **Part I: Lexical Awakening & Academic Polysemy (词汇激活与熟词生义精讲)**: High-frequency academic polysemy, valency shifts, affixes, and collocations.
- **Part II: Syntactic Constituents & Anti-Top-Heavy Grammar (句法骨架与句子成分精讲)**: 5 basic sentence patterns, End-weight principle, anti-top-heavy grammar (G001–G036), and 24 academic functional templates (EP001–EP024).
- **Part III: Discourse Logic & Argumentation Engine (篇章逻辑与论证引擎)**: Given-to-New flow, Toulmin micro-arguments, counterfactual concession-rebuttals, and zero AI-ese discourse surgery (L001–L030).
- **Part IV: The 48 Core Paragraph Blueprints Encyclopedia (48大段落构建蓝图全书)**: 6 thematic tracks covering Abstract, Intro, Methodology, Experiments, Limitations, Data Analysis, Argumentation, and Oral/Rebuttal/SoP (BP01–BP48).
- **Part V: Diagnostic Revision Clinic & 60 Surgical Cases (深度病段诊所与母语级重构图谱)**: 5 primary defect categories and 4-step surgical reconstructions (RC01–RC60).
- **Part VI: Full-Text Anthology (全篇范文与段落蓝图链拆解文库)**: 24 complete papers, speeches, rebuttals, SoPs, proposals, and essays (FT01–FT24).
- **Part VII: The Daily Practice Workbook with Ruled Writing Lines (每日实战练习册)**: Generous 11mm composition ruled lines for handwriting, inline fill-in underlines, and sentence replacement rewrite blocks.
- **Part VIII: Comprehensive Answer Key & Rubrics (书末独立完整答案与自检评分量表)**: Two-level indexed rapid-lookup Answer Keys for all workbook exercises and diagnostic rubrics.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Archive Extraction & Verification | Unpack both source zip archives cleanly and preserve data integrity | M1 | R1 |
| 2 | Modular Style Package | `style/academic_book_style.tex` with geometry, colors, titlesec, fancyhdr, tcolorbox | M1 | R2 |
| 3 | Composition Ruled Lines System | 11mm wide handwriting ruled lines (`\writinglines[11mm]{n}`) via pure TeX `\hrule` | M1 | R4 |
| 4 | Sentence Replacement Scaffold | Target expression highlights (`\DefectTarget`) and rewrite guide (`\SentenceRewriteItem`) | M1 | R4 |
| 5 | Automated Build Scripts | `build.sh` and `Makefile` with environment injection and multi-pass convergence | M1 | R6 |
| 6 | Frontmatter & Hyperlinked ToC | Hyperlinked Table of Contents with widened number boxes and PDF bookmarks | M2 | R3 |
| 7 | Lexical & Grammar Chapters | Parts I & II covering polysemy, valency, 36 grammar rules, and 24 templates | M2 | R1, R2 |
| 8 | Discourse Logic & Blueprints | Parts III & IV covering 30 logic rules and 48 paragraph blueprints in tcolorboxes | M2 | R1, R2 |
| 9 | Revision Clinic & Full-Text Anthology | Parts V & VI presenting 60 diagnostic cases and 24 model full compositions | M2 | R1, R2 |
| 10 | Interactive Workbook Layout | Part VII with ample handwriting ruled lines and clear task prompts | M3 | R4 |
| 11 | Chapter New-Page Enforcement | Every `\chapter` starts on a new page without accidental blank verso pages | M3 | R3 |
| 12 | Color Annotation Hierarchy | Clear visual color coding for concepts, examples, tips, errors, and exercises | M3 | R2 |
| 13 | Comprehensive Answer Key | Part VIII independent backmatter with 2-level indexing by chapter and question | M4 | R5 |
| 14 | Analytic Rubrics & Notes | Multi-dimensional scoring rubrics and constituent analyses in Answer Key | M4 | R5 |
| 15 | E2E PDF Compilation & Verification | Zero fatal errors, zero missing characters, verified bookmarks, clean PDF | M5 | R6 |
| 16 | Opaque-Box E2E Test Suite | Comprehensive multi-tier test harness validating structure, layout, and content | E2E Track | Dual Track |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Infrastructure & LaTeX Styling Engine | Extract archives, create `style/academic_book_style.tex`, implement boxes & ruled lines, setup `build.sh` & `Makefile` | None | DONE |
| M2 | Master Textbook Chapters (Parts I–VI) | Author frontmatter, Parts I–VI using modular TeX files, concept/example/tip boxes, color coding | M1 | PLANNED |
| M3 | Interactive Workbook with Ruled Lines (Part VII) | Author Part VII workbook exercises across 4 stages with 11mm composition lines and rewrite scaffolds | M1 | PLANNED |
| M4 | Comprehensive Answer Key Appendix (Part VIII) | Author Part VIII Answer Key with chapter/day indexing, model answers, analyses, and rubrics | M1 | PLANNED |
| M5 | E2E Compilation & Full PDF Validation | Wire `main.tex`, execute multi-pass compilation, pass 100% E2E test suite, adversarial coverage hardening | M2, M3, M4, TEST_READY | PLANNED |
| E2E | E2E Testing Suite Track | Independent test suite: infra, Category-Partition/BVA test cases (Tiers 1-4), publish `TEST_READY.md` | M1 | DONE (Remediated) |

## Interface Contracts
### `style/academic_book_style.tex` ↔ Chapter TeX Modules
- **Geometry**: A4, 23mm margins (`\textwidth=164mm`).
- **Typography**: Times New Roman (body), SimSun (CJK with AutoFakeBold=2), Noto Sans Mono CJK SC (monospace).
- **Colors**: `AcadNavy` (primary), `AcadSlate` (secondary), `AcadTeal` (example), `AcadAmber` (tip), `AcadForest` (exercise), `TargetHighlight` (error/replace), `RuleLineColor` (writing lines).
- **Boxes**:
  - `\begin{ConceptBox}{Title} ... \end{ConceptBox}`
  - `\begin{ExampleBox}{Title} ... \end{ExampleBox}`
  - `\begin{TipBox}{Title} ... \end{TipBox}`
  - `\begin{ExerciseBox}{Title} ... \end{ExerciseBox}`
- **Handwriting Lines & Replacement**:
  - `\writinglines[11mm]{N}`: draws $N$ horizontal lines with 11mm row spacing.
  - `\fillblank[width]{prompt}`: underlined fill-in blank.
  - `\DefectTarget{text}`: highlights text to be replaced in bold rose red.
  - `\SentenceRewriteItem[lines]{number}{original}`: formatted sentence rewrite task.
  - `\begin{ParagraphRevision}{case_num}{title} ... \end{ParagraphRevision}`: paragraph revision scaffold.

### Chapter Modules ↔ Master `main.tex`
- All chapters are modular `.tex` files included via `\input{chapters/...}`.
- Every chapter starts with `\chapter{...}`. `openany` in document class guarantees chapter starts on the immediate new page without blank sheets.

### Workbook Exercises (Part VII) ↔ Answer Key (Part VIII)
- Every exercise item has a unique index: `Part VII: Chapter X, Day Y, Task Z` or `Item N`.
- Part VIII Answer Key provides corresponding header `\AnswerDayHeader{Day}{Title}` and items `\AnswerItem{ID}{Reference Answer}{Analysis}` matching the exercise numbering exactly.

## Code Layout
```
/lzcapp/document/academic_english_book/
├── build.sh                      # Executable compilation script with TeXLive env injection
├── Makefile                      # Standard Makefile targets (all, pdf, clean, test)
├── PROJECT.md                    # Master project specification and progress tracking
├── main.tex                      # Master LaTeX document combining all parts
├── style/
│   └── academic_book_style.tex   # Package imports, geometry, colors, boxes, ruled lines
├── assets/
│   ├── raw_training/             # Extracted academic_english_training data
│   └── raw_mastery/              # Extracted academic_paragraph_and_essay_mastery data
├── chapters/
│   ├── frontmatter.tex           # Title page, preface, how to use
│   ├── part1_lexicon.tex         # Part I: Polysemy, affixes, collocations
│   ├── part2_syntax.tex          # Part II: 5 sentence types, End-weight, G001-G036, EP001-EP024
│   ├── part3_discourse.tex       # Part III: Logic rules L001-L030
│   ├── part4_blueprints.tex      # Part IV: 48 Paragraph Blueprints BP01-BP48
│   ├── part5_revision_clinic.tex # Part V: 60 Revision Cases RC01-RC60
│   ├── part6_anthology.tex       # Part VI: 24 Full Text Anthology FT01-FT24
│   ├── part7_workbook.tex        # Part VII: Workbook with ruled handwriting lines
│   └── part8_answer_key.tex      # Part VIII: Comprehensive indexed Answer Keys
├── tests/
│   ├── test_runner.py            # Automated E2E test runner
│   ├── tier1_feature_tests.py    # Tier 1: Feature coverage tests
│   ├── tier2_boundary_tests.py   # Tier 2: Boundary & corner cases
│   ├── tier3_interaction_tests.py# Tier 3: Cross-feature combinations
│   └── tier4_application_tests.py# Tier 4: Real-world acceptance scenarios
└── build/                        # Isolated compilation build artifacts and final PDF
```
