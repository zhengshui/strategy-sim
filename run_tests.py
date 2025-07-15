#!/usr/bin/env python3
"""
Test runner for StrategySim AI.

Comprehensive test suite runner with reporting and coverage analysis.
"""

import os
import sys
import pytest
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


def run_tests(
    test_path: str = "tests/",
    verbose: bool = True,
    coverage: bool = True,
    markers: Optional[List[str]] = None,
    parallel: bool = True
) -> int:
    """
    Run the test suite with specified options.
    
    Args:
        test_path: Path to test directory
        verbose: Enable verbose output
        coverage: Enable coverage reporting
        markers: Test markers to run (e.g., ['unit', 'integration'])
        parallel: Enable parallel test execution
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test path
    cmd.append(test_path)
    
    # Add verbose flag
    if verbose:
        cmd.append("-v")
    
    # Add coverage options
    if coverage:
        cmd.extend([
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80"
        ])
    
    # Add parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add markers
    if markers:
        for marker in markers:
            cmd.extend(["-m", marker])
    
    # Add additional pytest options
    cmd.extend([
        "--tb=short",
        "--strict-markers",
        "--disable-warnings"
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Run tests
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def run_specific_test_suites() -> Dict[str, int]:
    """
    Run specific test suites and return results.
    
    Returns:
        Dictionary mapping test suite names to exit codes
    """
    results = {}
    
    # Unit tests
    print("\n" + "="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)
    results["unit"] = run_tests(
        test_path="tests/test_models/ tests/test_agents/test_base_agent.py tests/test_agents/test_investor_agent.py tests/test_tools/",
        markers=["unit"],
        coverage=False
    )
    
    # Integration tests
    print("\n" + "="*60)
    print("RUNNING INTEGRATION TESTS")
    print("="*60)
    results["integration"] = run_tests(
        test_path="tests/test_integration/",
        markers=["integration"],
        coverage=False
    )
    
    # Tool tests
    print("\n" + "="*60)
    print("RUNNING TOOL TESTS")
    print("="*60)
    results["tools"] = run_tests(
        test_path="tests/test_tools/",
        coverage=False
    )
    
    # Utility tests
    print("\n" + "="*60)
    print("RUNNING UTILITY TESTS")
    print("="*60)
    results["utils"] = run_tests(
        test_path="tests/test_utils/",
        coverage=False
    )
    
    return results


def run_all_tests_with_coverage() -> int:
    """
    Run all tests with coverage reporting.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    print("\n" + "="*60)
    print("RUNNING FULL TEST SUITE WITH COVERAGE")
    print("="*60)
    
    return run_tests(
        test_path="tests/",
        verbose=True,
        coverage=True,
        parallel=True
    )


def check_test_requirements() -> bool:
    """
    Check if test requirements are installed.
    
    Returns:
        True if requirements are satisfied, False otherwise
    """
    required_packages = [
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "pytest-asyncio"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True


def print_test_summary(results: Dict[str, int]) -> None:
    """
    Print test results summary.
    
    Args:
        results: Dictionary mapping test suite names to exit codes
    """
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    total_suites = len(results)
    passed_suites = sum(1 for code in results.values() if code == 0)
    failed_suites = total_suites - passed_suites
    
    for suite_name, exit_code in results.items():
        status = "PASSED" if exit_code == 0 else "FAILED"
        print(f"{suite_name.upper():<15} {status}")
    
    print("-" * 60)
    print(f"Total suites: {total_suites}")
    print(f"Passed: {passed_suites}")
    print(f"Failed: {failed_suites}")
    
    if failed_suites == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n❌ {failed_suites} test suite(s) failed")


def generate_test_report() -> None:
    """Generate comprehensive test report."""
    print("\n" + "="*60)
    print("GENERATING TEST REPORT")
    print("="*60)
    
    # Run pytest with JUnit XML output
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "--junitxml=test_results.xml",
        "--cov=src",
        "--cov-report=xml",
        "--cov-report=html",
        "-v"
    ]
    
    try:
        subprocess.run(cmd, check=False)
        print("Test report generated:")
        print("  - test_results.xml (JUnit XML)")
        print("  - htmlcov/index.html (Coverage HTML)")
        print("  - coverage.xml (Coverage XML)")
    except Exception as e:
        print(f"Error generating test report: {e}")


def main():
    """Main test runner function."""
    print("StrategySim AI Test Runner")
    print("="*60)
    
    # Check requirements
    if not check_test_requirements():
        sys.exit(1)
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print("""
Usage: python run_tests.py [OPTIONS]

Options:
  --unit          Run only unit tests
  --integration   Run only integration tests  
  --tools         Run only tool tests
  --utils         Run only utility tests
  --coverage      Run all tests with coverage
  --report        Generate comprehensive test report
  --specific      Run specific test suites separately
  --help, -h      Show this help message

Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py --unit            # Run only unit tests
  python run_tests.py --coverage        # Run with coverage
  python run_tests.py --report          # Generate test report
  python run_tests.py --specific        # Run suites separately
        """)
        return
    
    # Execute based on arguments
    if "--unit" in args:
        exit_code = run_tests(
            test_path="tests/test_models/ tests/test_agents/test_base_agent.py tests/test_agents/test_investor_agent.py",
            markers=["unit"]
        )
    elif "--integration" in args:
        exit_code = run_tests(
            test_path="tests/test_integration/",
            markers=["integration"]
        )
    elif "--tools" in args:
        exit_code = run_tests(test_path="tests/test_tools/")
    elif "--utils" in args:
        exit_code = run_tests(test_path="tests/test_utils/")
    elif "--coverage" in args:
        exit_code = run_all_tests_with_coverage()
    elif "--report" in args:
        generate_test_report()
        exit_code = 0
    elif "--specific" in args:
        results = run_specific_test_suites()
        print_test_summary(results)
        exit_code = 0 if all(code == 0 for code in results.values()) else 1
    else:
        # Run all tests by default
        exit_code = run_all_tests_with_coverage()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()