#!/usr/bin/env python3
"""Build a symlink-only local HTTP view from a user-supplied UnityCache.

No game data is copied into this repository.
"""

from pathlib import Path
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("shared", type=Path, help="UnityCache/Shared directory")
    parser.add_argument("output", type=Path, help="local asset-repo directory")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    count = 0

    for entry in args.shared.iterdir():
        if not entry.is_dir():
            continue
        for version in entry.iterdir():
            data = version / "__data"
            if not data.is_file():
                continue

            target = args.output / f"{entry.name}.bundle"
            if target.exists() or target.is_symlink():
                target.unlink()
            target.symlink_to(data.resolve())
            count += 1
            break

    print(f"Mapped {count} archived cache entries into {args.output}")


if __name__ == "__main__":
    main()
