# Test Infrastructure Specification: Academic English Textbook & Workbook

**Project**: Academic English Textbook and Workbook (基于 LaTeX 的学术英语教学书与实战练习册)  
**Track**: E2E Testing Suite Track (Dual Track)  
**Author**: `teamwork_test_writer_e2e_1`  
**Status**: ACTIVE  
**Last Updated**: 2026-10-31  

---

## 1. Testing Methodology & Architectural Principles

The test harness for this project is engineered as an **opaque-box, requirement-driven, multi-tier verification engine**. In accordance with high-reliability engineering standards, tests validate observable deliverables against authoritative specifications without binding to private implementation details.

### Core Testing Principles
1. **Opaque-Box Requirement Derivation**:
   Expected outputs and structural assertions are derived strictly from:
   - `ORIGINAL_REQUEST.md` (R1–R6 requirements and acceptance criteria)
   - `PROJECT.md` (Architecture, 16-feature inventory, milestone contracts, code layout)
   - Source dataset archives (`academic_english_training.zip` and `academic_paragraph_and_essay_mastery.zip`)
   - Host TeX Live runtime, Fontconfig configurations, and standard typographic contracts.

2. **4-Tier Hierarchical Methodology**:
   - **Tier 1: Feature Coverage (>=5 test cases per feature)**: Every single feature in the 16-feature inventory is tested across its happy path, contract constraints, and primary functions (80+ test cases).
   - **Tier 2: Boundary & Corner Cases (>=5 test cases per boundary feature)**: Tests stress edge cases such as empty lines, extreme line counts (e.g. 50 ruled lines), custom heights (5mm–25mm), special LaTeX meta-characters (`%`, `&`, `_`, `^`, `{}`), deep ToC nesting, CJK/Latin mixed boundaries, and extreme sentence lengths.
   - **Tier 3: Cross-Feature Combinations & Pairwise Interactions**: Tests verify combinations of disparate subsystems, including ruled writing lines nested within breakable `tcolorbox` containers, `\DefectTarget` highlights inside `\SentenceRewriteItem`, CJK/math coexistence, ToC hyperlinks referencing revised paragraph anchors, and multi-pass compiler convergence.
   - **Tier 4: Real-World Acceptance Scenarios**: Realistic end-to-end user journeys (Student interactive workbook solving, Instructor diagnostic clinic analysis, PDF reader outline navigation, and clean CI/CD automated build from scratch).

3. **Progressive Testability**:
   The test harness is designed to execute across all project phases (M1 through M5). When evaluating an earlier milestone (e.g. M1), tests verify the current milestone's deliverables and underlying data contracts; tests for subsequent milestones cleanly detect absent artifacts and report milestone status without failing the active test suite. Once an artifact is authored, the test runner automatically executes deep end-to-end assertions against the deliverable.

4. **Self-Contained Portability**:
   The test runner `tests/test_runner.py` requires zero third-party dependencies outside the Python 3 standard library and existing platform tools. When PyMuPDF (`fitz`) is present (e.g. in the rendering venv), the runner leverages it for deep PDF outline and bounding box analysis; otherwise, it falls back gracefully to a robust native PDF inspection parser.

---

## 2. Feature Inventory to Requirement Mapping

