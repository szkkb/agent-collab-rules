#!/usr/bin/env python3
"""Read-only consistency checks for a portable agent-rules workspace.

Validates the rule document itself (size budget and required sections) and, when
run inside a Git checkout, that the tracked files match the reviewed manifest.
It performs no writes and does not inspect host-specific client configuration.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "## Work to completion",
    "## Shared workspace",
    "## Production and data",
    "## Project and skill maintenance",
    "## Git 与 GitHub 的归属边界",
)

# Keeps the rule file within a budget that several harnesses can load whole.
CHARACTER_LIMIT = 12000


def audit(root):
    source = root / "CLAUDE.md"
    checks = []

    def check(name, passed, detail):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    is_regular = source.is_file() and not source.is_symlink()
    check("canonical-is-regular-file", is_regular, str(source))
    content = source.read_text(encoding="utf-8") if source.is_file() else ""

    for section in REQUIRED_SECTIONS:
        check("section-present:" + section, section in content, section)

    check(
        "rule-size-within-budget",
        0 < len(content) < CHARACTER_LIMIT,
        {"characters": len(content), "limit": CHARACTER_LIMIT},
    )

    pointer = root / "AGENTS.md"
    pointer_text = pointer.read_text(encoding="utf-8") if pointer.is_file() else ""
    check(
        "agents-points-at-canonical",
        "CLAUDE.md" in pointer_text,
        str(pointer),
    )

    manifest = root / "TRACKED_FILES.txt"
    allowed = {line.strip() for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()} if manifest.is_file() else set()
    check("manifest-present", bool(allowed), str(manifest))

    if (root / ".git").exists():
        tracked = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            check=True,
        ).stdout.decode().split("\0")
        tracked = {p for p in tracked if p}
        check(
            "tracked-files-match-manifest",
            tracked == allowed,
            {"unexpected": sorted(tracked - allowed), "missing": sorted(allowed - tracked)},
        )
    else:
        check("tracked-files-match-manifest", True, "not a Git checkout; manifest check skipped")

    return {
        "source": str(source),
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "bytes": len(content.encode("utf-8")),
        "checks": checks,
        "scope": "Rule-file and manifest consistency only; it does not verify that any harness loaded or followed these rules.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="rules workspace root (default: the repository containing this script)")
    args = parser.parse_args(argv)
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(c["passed"] for c in result["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
