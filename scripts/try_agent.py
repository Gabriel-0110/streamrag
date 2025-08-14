from __future__ import annotations
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from src import env as _env  # noqa: F401
from src.core.agent.agent import agent


def main():
    res = agent.run_sync(
        "What documents are available? Use kb_search and cite sources."
    )
    print(res.output)


if __name__ == "__main__":
    main()
