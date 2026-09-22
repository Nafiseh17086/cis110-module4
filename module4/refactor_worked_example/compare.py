"""Run the SAME tests against all three versions - the step you must never skip.

    python compare.py

A refactor must not change what the code does. If any version gives a different
answer from before.py, the refactor is wrong, however much nicer it looks.
"""
import before
import suggestion
import after

TESTS = [
    [88, 64, 95, 71, 59],     # the example from the video
    [70, 70, 70],             # boundary: exactly 70 is NOT below 70
    [69],                     # a single score
    [50, 40, 30],             # every score below 70
    [100, 99, 100],           # the highest appears twice
]

all_same = True
for scores in TESTS:
    want = before.class_report(scores)
    for name, module in [("suggestion", suggestion), ("after", after)]:
        got = module.class_report(scores)
        same = got == want
        all_same = all_same and same
        print(f"{'SAME     ' if same else 'DIFFERENT'} {name:<10} {scores}  ->  {got}")

print()
print("All versions agree." if all_same else "At least one version changed the behaviour!")

# One thing NONE of the versions handle: an empty list.
for name, module in [("before", before), ("suggestion", suggestion), ("after", after)]:
    try:
        module.class_report([])
    except ZeroDivisionError:
        print(f"{name:<10} crashes on an empty list (ZeroDivisionError).")
