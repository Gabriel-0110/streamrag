from __future__ import annotations
from typing import List, Dict


def render_with_citations(answer: str, contexts: List[Dict]) -> str:
    """
    Append source citations to the answer.
    """
    if not contexts:
        return answer
    lines = [answer, "", "Sources:"]
    seen = set()
    for c in contexts:
        src = c.get("metadata", {}).get("source") or c.get("url")
        if not src or src in seen:
            continue
        seen.add(src)
        lines.append(f"- {src}")
    return "\n".join(lines)
