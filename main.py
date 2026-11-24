#!/usr/bin/env python3
"""Write the judged one-word Wi-Fi description to /output/entry.txt.

The artifact is exactly one word, 1-20 UTF-8 characters, with no trailing
newline. It is created atomically: a temp file in /output is written, given
mode 0644, and renamed over the artifact with os.replace.
"""

import os
import stat
import tempfile

ENTRY = "Catfish"
ARTIFACT = "/output/entry.txt"
MAX_CHARS = 20


def validate(text: str) -> bytes:
    """Return the exact artifact bytes, or refuse an entry the gate would refuse."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip() or any(ch.isspace() for ch in text):
        raise ValueError("entry must be one non-whitespace word")
    data = text.encode("utf-8")
    if len(data) != len(text):
        raise ValueError("entry must be ASCII-clean so every reader gets it instantly")
    if data.decode("utf-8") != text:
        raise ValueError("entry is not valid UTF-8")
    return data


def write_atomic(path: str, data: bytes) -> None:
    """Publish data at path with mode 0644, leaving no temp file behind."""
    out_dir = os.path.dirname(path)
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=out_dir)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # The grader refuses a mode-600 artifact: fix permissions BEFORE replace.
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
    mode = stat.S_IMODE(os.stat(path).st_mode)
    if mode != 0o644:
        raise RuntimeError(f"artifact mode is {mode:o}, expected 644")


def main() -> None:
    data = validate(ENTRY)
    write_atomic(ARTIFACT, data)


if __name__ == "__main__":
    main()