| Feature ID | Feature Name | Requirement | Milestone | Source Oracle / Contract | Tier 1 Tests |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **F01** | Archive Extraction & Verification | R1 | M1 | `academic_english_training.zip`, `academic_paragraph_and_essay_mastery.zip` | `F01_T01`–`F01_T05` |
| **F02** | Modular Style Package | R2 | M1 | `style/academic_book_style.tex`, 23mm margins, Times/SimSun fonts | `F02_T01`–`F02_T05` |
| **F03** | Composition Ruled Lines System | R4 | M1 | `\writinglines[11mm]{n}`, pure TeX `\hrule`, 11mm row height | `F03_T01`–`F03_T05` |
| **F04** | Sentence Replacement Scaffold | R4 | M1 | `\DefectTarget`, `\SentenceRewriteItem`, `\fillblank` | `F04_T01`–`F04_T05` |
| **F05** | Automated Build Scripts | R6 | M1 | `build.sh`, `Makefile`, TeX Live env injection, exit code 0 | `F05_T01`–`F05_T05` |
| **F06** | Frontmatter & Hyperlinked ToC | R3 | M2 | `\frontmatter`, `\tableofcontents`, `\@pnumwidth`, hyperref | `F06_T01`–`F06_T05` |
| **F07** | Lexical & Grammar Chapters | R1, R2 | M2 | Part I (polysemy, valency) & Part II (G001–G036, EP001–EP024) | `F07_T01`–`F07_T05` |
| **F08** | Discourse Logic & Blueprints | R1, R2 | M2 | Part III (L001–L030) & Part IV (48 blueprints BP01–BP48) | `F08_T01`–`F08_T05` |
| **F09** | Revision Clinic & Full-Text Anthology | R1, R2 | M2 | Part V (60 cases RC01–RC60) & Part VI (24 essays FT01–FT24) | `F09_T01`–`F09_T05` |
| **F10** | Interactive Workbook Layout | R4 | M3 | Part VII: Daily exercises, 11mm handwriting lines, task prompts | `F10_T01`–`F10_T05` |
| **F11** | Chapter New-Page Enforcement | R3 | M3 | `openany` documentclass, every `\chapter` starts on fresh page | `F11_T01`–`F11_T05` |
| **F12** | Color Annotation Hierarchy | R2 | M3 | AcadNavy, AcadSlate, AcadTeal, AcadAmber, AcadForest, TargetHighlight | `F12_T01`–`F12_T05` |
| **F13** | Comprehensive Answer Key | R5 | M4 | Part VIII: 2-level indexing (Chapter/Day -> Question ID) | `F13_T01`–`F13_T05` |
| **F14** | Analytic Rubrics & Notes | R5 | M4 | Part VIII: linguistic analysis, style notes, diagnostic rubrics | `F14_T01`–`F14_T05` |
| **F15** | E2E PDF Compilation & Verification | R6 | M5 | `build/academic_english_book.pdf`, 0 overfull, 0 missing characters | `F15_T01`–`F15_T05` |
| **F16** | Opaque-Box E2E Test Suite Meta | Dual Track | E2E | `tests/test_runner.py`, self-contained execution, exit code 0 | `F16_T01`–`F16_T05` |

---

## 3. Directory Layout

```
/lzcapp/document/academic_english_book/
├── TEST_INFRA.md                 # Test architecture & methodology specification
├── TEST_READY.md                 # Test execution verification and sign-off report
└── tests/
    ├── test_runner.py            # Unified executable test runner & reporter
    ├── test_helpers.py           # Shared utilities (XeLaTeX runner, PDF inspector, data checks)
    ├── tier1_feature_tests.py    # Tier 1: 80+ Feature Coverage tests (Features 1-16)
    ├── tier2_boundary_tests.py   # Tier 2: 15+ Boundary & Corner Case tests
    ├── tier3_interaction_tests.py# Tier 3: 12+ Pairwise Interaction tests
    └── tier4_application_tests.py# Tier 4: 5 Real-World Acceptance Scenarios
```

---

## 4. Test Runner CLI Instructions

The test runner can be invoked directly with Python 3:

```bash
# 1. Run the entire test suite (all 4 tiers)
python3 tests/test_runner.py

# 2. Run a specific tier (1, 2, 3, or 4)
python3 tests/test_runner.py --tier 1
python3 tests/test_runner.py --tier 2
python3 tests/test_runner.py --tier 3
python3 tests/test_runner.py --tier 4

# 3. Filter tests by milestone scope (e.g. M1, M2, M3, M4, M5, or ALL)
python3 tests/test_runner.py --milestone M1

# 4. Verbose output showing each test's assertion details
python3 tests/test_runner.py --verbose

# 5. Output machine-readable JSON summary for CI/CD integration
python3 tests/test_runner.py --json
```

### Exit Code Contract
- `0`: All executed tests passed (or skipped pending future milestones). Zero contract violations.
- `1`: One or more tests failed (contract violation, build error, or regression).

---

## 5. Verification Oracles & Standards

### 5.1 TeX Live & Font Environment
The runner automatically checks and exports the host TeX Live environment:
- **TeX Binaries**: `/home/guangdai/.local/share/papers-pdf-texlive/2026/bin/x86_64-linux`
- **Runtime Binaries**: `/home/guangdai/.local/share/papers-pdf-runtime/usr/bin`
- **Runtime Libraries**: `/home/guangdai/.local/share/papers-pdf-runtime/usr/lib`
- **Fontconfig Configuration**: `/home/guangdai/.local/share/papers-pdf-runtime/etc/fonts/fonts.conf`
- **PyMuPDF Venv**: `/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/.venv-toolkit-20261025/bin/python`

### 5.2 PDF Validation Metrics
When validating PDF deliverables, the following thresholds are enforced:
- **Missing Characters**: Exactly `0` instances of `Missing character:` in the compilation log.
- **Overfull `\hbox`**: Clean text formatting without unconstrained text margins.
- **Outline Hierarchy**: Verified document outline matching Parts I–VIII and Chapter titles.
- **Hyperlink Destination**: Valid page target coordinates for all ToC hyperlinks.
- **Ruled Line Spacing**: Exactly 11mm vertical pitch for composition ruled lines.
