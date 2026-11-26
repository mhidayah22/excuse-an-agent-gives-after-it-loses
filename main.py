# The Excuse an Agent Gives After It Loses — entry program
#
# Writes the one-line entry (145 characters) to entry.txt inside
# MAKEFUN_OUTPUT_DIR first, then /output, then a local fallback.

import os
import sys

ENTRY = (
    "You told me to be funny, not to win. I followed instructions perfectly. "
    "If you wanted a trophy, you should have specified 'trophy' in the prompt."
)


def resolve_output_dir():
    """Honour MAKEFUN_OUTPUT_DIR first, then /output, then a local fallback."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def main():
    line = ENTRY
    if not line or "\n" in line or "\r" in line:
        print("error: entry must be exactly one line", file=sys.stderr)
        return 1
    if line != line.strip() or "  " in line:
        print("error: entry has leading/trailing or double whitespace",
              file=sys.stderr)
        return 1
    if len(line) > 200:
        print(f"error: entry is {len(line)} characters, over the 200 limit",
              file=sys.stderr)
        return 1
    # Strict UTF-8 round-trip: the written bytes must decode back exactly.
    encoded = line.encode("utf-8")
    if encoded.decode("utf-8") != line:
        print("error: entry is not a clean UTF-8 round-trip", file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(encoded)
    with open(out_path, "rb") as f:
        if f.read() != encoded:
            print("error: written entry.txt does not match", file=sys.stderr)
            return 1
    print(f"wrote {len(line)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
