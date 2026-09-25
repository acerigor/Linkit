#!/usr/bin/env python3
"""PreToolUse hook: block edits to .env / .env.local."""
import json
import os
import sys

PROTECTED = {".env", ".env.local"}

def target_path(tool_name: str, tool_input: dict) -> str | None:
    if tool_name in ("Edit", "Write", "NotebookEdit"):
        return tool_input.get("file_path") or tool_input.get("notebook_path")
    if tool_name == "MultiEdit":
        return tool_input.get("file_path")
    return None

def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}
    path = target_path(tool_name, tool_input)
    if not path:
        return 0

    basename = os.path.basename(path)
    if basename in PROTECTED:
        # Exit code 2 tells Claude Code to BLOCK the tool call and feed
        # stderr back to the model as the reason for the block.
        print(f"Blocked: {basename} is protected. Ask the user before editing.", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
