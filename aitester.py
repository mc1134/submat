"""Test runner imported and invoked by solution.py.

Required test_cases.py format:
    test_cases = {
        "case name": {"mat": [[1, 0], [1, 1]], "val": 3},
        ...
    }

Optional dictionaries supported in test_cases.py:
    invalid_matrix_dims_test_cases
    invalid_chars_test_cases

Each optional dictionary uses the same case format.
"""

from test_cases import test_cases


_OPTIONAL_CASE_GROUPS = (
    "invalid_matrix_dims_test_cases",
    "invalid_chars_test_cases",
)


def _validate_case(case_name, case):
    if not isinstance(case, dict):
        raise TypeError(f"{case_name!r} must be a dictionary")

    if "mat" not in case or "val" not in case:
        raise KeyError(f"{case_name!r} must contain 'mat' and 'val' keys")


def _run_case(solution, group_name, case_name, case):
    qualified_name = f"{group_name}/{case_name}"

    try:
        _validate_case(qualified_name, case)
        actual = solution.submat(case["mat"])
        expected = case["val"]

        if actual == expected:
            print(f"[PASS] {qualified_name}")
            return "PASS"

        print(
            f"[FAIL] {qualified_name}: "
            f"expected {expected!r}, got {actual!r}"
        )
        return "FAIL"

    except Exception as exc:
        print(
            f"[ERROR] {qualified_name}: "
            f"{type(exc).__name__}: {exc}"
        )
        return "ERROR"


def _run_group(solution, group_name, cases):
    if not isinstance(cases, dict):
        raise TypeError(f"{group_name} must be a dictionary")

    results = []
    for case_name, case in cases.items():
        results.append(_run_case(solution, group_name, case_name, case))
    return results


def run_tests(solution):
    """Run the test cases against an already-created Solution instance.

    This function is intentionally the public entry point because solution.py
    creates Solution and calls tester.run_tests(solution).

    Returns True when every executed test passes; otherwise returns False.
    """
    all_results = []

    all_results.extend(_run_group(solution, "test_cases", test_cases))

    current_module = globals()
    for group_name in _OPTIONAL_CASE_GROUPS:
        cases = current_module.get(group_name)
        if cases is not None:
            all_results.extend(_run_group(solution, group_name, cases))

    passed = all_results.count("PASS")
    failed = all_results.count("FAIL")
    errors = all_results.count("ERROR")

    print("\nTest summary")
    print(f"  Total:  {len(all_results)}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Errors: {errors}")

    return failed == 0 and errors == 0


# Import optional case dictionaries, if they exist, without requiring them.
try:
    from test_cases import invalid_matrix_dims_test_cases
except ImportError:
    invalid_matrix_dims_test_cases = None

try:
    from test_cases import invalid_chars_test_cases
except ImportError:
    invalid_chars_test_cases = None
