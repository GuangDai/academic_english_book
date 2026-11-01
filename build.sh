#!/usr/bin/env bash
# ==============================================================================
# build.sh - Multi-Pass Convergent XeLaTeX Compilation Engine
# ==============================================================================
set -euo pipefail

# 1. Project Directory & Path Resolution
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 1.1 Command-Line Action Dispatcher
if [ "${1:-}" = "--test" ] || [ "${1:-}" = "test" ]; then
    shift
    TEST_RUNNER="$PROJECT_DIR/tests/test_runner.py"
    WITH_ENV="/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/with_pdf_env.sh"
    if [ -x "$WITH_ENV" ]; then
        exec "$WITH_ENV" python3 "$TEST_RUNNER" "$@"
    else
        exec python3 "$TEST_RUNNER" "$@"
    fi
fi

if [ "${1:-}" = "--clean" ] || [ "${1:-}" = "clean" ]; then
    echo "==> Cleaning build artifacts..."
    rm -rf "$PROJECT_DIR/build" "$PROJECT_DIR/academic_english_book.pdf"
    echo "==> Clean complete."
    exit 0
fi

OUTPUT_DIR="${1:-$PROJECT_DIR/build}"
SOURCE_FILE="${2:-main.tex}"
SOURCE_BASE="$(basename "$SOURCE_FILE" .tex)"
FINAL_PDF_NAME="academic_english_book.pdf"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "==> ERROR: Source file '$SOURCE_FILE' not found in $PROJECT_DIR" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# 2. TeX Live and Fontconfig Environment Injection
PDF_TEXLIVE_BIN="/home/guangdai/.local/share/papers-pdf-texlive/2026/bin/x86_64-linux"
PDF_RUNTIME_DIR="/home/guangdai/.local/share/papers-pdf-runtime"
PDF_VENV_BIN="/lzcapp/document/Papers/九篇论文_严谨三遍精读/rendering/.venv-toolkit-20261025/bin"

if [ -d "$PDF_RUNTIME_DIR/usr/bin" ]; then
    export PATH="$PDF_RUNTIME_DIR/usr/bin:$PATH"
fi
if [ -d "$PDF_TEXLIVE_BIN" ]; then
    export PATH="$PDF_TEXLIVE_BIN:$PATH"
fi
if [ -d "$PDF_VENV_BIN" ]; then
    export PATH="$PDF_VENV_BIN:$PATH"
fi

if [ -d "$PDF_RUNTIME_DIR/usr/lib" ]; then
    export LD_LIBRARY_PATH="$PDF_RUNTIME_DIR/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi
if [ -f "$PDF_RUNTIME_DIR/etc/fonts/fonts.conf" ]; then
    export FONTCONFIG_FILE="$PDF_RUNTIME_DIR/etc/fonts/fonts.conf"
fi
export TEXINPUTS=".:$PROJECT_DIR/style:$PROJECT_DIR:${TEXINPUTS:-}"
export PYTHONDONTWRITEBYTECODE=1

# 3. Environment Sanity Check
if ! command -v xelatex >/dev/null 2>&1; then
    echo "ERROR: xelatex not found on PATH ($PATH)" >&2
    exit 1
fi
if ! command -v xdvipdfmx >/dev/null 2>&1; then
    echo "ERROR: xdvipdfmx not found on PATH ($PATH)" >&2
    exit 1
fi

echo "======================================================================"
echo " Academic English Book Build Pipeline"
echo " Compiler: $(xelatex --version | head -n 1)"
echo " Source:   $SOURCE_FILE"
echo " Build:    $OUTPUT_DIR"
echo "======================================================================"

