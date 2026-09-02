#!/usr/bin/env python3
"""Command hook entrypoint for the shared Friday host runtime."""
from __future__ import annotations

import argparse
import json
import sys

from runtime import handle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=("claude", "codex"), required=True)
    args = parser.parse_args()
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        data = {}
    output = handle(args.host, data if isinstance(data, dict) else {})
    if output:
        print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
