"""Test runner invoked by solution.py.

Required in test_cases.py:
    test_cases = {
        "case name": {"mat": [[1, 0], [1, 1]], "val": 3},
        ...
    }

Optional test-case dictionaries:
    invalid_matrix_dims_test_cases
    invalid_chars_test_cases

Cases in either optional dictionary must include an "error" key containing a
list of expected exception classes. An empty list means no exception is
expected, so the returned value is compared with "val".
"""

import test_cases as cases_module

CASE_GROUP_NAMES = (
    "test_cases",
    "invalid_matrix_dims_test_cases",
    "invalid_chars_test_cases",
)

EXPECTED_ERROR_GROUPS = {
    "invalid_matrix_dims_test_cases",
    "invalid_chars_test_cases",
}

def _get_case_groups():
    """Return all defined, non-None test-case groups."""
    if not hasattr(cases_module, "test_cases"):
        raise AttributeError("test_cases.py must define 'test_cases'")

    groups = []
    for group_name in CASE_GROUP_NAMES:
        group = getattr(cases_module, group_name, None)
        if group is not None:
            if not isinstance(group, dict):
                raise TypeError(f"{group_name} must be a dictionary")
            groups.append((group_name, group))

    return groups

def _validate_case(case_name, case, expects_error):
    if not isinstance(case, dict):
        raise TypeError(f"{case_name!r} must be a dictionary")

    required_keys = {"mat", "val"}
    if expects_error:
        required_keys.add("error")

    missing_keys = required_keys.difference(case)
    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise KeyError(f"{case_name!r} is missing required key(s): {missing}")

    if expects_error:
        expected_errors = case["error"]
        if not isinstance(expected_errors, list):
            raise TypeError(
                f"{case_name!r}['error'] must be a list of exception classes"
            )

        for expected_error in expected_errors:
            if not isinstance(expected_error, type) or not issubclass(
                expected_error, Exception
            ):
                raise TypeError(
                    f"{case_name!r}['error'] must contain only exception classes"
                )

def _run_case(solution, group_name, case_name, case, test_number, total):
    qualified_name = f"{group_name}/{case_name}"
    expects_error = group_name in EXPECTED_ERROR_GROUPS

    try:
        _validate_case(qualified_name, case, expects_error)
    except Exception as exc:
        print(
            f"[{test_number}/{total}] [ERROR] {qualified_name}: "
            f"invalid test definition - {type(exc).__name__}: {exc}"
        )
        return "ERROR"

    expected_errors = case.get("error", []) if expects_error else []

    try:
        actual = solution.submat(case["mat"])
    except Exception as exc:
        if expected_errors:
            # Compare the concrete exception type to make the result easier to
            # explain in the test output.
            if type(exc) in expected_errors:
                expected_names = ", ".join(
                    expected_error.__name__ for expected_error in expected_errors
                )
                print(
                    f"[{test_number}/{total}] [PASS] {qualified_name}: "
                    f"raised expected exception ({expected_names})"
                )
                return "PASS"

            expected_names = ", ".join(
                expected_error.__name__ for expected_error in expected_errors
            )
            print(
                f"[{test_number}/{total}] [FAIL] {qualified_name}: "
                f"expected one of ({expected_names}), got {type(exc).__name__}"
            )
            return "FAIL"

        print(
            f"[{test_number}/{total}] [ERROR] {qualified_name}: "
            f"unexpected {type(exc).__name__}: {exc}"
        )
        return "ERROR"

    if expected_errors:
        expected_names = ", ".join(
            expected_error.__name__ for expected_error in expected_errors
        )
        print(
            f"[{test_number}/{total}] [FAIL] {qualified_name}: "
            f"expected one of ({expected_names}), but no exception was raised"
        )
        return "FAIL"

    expected = case["val"]
    if actual == expected:
        print(
            f"[{test_number}/{total}] [PASS] {qualified_name}: "
            f"returned {actual!r}"
        )
        return "PASS"

    print(
        f"[{test_number}/{total}] [FAIL] {qualified_name}: "
        f"expected {expected!r}, got {actual!r}"
    )
    return "FAIL"

def run_tests(solution):
    """Run all available tests against the supplied Solution instance.

    Called by solution.py as:
        solution = Solution()
        tester.run_tests(solution)

    Returns True only when every test passes.
    """
    groups = _get_case_groups()
    total = sum(len(group) for _, group in groups)
    results = []
    test_number = 0

    for group_name, group in groups:
        for case_name, case in group.items():
            test_number += 1
            results.append(
                _run_case(
                    solution,
                    group_name,
                    case_name,
                    case,
                    test_number,
                    total,
                )
            )

    passed = results.count("PASS")
    failed = results.count("FAIL")
    errors = results.count("ERROR")

    print("\nTest summary")
    print(f"  Total:  {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Errors: {errors}")

    return failed == 0 and errors == 0