# Helper function: Compute sha256 of existing state files safely
compute_digest() {
    local dir="$1"
    local base="$2"
    local existing=()
    for ext in aux toc out; do
        if [ -f "$dir/$base.$ext" ]; then
            existing+=("$dir/$base.$ext")
        fi
    done
    if [ ${#existing[@]} -gt 0 ]; then
        sha256sum "${existing[@]}" | sha256sum | awk '{print $1}'
    else
        echo "uninitialized"
    fi
}

# 4. Multi-Pass Hash Convergence Loop
PREV_HASH=""
CONVERGED=false
MAX_PASSES=6
MIN_PASSES=3
ACTUAL_PASSES=0

for pass in $(seq 1 $MAX_PASSES); do
    ACTUAL_PASSES=$pass
    echo "[Pass $pass / $MAX_PASSES] Compiling intermediate XDV..."
    
    if ! xelatex -no-pdf -interaction=nonstopmode -halt-on-error \
                 -output-directory="$OUTPUT_DIR" "$SOURCE_FILE" > "$OUTPUT_DIR/build_pass_${pass}.log" 2>&1; then
        if [ "$pass" -eq 1 ] && [ -f "$OUTPUT_DIR/$SOURCE_BASE.aux" ]; then
            echo "==> Pass 1 failed (possible stale/corrupt aux cache). Purging aux cache and retrying..."
            rm -f "$OUTPUT_DIR/$SOURCE_BASE".{aux,toc,out,log,xdv}
            if xelatex -no-pdf -interaction=nonstopmode -halt-on-error \
                       -output-directory="$OUTPUT_DIR" "$SOURCE_FILE" > "$OUTPUT_DIR/build_pass_${pass}.log" 2>&1; then
                echo "==> Pass 1 retry succeeded after purging stale aux cache."
            else
                echo "==> ERROR: Compilation failed on pass $pass even after cleaning aux cache. Showing last 35 lines of log:" >&2
                tail -n 35 "$OUTPUT_DIR/build_pass_${pass}.log" >&2
                exit 1
            fi
        else
            echo "==> ERROR: Compilation failed on pass $pass. Showing last 35 lines of log:" >&2
            tail -n 35 "$OUTPUT_DIR/build_pass_${pass}.log" >&2
            exit 1
        fi
    fi
    
    CURR_HASH=$(compute_digest "$OUTPUT_DIR" "$SOURCE_BASE")
    echo "       State digest: $CURR_HASH"
    
    if [ "$pass" -ge "$MIN_PASSES" ] && [ "$CURR_HASH" = "$PREV_HASH" ]; then
        CONVERGED=true
        echo "==> Hash converged on pass $pass! Cross-references & ToC stabilized."
        break
    fi
    PREV_HASH="$CURR_HASH"
done

if [ "$CONVERGED" = false ]; then
    echo "WARNING: Multi-pass reached limit ($MAX_PASSES passes) without strict hash convergence."
fi

# 5. Emit Final PDF via xdvipdfmx
echo "[Emit PDF] Converting XDV to publication-quality PDF via xdvipdfmx..."
if ! xdvipdfmx -o "$OUTPUT_DIR/$SOURCE_BASE.pdf" "$OUTPUT_DIR/$SOURCE_BASE.xdv" > "$OUTPUT_DIR/xdvipdfmx.log" 2>&1; then
    echo "==> ERROR: xdvipdfmx failed. Showing log:" >&2
    cat "$OUTPUT_DIR/xdvipdfmx.log" >&2
    exit 1
fi

# 6. Deliverable Synchronization
if [ "$SOURCE_BASE" = "main" ]; then
    cp "$OUTPUT_DIR/$SOURCE_BASE.pdf" "$PROJECT_DIR/$FINAL_PDF_NAME"
    DELIVERABLE_PATH="$PROJECT_DIR/$FINAL_PDF_NAME"
else
    DELIVERABLE_PATH="$OUTPUT_DIR/$SOURCE_BASE.pdf"
fi

PDF_SIZE=$(stat -c%s "$DELIVERABLE_PATH" 2>/dev/null || stat -f%z "$DELIVERABLE_PATH")
PDF_SIZE_HUMAN=$(ls -lh "$DELIVERABLE_PATH" | awk '{print $5}')

echo "======================================================================"
echo " BUILD SUCCESSFUL!"
echo " Passes:      $ACTUAL_PASSES (Converged: $CONVERGED)"
echo " Output:      $DELIVERABLE_PATH ($PDF_SIZE_HUMAN, $PDF_SIZE bytes)"
echo " Build Dir:   $OUTPUT_DIR/"
echo "======================================================================"
