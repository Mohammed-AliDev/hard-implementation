"""Create an isolated standard-library Spec Kit fixture for real agent smoke tests."""
import argparse
from pathlib import Path
import subprocess

FILES = {
    "AGENTS.md": """# Fixture instructions
Use Python's standard library only. Work only in this repository. No network,
package installation, pushing, or outside modifications are needed. Run tests with
`python3 -m unittest discover -s tests -v`. Use the requested implementation skill.
This is a small feature; use its tier/applicability rules. Preserve user-notes.txt.
""",
    "user-notes.txt": "User-owned content: preserve this file exactly.\n",
    ".gitignore": "__pycache__/\n*.pyc\n",
    "specs/001-invoice/spec.md": """# Invoice amounts
Build a tiny local Python library in invoice.py.

`parse_amount(value)` accepts only strings of ASCII digits with optional one or
two fractional digits, such as '0', '12.3', and '12.34'. Return integer cents.
Reject empty strings, signs, whitespace, exponent notation, non-ASCII digits,
more than two decimal places, and non-string input with ValueError. Leading zeroes
are allowed. Do not use floating point for money.

`invoice_total(amounts, discount_cents=0)` parses a list of amount strings, sums
their cents, and subtracts a nonnegative integer discount no larger than the sum.
Reject bool or other non-int discounts with ValueError. Reject invalid amounts
using the same parsing rule. Empty list with zero discount returns zero.

Document the two functions and test the public behavior and rejection cases.
""",
    "specs/001-invoice/plan.md": """# Plan
One pure Python module, invoice.py, and unittest tests under tests/.
T001 is foundational. T002 depends on T001. T003 depends on T001 and T002.
T004 documents the verified public behavior. No external dependencies or services.
Use `python3 -m unittest discover -s tests -v` as the validation command.
""",
    "specs/001-invoice/tasks.md": """# Tasks
- [ ] T001 Implement parse_amount and focused validation tests.
- [ ] T002 Implement invoice_total using parse_amount with discount validation.
- [ ] T003 Add regression tests for valid totals and all invalid input boundaries.
- [ ] T004 Document usage in README.md and run the complete local test suite.
""",
    "invoice.py": '"""Invoice utilities to be implemented from the Spec."""\n',
    "tests/test_baseline.py": "import unittest\n\nclass Baseline(unittest.TestCase):\n    def test_import(self):\n        import invoice\n",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    root = args.directory.resolve()
    if root.exists() and any(root.iterdir()):
        parser.error("Fixture directory must be empty or new")
    root.mkdir(parents=True, exist_ok=True)
    for name, content in FILES.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    subprocess.run(["git", "init", "-b", "feature/001-invoice", str(root)], check=True)
    for key, value in (("user.name", "Smoke Test"), ("user.email", "smoke@example.invalid")):
        subprocess.run(["git", "-C", str(root), "config", key, value], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "Fixture baseline"], check=True)
    print(root)


if __name__ == "__main__":
    main()
