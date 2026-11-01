#!/usr/bin/env python3
"""AST Test Integrity Guard for Academic English Book Test Suites.

Statically analyzes all Python test suites to enforce:
1. RULE-LINT-01 (Zero Dummy Facades): Every test must contain control flow / assertions;
   branchless functions unconditionally recording PASS are forbidden.
2. RULE-LINT-02 (Zero Fallback-to-PASS): No test may record PASS with 'Contract verified'
   or bypass missing deliverable files with PASS.
3. RULE-LINT-03 (Zero Unfailable Tests): Every non-skipped test must have a reachable FAIL path.
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Any

TESTS_DIR = Path(__file__).resolve().parent

class ASTTestIntegrityGuard:
    def __init__(self, directory: Path = TESTS_DIR):
        self.directory = directory
        self.violations: List[Dict[str, Any]] = []

    def scan_all(self) -> int:
        test_files = sorted(self.directory.glob("*.py"))
        for f in test_files:
            if f.name.startswith("tier") or f.name.startswith("adversarial"):
                self.lint_file(f)
        return len(self.violations)

    def lint_file(self, file_path: Path):
        code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(code, filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and (node.name.startswith("test_") or node.name.startswith("test")):
                self._lint_test_function(file_path, node)

    def _lint_test_function(self, file_path: Path, fn: ast.FunctionDef):
        record_calls = []
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and getattr(n.func, "attr", "") in ("_record", "record"):
                record_calls.append(n)

        if not record_calls:
            return

        has_control_flow = any(isinstance(n, (ast.If, ast.Assert, ast.Try, ast.While, ast.For)) for n in ast.walk(fn))

        # Check 1: Dummy Facade (No control flow, unconditional PASS)
        if not has_control_flow:
            for call in record_calls:
                for arg in call.args:
                    if isinstance(arg, ast.Constant) and arg.value == "PASS":
                        self.violations.append({
                            "file": file_path.name,
                            "line": fn.lineno,
                            "test": fn.name,
                            "rule": "LINT-01-DUMMY-FACADE",
                            "msg": f"Test '{fn.name}' has no control flow and unconditionally records PASS."
                        })

        # Check 2: 'Contract verified' or fallback PASS
        for call in record_calls:
            status = None
            msg = ""
            for arg in call.args:
                if isinstance(arg, ast.Constant):
                    if arg.value in ("PASS", "FAIL", "SKIP"):
                        status = arg.value
                    elif isinstance(arg.value, str):
                        msg += arg.value + " "
                elif isinstance(arg, ast.JoinedStr):
                    for val in arg.values:
                        if isinstance(val, ast.Constant) and isinstance(val.value, str):
                            msg += val.value + " "
            if status == "PASS" and "contract verified" in msg.lower():
                self.violations.append({
                    "file": file_path.name,
                    "line": call.lineno,
                    "test": fn.name,
                    "rule": "LINT-02-CONTRACT-VERIFIED-PASS",
                    "msg": f"Test '{fn.name}' records PASS with 'Contract verified': {msg.strip()}"
                })

        # Check 3: Only PASS statically possible (no FAIL and no SKIP)
        statuses = set()
        for call in record_calls:
            for arg in call.args:
                if isinstance(arg, ast.Constant) and arg.value in ("PASS", "FAIL", "SKIP"):
                    statuses.add(arg.value)

        dynamic_status = any(
            isinstance(call.args[2] if len(call.args) > 2 else None, ast.Name) or
            isinstance(call.args[3] if len(call.args) > 3 else None, ast.Name)
            for call in record_calls
        )

        if "PASS" in statuses and "FAIL" not in statuses and "SKIP" not in statuses and not dynamic_status:
            if not any(v["test"] == fn.name and v["rule"] == "LINT-01-DUMMY-FACADE" for v in self.violations):
                self.violations.append({
                    "file": file_path.name,
                    "line": fn.lineno,
                    "test": fn.name,
                    "rule": "LINT-03-NO-FAIL-PATH",
                    "msg": f"Test '{fn.name}' has no failure or skip branch (only literal PASS recorded)."
                })


def main():
    guard = ASTTestIntegrityGuard()
    violation_count = guard.scan_all()
    if violation_count > 0:
        print(f"\033[1m\033[31m[AST INTEGRITY GUARD] DETECTED {violation_count} VIOLATIONS:\033[0m")
        for v in guard.violations:
            print(f"  \033[31m✖\033[0m [{v['rule']}] {v['file']}:{v['line']} ({v['test']}): {v['msg']}")
        sys.exit(1)
    else:
        print("\033[1m\033[32m✔ [AST INTEGRITY GUARD] Zero dummy facades, zero fallback PASS branches detected.\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()
