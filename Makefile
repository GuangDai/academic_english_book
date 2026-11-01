# ==============================================================================
# Makefile - Academic English Book Build System
# ==============================================================================

SHELL := /usr/bin/env bash
.SHELLFLAGS := -euo pipefail -c

BUILD_DIR ?= build
SOURCE ?= main.tex
TARGET_PDF ?= academic_english_book.pdf

.PHONY: all pdf clean qa test lint-tests help

all: pdf

pdf:
	chmod +x ./build.sh
	./build.sh $(BUILD_DIR) $(SOURCE)

lint-tests:
	python3 tests/ast_test_guard.py

test: lint-tests
	chmod +x ./build.sh
	./build.sh --test

clean:
	@echo "==> Cleaning build artifacts..."
	rm -rf $(BUILD_DIR) $(TARGET_PDF)
	@echo "==> Clean complete."

qa: pdf
	@if [ -f "/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/pdf_format_rendering_toolkit/qa_pdf.py" ]; then \
		echo "==> Running PDF QA inspection..."; \
		rm -rf $(BUILD_DIR)/qa; \
		/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/with_pdf_env.sh python \
			/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/pdf_format_rendering_toolkit/qa_pdf.py \
			$(TARGET_PDF) --output $(BUILD_DIR)/qa --log $(BUILD_DIR)/build_pass_3.log || true; \
	else \
		echo "==> QA toolkit not found; skipping QA."; \
	fi

help:
	@echo "Academic English Book Build System"
	@echo "Available targets:"
	@echo "  all    : Compile complete book PDF (default, runs multi-pass convergence)"
	@echo "  pdf    : Alias for 'all'"
	@echo "  clean  : Remove build/ directory and output PDF"
	@echo "  test   : Execute automated E2E test suite under injected TeX/Python environment"
	@echo "  qa     : Run PDF QA inspection tool"
	@echo "  help   : Display this help message"
