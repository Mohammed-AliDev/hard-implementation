"""Preview GitHub About changes; --apply writes them after authorized publication."""
import argparse
import json
import subprocess

from check_consistency import facts, github_issues, github_metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply description and topics to the configured repository")
    args = parser.parse_args()
    data = facts()
    desired = {"description": data["description"], "topics": data["topics"]}
    if not args.apply:
        print(json.dumps(desired, indent=2))
        print("Preview only. Use --apply when updating GitHub is authorized.")
        return 0
    for method, suffix, payload in (
        ("PATCH", "", {"description": desired["description"]}),
        ("PUT", "/topics", {"names": desired["topics"]}),
    ):
        result = subprocess.run(["gh", "api", "--method", method, f"repos/{data['repository']}{suffix}",
                                 "--input", "-"], input=json.dumps(payload), text=True,
                                capture_output=True, timeout=30)
        if result.returncode:
            raise SystemExit(f"GitHub {method} metadata update failed; verify authentication/network access before retrying")
    errors = github_issues(data, github_metadata(data))
    if errors:
        raise SystemExit("\n".join(errors))
    print("GitHub About description and topics updated and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
