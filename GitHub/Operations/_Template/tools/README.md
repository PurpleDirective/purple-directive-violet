# Tools Directory

## Purpose
This directory contains deterministic Python scripts that form the Execution layer (Layer 3) of the DOE Framework. Tools do the actual work — the AI agent orchestrates, but tools execute.

## Design Principles

**Deterministic only.** No LLM calls inside tools. Given the same input, a tool must always produce the same output. The AI agent handles judgment; tools handle computation.

**Input validation.** Every tool validates its inputs before executing. Fail fast with clear error messages rather than producing bad output silently.

**Structured I/O.** Tools accept structured input (JSON, command-line args) and return structured output (JSON to stdout). This makes them composable and auditable.

**Error handling.** Tools catch exceptions and return structured error responses rather than crashing. The orchestration layer needs to know what went wrong, not just that something failed.

## Creating a New Tool

1. Name it descriptively: `calculate_dosage.py`, `validate_schedule.py`, `parse_transcript.py`
2. Include a docstring explaining what the tool does, its inputs, and its outputs
3. Validate all inputs at the top of the script
4. Return JSON to stdout for structured results
5. Use exit code 0 for success, non-zero for failure
6. Log actions when they modify state

## MCP Compatibility
Tools may be wrapped as MCP tools for invocation by Violet or other agents. Design tools to be stateless where possible — accept all needed context as input rather than relying on ambient state.

## Template

```python
#!/usr/bin/env python3
"""[TOOL_NAME] — [One-line description]

Usage:
    python [tool_name].py <input_json>

Input:
    JSON object with fields:
    - field_1 (str): [description]
    - field_2 (int): [description]

Output:
    JSON object with fields:
    - status (str): "success" or "error"
    - result (dict): [description of result]
    - message (str): Human-readable summary
"""

import json
import sys


def validate_input(data: dict) -> None:
    """Validate input data. Raises ValueError on invalid input."""
    required_fields = ["field_1", "field_2"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")


def execute(data: dict) -> dict:
    """Main execution logic. Returns result dict."""
    # Tool logic here
    return {"status": "success", "result": {}, "message": "Done."}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No input provided."}))
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        validate_input(data)
        result = execute(data)
        print(json.dumps(result))
    except (json.JSONDecodeError, ValueError) as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Unexpected error: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
```
