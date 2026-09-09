import time
import test_cases as TC
from unittest.mock import MagicMock, PropertyMock, patch

def pretty_time(t):
    table = {
        0: "s",
        -1: "ms",
        -2: "us",
        -3: "ns",
        -4: "ps"
    }
    mult = 0
    if t <= 10**-12:
        return t, "s"
    if t < 1:
        while t < 1:
            mult -= 1
            t *= 10**3
    return t, table[mult]

class TestInst:
    def __init__(self, solution, test_cases, test_id):
        self.solution = solution
        self.status = "NA"
        self.test_cases = test_cases
        self.test_id = test_id

    def run_tests(self):
        print(f"===== Running tests ===== {self.test_id} =====")
        names = list(self.test_cases.keys())
        names.sort()
        counter = 1
        run_result = []
        for name in names:
            obj = self.test_cases[name]
            mat = obj["mat"]
            val = obj["val"]
            start_time = time.time()
            try:
                a = self.solution.submat(mat)
            except Exception as e:
                end_time = time.time()
                t, u = pretty_time(end_time - start_time)
                print(f"❗ ({counter}/{len(names)}) Solution {name} ERROR (took {round(t, 3)}{u}): {e}")
                counter += 1
                continue
            end_time = time.time()
            res = "✔️"
            fail = ""
            try:
                assert a == val, f"\n\tExpected {val} but got {a}"
                run_result += ["PASS"]
            except AssertionError as e:
                res = "❌"
                fail = e
                run_result += ["FAIL"]
                self.status = "FAIL"
            t, u = pretty_time(end_time - start_time)
            print(f"{res} ({counter}/{len(names)}) Solution {name}: {a}; took {round(t, 3)}{u}{fail}")
            counter += 1
        return run_result

    def get_test_list(self):
        return self.test_cases
    def set_test_list(self, new_list) -> None:
        self.test_cases = new_list

    def get_algo(self):
        if self.solution:
            raise Exception("TestInst tried to get algo")
        return None

def make_inst(solution, test_cases, TEST_ID = "NA"):
    inst = TestInst.__new__(TestInst)
    inst.get_test_list = MagicMock(return_value = test_cases)
    type(inst).get_algo = PropertyMock(return_value = solution.submat)
    inst.__init__(
        solution,
        test_cases,
        TEST_ID
    )
    inst.status = "PASS"
    return inst

class TestAlgorithm:
    def __init__(self):
        self.solution = None

    def test_pass_all_matrix_tests(self):
        inst = make_inst(self.solution,
                         TC.test_cases,
                         "PASS Matrix Tests")
        results = inst.run_tests()
        assert inst.status == "PASS"
        assert all([i == "PASS" for i in results])

    def test_fail_when_matrix_not_well_formed(self):
        inst = make_inst(self.solution,
                         {i: j for i, j in TC.f_test_cases.items() if i[0] == "X"},
                         "FAIL matrix not well-formed")
        results = inst.run_tests()
        assert inst.status == "FAIL"
        assert all([i == "FAIL" for i in results])

    def test_fail_when_matrix_has_non_01(self):
        inst = make_inst(self.solution,
                         {i: j for i, j in TC.f_test_cases.items() if i[0] == "Y"},
                         "FAIL matrix illegal chars")
        results = inst.run_tests()
        assert inst.status == "FAIL"
        assert all([i == "FAIL" for i in results])

def run_tests(solution):
    t = TestAlgorithm()
    t.solution = solution
    t.test_pass_all_matrix_tests()
    t.test_fail_when_matrix_not_well_formed()
    t.test_fail_when_matrix_has_non_01()