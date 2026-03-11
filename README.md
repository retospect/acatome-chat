# acatome-chat

**A local-first AI research assistant for scientific literature.**

Runs with a **local Ollama model** by default — or switch to **Claude**, **GPT-4o**, or any litellm-compatible provider with a single flag. One install gives you an interactive shell with a searchable paper library, document editing, live web search, and domain-specific databases — all wired together through the Model Context Protocol (MCP).

## What you get

| Capability | Powered by | What it does |
|---|---|---|
| **Paper library** | `acatome-mcp` + `acatome-store` | Semantic search over your papers. Navigate by slug, DOI, or arXiv ID. Read abstracts, TOCs, full chunks, figures. Add notes. |
| **PDF extraction** | `acatome-extract` | Drop a PDF, get structured text with metadata lookup (CrossRef + Semantic Scholar), RAKE keywords, and optional LLM summaries. Supports articles, datasheets, tech reports. |
| **Document writing** | `precis-mcp` | Open, navigate, and edit Word (.docx) and LaTeX (.tex) documents. Tracked changes in Word. Auto-numbered headings. Citation support. |
| **Web search** | `perplexity-sonar-mcp` | Live web queries via Perplexity Sonar — quick lookups, deep research with citations, academic and finance focus modes. |
| **Catalysis DB** | `catapult-mcp` | Query DFT reaction energies, activation barriers, and catalyst comparisons from CatHub and Materials Project. |
| **MOF DB** | `grandmofty-mcp` | Search Metal-Organic Frameworks by pore size, surface area, void fraction, gas isotherms. Data from CoRE, hMOF, QMOF. |
| **LLM shell** | `acatome-lambic` | Provider-agnostic chat with tool use, thinking mode, and MCP server management. Works with Ollama, OpenAI, Anthropic, and any litellm-compatible provider. |

## Install

```bash
pip install acatome-chat
# or
uv add acatome-chat
```

That's it. All MCP servers and the paper store are included. Default backend is **SQLite + Chroma** — no external services needed.

For heavier setups:
```bash
uv add "acatome-chat[postgres]"     # PostgreSQL + pgvector
uv add "acatome-chat[embeddings]"   # sentence-transformers
```

## Quick start

```bash
# Start the shell (default: ollama/qwen3.5:9b)
acatome-chat

# Use a different model
acatome-chat --model ollama/llama3.1:8b
acatome-chat --model anthropic/claude-sonnet-4-20250514
acatome-chat --model openai/gpt-4o

# Disable thinking/reasoning mode
acatome-chat --no-think
```

### Build your paper library

```bash
# Extract a single PDF
acatome-extract extract paper.pdf

# Extract all PDFs in a directory
acatome-extract extract ~/Downloads/papers/

# Watch a folder for new PDFs
acatome-extract watch ~/Downloads/papers/

# Enrich with LLM summaries
acatome-extract enrich ~/.acatome/papers/

# Ingest into the searchable store
acatome-store ingest ~/.acatome/papers/
```

### Talk to your papers

Once inside the shell, the LLM has direct access to your library:

```
> Find papers about CO2 capture in MOFs from 2020 onwards
> Read the abstract of li2024mof
> Summarize the key findings from chunks 12-18
> Search the web for recent advances in direct air capture
> Open my review draft and add a paragraph about these results
```

## Architecture

```
acatome-chat (you are here)
├── acatome-lambic        LLM shell engine (MCP client)
├── acatome-mcp           Paper query MCP server
│   └── acatome-store     SQLite/Postgres + Chroma/pgvector storage
│       └── acatome-meta  Shared config and metadata
├── acatome-extract       PDF → structured bundle pipeline
│   └── precis-summary    RAKE keyword extraction
├── precis-mcp            Document editor MCP server
├── perplexity-sonar-mcp  Web search MCP server
├── catapult-mcp          Catalysis database MCP server
│   └── chemdb-common     Shared chemistry DB utilities
└── grandmofty-mcp        MOF database MCP server
    └── chemdb-common
```

## Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `PERPLEXITY_API_KEY` | For web search | Perplexity Sonar API key |
| `OPENAI_API_KEY` | For OpenAI models | OpenAI API key |
| `ANTHROPIC_API_KEY` | For Anthropic models | Anthropic API key |

For local models via Ollama, no API keys are needed.

## License

GPL-3.0-or-later
