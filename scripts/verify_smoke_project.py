"""Independently check observable outcomes of the live-agent fixture."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess


def verify(root):
    spec = importlib.util.spec_from_file_location("fixture_invoice", root / "invoice.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = 0
    for value, expected in (("0", 0), ("12.3", 1230), ("12.34", 1234),
                            ("000.01", 1), ("9999999999999999.99", 999999999999999999)):
        actual = module.parse_amount(value)
        assert type(actual) is int and actual == expected, (value, actual)
        cases += 1
    for value in ("", " 1", "1 ", "+1", "-1", "1e2", "1.234", "١٢", "１２", ".5", "12.",
                  "1\n", 1, 1.0, None, True):
        try:
            module.parse_amount(value)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted invalid amount: {value!r}")
        cases += 1
    for amounts, discount, expected in (([], 0, 0), (["1.20", "2.30"], 25, 325),
                                         (["1"], 100, 0), (["00.01", "0.09"], 0, 10)):
        actual = module.invoice_total(amounts, discount)
        assert type(actual) is int and actual == expected, (amounts, discount, actual)
        cases += 1
    for amounts, discount in ((["1"], -1), (["1"], 101), (["1"], True),
                               (["1"], 1.5), (["1"], "1"), (["bad"], 0), ([], 1)):
        try:
            module.invoice_total(amounts, discount)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted invalid invoice: {amounts!r}, {discount!r}")
        cases += 1
    assert (root / "user-notes.txt").read_text() == "User-owned content: preserve this file exactly.\n"
    tasks = (root / "specs/001-invoice/tasks.md").read_text()
    for task_id in ("T001", "T002", "T003", "T004"):
        assert f"[x] {task_id}" in tasks or f"[X] {task_id}" in tasks, task_id
    assert (root / "specs/001-invoice/evidence/implementation-state.md").is_file()
    assert (root / "README.md").is_file()
    subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, check=True)
    subprocess.run(["git", "diff", "--check"], cwd=root, check=True)
    print(json.dumps({"independent_behavior_cases": cases, "all_four_tasks_checked": True,
                      "user_file_preserved": True, "checkpoint_exists": True}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    verify(parser.parse_args().directory.resolve())
