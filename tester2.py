import time
from test_cases import test_cases

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

def run_tests(solution):
    names = list(test_cases.keys())
    names.sort()
    counter = 1
    for name in names:
        obj = test_cases[name]
        mat = obj["mat"]
        val = obj["val"]
        start_time = time.time()
        try:
            a = solution.submat(mat)
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
        except AssertionError as e:
            res = "❌"
            fail = e
        t, u = pretty_time(end_time - start_time)
        print(f"{res} ({counter}/{len(names)}) Solution {name}: {a}; took {round(t, 3)}{u}{fail}")
        counter += 1