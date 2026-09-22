"""
CIS 110 - environment check
===========================

Run this from the lab folder:

    python setup/verify_environment.py

It checks that everything Lab 4 needs is installed, and tells you exactly
what to fix if something is missing. It does not change anything on your
computer.

If a check says NOT YET and TROUBLESHOOTING.md does not solve it, copy
everything this script prints and post it to the Q&A discussion.
"""

import importlib.util
import os
import platform
import sys
import tempfile

REQUIRED = (3, 12)
results = []


def check(passed, label, fix=""):
    results.append(passed)
    print(f"  {'PASS   ' if passed else 'NOT YET'}  {label}")
    if not passed and fix:
        for line in fix.splitlines():
            print(f"           {line}")


print("=" * 60)
print("  CIS 110 - environment check")
print("=" * 60)
print(f"  Operating system : {platform.system()} {platform.release()}")
print(f"  Python location  : {sys.executable}")
print()

version = sys.version_info
check(
    version >= REQUIRED,
    f"Python {version.major}.{version.minor}.{version.micro} (need {REQUIRED[0]}.{REQUIRED[1]} or later)",
    "Install the latest Python from https://www.python.org/downloads/\n"
    "See setup/TROUBLESHOOTING.md, section 1.",
)

check(
    importlib.util.find_spec("ipykernel") is not None,
    "ipykernel installed (lets VS Code run notebooks)",
    "Run:  python -m pip install ipykernel\n"
    "See setup/TROUBLESHOOTING.md, section 3.",
)

if importlib.util.find_spec("matplotlib") is None:
    print("  OPTIONAL matplotlib not installed - only needed for the optional chart cell.")
    print("           To add it:  python -m pip install matplotlib")
else:
    print("  PASS     matplotlib installed (optional chart cell)")

here = os.path.dirname(os.path.abspath(__file__))
lab_folder = os.path.dirname(here)
check(
    os.path.exists(os.path.join(lab_folder, "lab4_text_analyzer.ipynb")),
    "Lab 4 notebook found",
    "Run this script from inside the unzipped lab folder.",
)

try:
    with tempfile.NamedTemporaryFile(dir=lab_folder, delete=True):
        pass
    can_write = True
except OSError:
    can_write = False
check(
    can_write,
    "Can save files in the lab folder",
    "Move the lab folder somewhere you own, such as Documents,\n"
    "and do not work from inside the zip file itself.",
)

print()
print("-" * 60)
if all(results):
    print("  All set. Open lab4_text_analyzer.ipynb and start Lab 4.")
else:
    print(f"  {results.count(False)} thing(s) to fix. See setup/TROUBLESHOOTING.md.")
print("-" * 60)
sys.exit(0 if all(results) else 1)
