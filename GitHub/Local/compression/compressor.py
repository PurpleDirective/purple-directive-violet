"""
Purple Context Compressor — LLMLingua-2 Integration

Compresses agent profiles and context for injection into local models (Ollama).
Uses Microsoft's LLMLingua-2 for intelligent prompt compression that preserves
semantic meaning while reducing token count.

Usage:
    from compressor import compress_context

    compressed = compress_context(
        text="Full agent profile text...",
        ratio=0.5,          # Target 50% of original length
        force_tokens=["E.I.K.", "Violet", "Evolution"]  # Never remove these
    )
"""

import sys
from pathlib import Path
from typing import Optional


def compress_context(
    text: str,
    ratio: float = 0.33,
    force_tokens: Optional[list[str]] = None,
    use_llmlingua: bool = True,
) -> str:
    """
    Compress text using LLMLingua-2 or fallback to simple truncation.

    Args:
        text: The full text to compress.
        ratio: Target compression ratio (0.33 = keep ~33% of tokens). Default 3x compression.
        force_tokens: List of tokens/phrases that must be preserved in output.
        use_llmlingua: If True, attempt LLMLingua-2. If False or unavailable, use fallback.

    Returns:
        Compressed text string.
    """
    if not text or not text.strip():
        return text

    if use_llmlingua:
        try:
            return _compress_llmlingua(text, ratio, force_tokens)
        except ImportError:
            print(
                "[compressor] LLMLingua-2 not available. Install with: pip install llmlingua",
                file=sys.stderr,
            )
        except Exception as e:
            print(
                f"[compressor] LLMLingua-2 failed, using fallback: {e}",
                file=sys.stderr,
            )

    return _compress_fallback(text, ratio)


def _compress_llmlingua(
    text: str,
    ratio: float,
    force_tokens: Optional[list[str]] = None,
) -> str:
    """Compress using LLMLingua-2 (BERT-level encoder, fast)."""
    from llmlingua import PromptCompressor

    compressor = PromptCompressor(
        model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
        use_llmlingua2=True,
    )

    result = compressor.compress_prompt(
        text,
        rate=ratio,
        force_tokens=force_tokens or [],
        drop_consecutive=True,
    )

    return result["compressed_prompt"]


def _compress_fallback(text: str, ratio: float) -> str:
    """
    Simple fallback compression: preserve structure, remove verbose content.

    Strategy:
    1. Keep all headers (lines starting with #)
    2. Keep all bullet points and list items
    3. Keep lines with key markers (**, |, --, →)
    4. Trim remaining lines to fit ratio
    """
    lines = text.split("\n")
    priority_lines = []
    regular_lines = []

    for line in lines:
        stripped = line.strip()
        if (
            stripped.startswith("#")
            or stripped.startswith("- ")
            or stripped.startswith("* ")
            or stripped.startswith("|")
            or "**" in stripped
            or "→" in stripped
            or stripped.startswith("```")
            or stripped == ""
        ):
            priority_lines.append((len(priority_lines) + len(regular_lines), line))
        else:
            regular_lines.append((len(priority_lines) + len(regular_lines), line))

    target_lines = max(1, int(len(lines) * ratio))
    priority_count = len(priority_lines)

    if priority_count >= target_lines:
        # Even priority lines exceed budget — take first target_lines priority lines
        selected = sorted(priority_lines[:target_lines], key=lambda x: x[0])
    else:
        # Take all priority lines + fill remaining budget with regular lines
        remaining = target_lines - priority_count
        selected = sorted(
            priority_lines + regular_lines[:remaining], key=lambda x: x[0]
        )

    return "\n".join(line for _, line in selected)


def compress_file(
    filepath: str,
    ratio: float = 0.33,
    force_tokens: Optional[list[str]] = None,
    output_path: Optional[str] = None,
) -> str:
    """
    Compress a file and optionally write the result.

    Args:
        filepath: Path to the file to compress.
        ratio: Target compression ratio.
        force_tokens: Tokens to preserve.
        output_path: If provided, write compressed text here.

    Returns:
        Compressed text string.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    text = path.read_text(encoding="utf-8")
    compressed = compress_context(text, ratio, force_tokens)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(compressed, encoding="utf-8")

    return compressed


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 characters per token for English text."""
    return len(text) // 4


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Purple Context Compressor")
    parser.add_argument("file", help="Path to file to compress")
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.33,
        help="Compression ratio (default: 0.33 = 3x compression)",
    )
    parser.add_argument(
        "--output", "-o", help="Output file path (default: print to stdout)"
    )
    parser.add_argument(
        "--force-tokens",
        nargs="+",
        help="Tokens to preserve during compression",
    )
    parser.add_argument(
        "--no-llmlingua",
        action="store_true",
        help="Use fallback compression instead of LLMLingua-2",
    )

    args = parser.parse_args()

    result = compress_file(
        args.file,
        ratio=args.ratio,
        force_tokens=args.force_tokens,
        output_path=args.output,
    )

    if not args.output:
        print(result)
    else:
        original = Path(args.file).read_text(encoding="utf-8")
        orig_tokens = estimate_tokens(original)
        comp_tokens = estimate_tokens(result)
        print(
            f"Compressed: {orig_tokens} → {comp_tokens} tokens "
            f"({comp_tokens/orig_tokens:.0%} of original)"
        )
