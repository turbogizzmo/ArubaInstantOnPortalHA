#!/usr/bin/env python3
"""Reject common forms of private deployment data in tracked text files."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico"}
RULES = {
    "Home Assistant device-registry path": re.compile(
        rb"/config/devices/device/[0-9a-f]{32}\b", re.IGNORECASE
    ),
    "MAC address": re.compile(
        rb"\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b", re.IGNORECASE
    ),
    "private IPv4 address": re.compile(
        rb"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
        rb"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
    ),
    "email address": re.compile(
        rb"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE
    ),
}


def tracked_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    )
    return [
        ROOT / item.decode()
        for item in output.split(b"\0")
        if item and Path(item.decode()).suffix.lower() not in SKIP_SUFFIXES
    ]


def main() -> int:
    findings: list[str] = []
    for path in tracked_files():
        data = path.read_bytes()
        for rule_name, pattern in RULES.items():
            for match in pattern.finditer(data):
                line = data.count(b"\n", 0, match.start()) + 1
                findings.append(
                    f"{path.relative_to(ROOT)}:{line}: {rule_name}"
                )

    if findings:
        print("Privacy check failed. Replace deployment data with generic examples:")
        print("\n".join(findings))
        return 1

    print("Privacy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
