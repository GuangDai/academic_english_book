#!/usr/bin/env python3
"""Unified Automated Test Runner for Academic English Textbook & Workbook.

Executes 4 tiers of opaque-box, requirement-driven tests:
- Tier 1: Feature Coverage (Features 1-16)
- Tier 2: Boundary & Corner Cases
- Tier 3: Cross-Feature Combinations & Pairwise Interactions
- Tier 4: Real-World Acceptance Scenarios
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Ensure tests directory is on path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from test_helpers import TestResult
from tier1_feature_tests import Tier1FeatureTests
from tier2_boundary_tests import Tier2BoundaryTests
from tier3_interaction_tests import Tier3InteractionTests
from tier4_application_tests import Tier4ApplicationTests

# ANSI Terminal Colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
DIM = "\033[2m"


def print_banner():
    banner = f"""{BOLD}{CYAN}
================================================================================
   ACADEMIC ENGLISH TEXTBOOK & WORKBOOK — E2E TEST SUITE RUNNER
   4-Tier Opaque-Box Requirement Verification Engine
================================================================================{RESET}"""
    print(banner)


def format_status(status: str) -> str:
    if status == "PASS":
        return f"{GREEN}{BOLD}PASS{RESET}"
    elif status == "FAIL":
        return f"{RED}{BOLD}FAIL{RESET}"
    elif status == "SKIP":
        return f"{YELLOW}{BOLD}SKIP{RESET}"
    return status


class TestRunner:
    """Orchestrates test suite execution, tier selection, and report generation."""

    def __init__(self, tiers: Optional[List[int]] = None, milestone: str = "ALL",
                 verbose: bool = False, json_output: bool = False):
        self.selected_tiers = tiers or [1, 2, 3, 4]
        self.milestone = milestone
        self.verbose = verbose
        self.json_output = json_output
        self.all_results: List[TestResult] = []

    def run(self) -> int:
        start_total = time.time()
        if not self.json_output:
            print_banner()
            print(f"{BOLD}Configuration:{RESET} Tiers={self.selected_tiers} | Milestone={self.milestone} | Verbose={self.verbose}\n")

        # Stage 0: AST Test Integrity Guard
        from ast_test_guard import ASTTestIntegrityGuard
        guard = ASTTestIntegrityGuard(CURRENT_DIR)
        v_count = guard.scan_all()
        if v_count > 0:
            print(f"\n{BOLD}{RED}CRITICAL: AST Test Integrity Guard detected {v_count} violations!{RESET}")
            for v in guard.violations:
                print(f"  {RED}✖ [{v['rule']}]{RESET} {v['file']}:{v['line']} ({v['test']}): {v['msg']}")
            return 1

        # Execute selected tiers
        if 1 in self.selected_tiers:
            if not self.json_output:
                print(f"{BOLD}{MAGENTA}>>> Running Tier 1: Feature Coverage (Features 1-16)...{RESET}")
            t1_suite = Tier1FeatureTests()
            t1_results = t1_suite.run_all(self.milestone)
            self._process_tier_results(1, t1_results)

        if 2 in self.selected_tiers:
            if not self.json_output:
                print(f"\n{BOLD}{MAGENTA}>>> Running Tier 2: Boundary & Corner Cases...{RESET}")
            t2_suite = Tier2BoundaryTests()
            t2_results = t2_suite.run_all(self.milestone)
            self._process_tier_results(2, t2_results)

        if 3 in self.selected_tiers:
            if not self.json_output:
                print(f"\n{BOLD}{MAGENTA}>>> Running Tier 3: Cross-Feature Interactions...{RESET}")
            t3_suite = Tier3InteractionTests()
            t3_results = t3_suite.run_all(self.milestone)
            self._process_tier_results(3, t3_results)

        if 4 in self.selected_tiers:
            if not self.json_output:
                print(f"\n{BOLD}{MAGENTA}>>> Running Tier 4: Real-World Acceptance Scenarios...{RESET}")
            t4_suite = Tier4ApplicationTests()
            t4_results = t4_suite.run_all(self.milestone)
            self._process_tier_results(4, t4_results)

        total_duration = time.time() - start_total

        # Reporting
        if self.json_output:
            self._print_json_summary(total_duration)
        else:
            self._print_human_summary(total_duration)

        # Exit code contract: 0 if 0 fails, 1 otherwise
        failed_count = sum(1 for r in self.all_results if r.status == "FAIL")
        return 0 if failed_count == 0 else 1

    def _process_tier_results(self, tier: int, results: List[TestResult]):
        self.all_results.extend(results)
        if not self.json_output:
            tier_passes = sum(1 for r in results if r.status == "PASS")
            tier_fails = sum(1 for r in results if r.status == "FAIL")
            tier_skips = sum(1 for r in results if r.status == "SKIP")
            
            for r in results:
                if self.verbose or r.status == "FAIL":
                    status_str = format_status(r.status)
                    duration_str = f"{DIM}({r.duration:.2f}s){RESET}"
                    feat_tag = f"[{r.feature_id}] " if r.feature_id else ""
                    print(f"  {status_str} {feat_tag}{r.test_id}: {r.name} {duration_str}")
                    if r.message and (r.status == "FAIL" or self.verbose):
                        print(f"       {DIM}└─ {r.message}{RESET}")

            print(f"  {BOLD}Tier {tier} Summary:{RESET} {GREEN}{tier_passes} passed{RESET}, "
                  f"{RED}{tier_fails} failed{RESET}, {YELLOW}{tier_skips} skipped{RESET} "
                  f"({len(results)} total)")

    def _print_human_summary(self, total_duration: float):
        total_tests = len(self.all_results)
        passed = sum(1 for r in self.all_results if r.status == "PASS")
        failed = sum(1 for r in self.all_results if r.status == "FAIL")
        skipped = sum(1 for r in self.all_results if r.status == "SKIP")

        print(f"\n{BOLD}{CYAN}================================================================================{RESET}")
        print(f"{BOLD}{WHITE}                           TEST EXECUTION SUMMARY{RESET}")
        print(f"{BOLD}{CYAN}================================================================================{RESET}")

        tier_names = {
            1: "Tier 1: Feature Coverage (Features 1-16)",
            2: "Tier 2: Boundary & Corner Cases",
            3: "Tier 3: Cross-Feature Interactions",
            4: "Tier 4: Acceptance Scenarios"
        }

        print(f"{BOLD}{'Tier / Category':<45} | {'Total':<6} | {'Pass':<6} | {'Fail':<6} | {'Skip':<6}{RESET}")
        print("-" * 78)

        for t in self.selected_tiers:
            t_res = [r for r in self.all_results if r.tier == t]
            t_tot = len(t_res)
            t_p = sum(1 for r in t_res if r.status == "PASS")
            t_f = sum(1 for r in t_res if r.status == "FAIL")
            t_s = sum(1 for r in t_res if r.status == "SKIP")
            name = tier_names.get(t, f"Tier {t}")
            print(f"{name:<45} | {t_tot:<6} | {t_p:<6} | {t_f:<6} | {t_s:<6}")

        print("-" * 78)
        print(f"{BOLD}{'TOTAL':<45} | {total_tests:<6} | {passed:<6} | {failed:<6} | {skipped:<6}{RESET}")
        print(f"{BOLD}{CYAN}================================================================================{RESET}")

        if failed > 0:
            print(f"\n{BOLD}{RED}FAILED TESTS DETECTED ({failed}):{RESET}")
            for r in self.all_results:
                if r.status == "FAIL":
                    print(f"  {RED}✖{RESET} [{r.test_id}] {r.name}: {r.message}")
            print(f"\n{BOLD}{RED}>>> RESULT: TEST SUITE FAILED (Total time: {total_duration:.2f}s){RESET}\n")
        else:
            print(f"\n{BOLD}{GREEN}✔ 100% PASS RATE — ALL REQUIREMENTS & INTERFACE CONTRACTS VERIFIED{RESET}")
            print(f"{DIM}Total execution time: {total_duration:.2f}s across {total_tests} test cases.{RESET}\n")

    def _print_json_summary(self, total_duration: float):
        summary = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'duration_seconds': round(total_duration, 2),
            'total_tests': len(self.all_results),
            'passed': sum(1 for r in self.all_results if r.status == "PASS"),
            'failed': sum(1 for r in self.all_results if r.status == "FAIL"),
            'skipped': sum(1 for r in self.all_results if r.status == "SKIP"),
            'tests': [r.to_dict() for r in self.all_results]
        }
        print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Academic English Book E2E Test Suite Runner")
    parser.add_argument("--tier", type=str, default=None,
                        help="Comma-separated tiers to run, e.g. '1,2' or '4' (default: all)")
    parser.add_argument("--milestone", type=str, default="ALL",
                        choices=["ALL", "M1", "M2", "M3", "M4", "M5"],
                        help="Filter assertions by milestone (default: ALL)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed per-test execution information")
    parser.add_argument("--json", action="store_true",
                        help="Output machine-readable JSON summary for CI/CD")

    args = parser.parse_args()

    selected_tiers = None
    if args.tier:
        selected_tiers = [int(t.strip()) for t in args.tier.split(",") if t.strip().isdigit()]

    runner = TestRunner(
        tiers=selected_tiers,
        milestone=args.milestone,
        verbose=args.verbose,
        json_output=args.json
    )
    exit_code = runner.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
