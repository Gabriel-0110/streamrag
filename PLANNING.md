# Project Planning: RAG AI Agent with Pydantic AI and Supabase

## Purpose
High-level vision, architecture, constraints, tech stack, tools, and organizational principles for the RAG-Vs project.

**Prompt to AI**: "Use the structure and decisions outlined in PLANNING.md."

## Project Vision
Build a clean, minimal, and practical RAG (Retrieval-Augmented Generation) application that demonstrates best practices for:
- Document ingestion and vector storage
- AI agent architecture with tool integration
- Modern Python development practices
- Clean, maintainable code organization

## Architecture Principles

### 1. Modular Design
- **Separation of Concerns**: Core logic separated from UI and configuration
- **Clear Boundaries**: Well-defined interfaces between components
- **Extensibility**: Easy to add new features or swap components

### 2. Project Structure
```
src/
├── core/           # Core business logic (stable, reusable)
│   ├── agent/      # AI agent components
│   └── ingestion/  # Document processing pipeline
├── ui/             # User interfaces (can be swapped/extended)
└── env.py          # Environment management

config/             # Configuration files and templates
sql/               # Database schemas and scripts
scripts/           # Utility and development scripts
docs/              # Documentation
tests/             # Test suite
```

### 3. Technology Stack

**Core Technologies**:
- **Pydantic AI**: Modern AI agent framework with type safety
- **OpenAI**: GPT models for generation, embeddings for retrieval
- **Supabase**: PostgreSQL + pgvector for vector storage
- **Streamlit**: Simple web UI for prototyping

**Development Tools**:
- **uv**: Modern Python package manager
- **Ruff**: Fast Python linter and formatter
- **pytest**: Testing framework
- **Type hints**: Full type safety throughout

### 4. Code Quality Standards
- All code must pass Ruff linting (zero warnings)
- Type hints required for all public APIs
- Clear error handling and logging
- Comprehensive docstrings for modules and functions

## Implementation Guidelines

### For AI Assistants
When working on this project:

1. **Follow the Structure**: Use the established directory layout
2. **Update Imports**: When moving files, update all import paths
3. **Maintain Quality**: Run `uv run ruff check src/` before finalizing changes
4. **Document Changes**: Update README.md and docs/ when structure changes
5. **Test Everything**: Verify functionality after refactoring

### Key Design Decisions

1. **Why Pydantic AI**: Type-safe agent framework with excellent tool integration
2. **Why Supabase**: Managed PostgreSQL with pgvector, simpler than self-hosting
3. **Why Streamlit**: Rapid prototyping, but UI layer is easily replaceable
4. **Why uv**: Faster than pip, better dependency resolution
5. **Why Modular Structure**: Enables testing, maintenance, and team collaboration

## Development Workflow

1. **Setup**: Use `uv sync` for dependencies
2. **Environment**: Copy `config/ENV.sample` to `.env`
3. **Database**: Run `sql/setup_database.sql` in Supabase
4. **Test**: Use `scripts/try_agent.py` for quick testing
5. **Lint**: Always run `uv run ruff check src/` before commits

## Extension Points

- **New UIs**: Add to `src/ui/` (FastAPI, CLI, etc.)
- **New Agents**: Extend `src/core/agent/` with specialized agents
- **New Data Sources**: Add processors to `src/core/ingestion/`
- **New Storage**: Abstract storage layer in `src/core/ingestion/`

This structure supports both rapid prototyping and production deployment.
