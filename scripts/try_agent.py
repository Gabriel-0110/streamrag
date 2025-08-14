from __future__ import annotations
from src.agent.agent import agent


def main():
    res = agent.run_sync(
        "What documents are available? Use kb_search and cite sources."
    )
    print(res.output)


if __name__ == "__main__":
    main()
