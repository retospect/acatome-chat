# acatome-chat

**A local-first AI research assistant for scientific literature.**

Runs with a **local Ollama model** by default — or switch to **Claude**, **GPT-4o**, or any litellm-compatible provider with a single flag. One install gives you an interactive shell with a searchable paper library, document editing, live web search, and domain-specific databases — all wired together through the Model Context Protocol (MCP).

## What you get

| Capability | Powered by | What it does |
|---|---|---|
| **Paper library** | [`acatome-mcp`](https://github.com/retospect/acatome-mcp) + [`acatome-store`](https://github.com/retospect/acatome-store) | Semantic search over your papers. Navigate by slug, DOI, or arXiv ID. Read abstracts, TOCs, full chunks, figures. Add notes. |
| **PDF extraction** | [`acatome-extract`](https://github.com/retospect/acatome-extract) | Drop a PDF, get structured text with metadata lookup (CrossRef + Semantic Scholar), RAKE keywords, and optional LLM summaries. Supports articles, datasheets, tech reports. |
| **Document writing** | [`precis-mcp`](https://github.com/retospect/precis-mcp) | Open, navigate, and edit Word (.docx) and LaTeX (.tex) documents. Tracked changes in Word. Auto-numbered headings. Citation support. |
| **Web search** | [`perplexity-sonar-mcp`](https://github.com/retospect/perplexity-sonar-mcp) | Live web queries via Perplexity Sonar — quick lookups, deep research with citations, academic and finance focus modes. |
| **Catalysis DB** | [`catapult-mcp`](https://github.com/retospect/catapult-mcp) | Query DFT reaction energies, activation barriers, and catalyst comparisons from CatHub and Materials Project. |
| **MOF DB** | [`grandmofty-mcp`](https://github.com/retospect/grandmofty-mcp) | Search Metal-Organic Frameworks by pore size, surface area, void fraction, gas isotherms. Data from CoRE, hMOF, QMOF. |
| **LLM shell** | [`acatome-lambic`](https://github.com/retospect/acatome-lambic) | Provider-agnostic chat with tool use, thinking mode, and MCP server management. Works with Ollama, OpenAI, Anthropic, and any litellm-compatible provider. |

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

### 1. Build your paper library

Extract PDFs and ingest them into the searchable store:

```bash
# Extract a single PDF (or a whole directory)
acatome-extract extract paper.pdf
acatome-extract extract ~/Downloads/papers/

# Ingest extracted bundles into the searchable store
acatome-store ingest ~/.acatome/papers/
```

Optional enrichment steps:
```bash
# Watch a folder for new PDFs (auto-extracts on arrival)
acatome-extract watch ~/Downloads/papers/

# Add LLM-generated summaries to your bundles
acatome-extract enrich ~/.acatome/papers/
```

### 2. Start the chat

```bash
# Default: local Ollama model (ollama/qwen3.5:9b)
acatome-chat

# Or use Claude / GPT-4o / any litellm provider
acatome-chat --model anthropic/claude-sonnet-4-20250514
acatome-chat --model openai/gpt-4o
acatome-chat --model ollama/llama3.1:8b

# Disable thinking/reasoning mode
acatome-chat --no-think
```

### 3. Use slash commands

The shell has `/` commands with **tab autocomplete**:

| Command | What it does |
|---|---|
| `/tools` | List all available MCP tools |
| `/status` | Show connected model and servers |
| `/model <spec>` | Switch LLM provider on the fly |
| `/think` / `/nothink` | Toggle reasoning mode |
| `/db` | Show paper library connection info and stats |
| `/review <prompt>` | Review the active document (see below) |
| `/help` | Show command help |
| `/quit` | Exit the shell |

### 4. Review documents

```
› /review check scientific rigor and paragraph structure
› /review fix grammar and clarity --fix
› /review verify citations --comments-only
› /review improve transitions --section S2.3
```

The assistant reads each section, applies fixes as tracked changes, and adds margin comments for issues needing human judgment.

### 5. Talk to your papers

After ingesting papers, the LLM has direct access to your library. Example prompts:

```
› Find papers about CO2 conversion and write a summary with citations into co2review.docx
› Search for MOFs with high CO2 uptake and compare their pore sizes
› Read the abstract of li2024mof and summarize the key findings
› Open my draft.docx and add a new section about these results
› Search the web for recent advances in direct air capture
```

The assistant can read your papers, search the web, query chemistry databases, and **write results directly into .docx or .tex files** — all in one conversation.

> **Note:** Document editing supports **.docx** and **.tex** formats. For Word files, changes are written as tracked changes. Be aware that Word may overwrite the file if it's open — save and close Word before asking the assistant to edit.

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
