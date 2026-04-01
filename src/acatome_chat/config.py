"""Default acatome-chat configuration."""

from __future__ import annotations

import os
import shutil

from acatome_lambic.core.config import LlmConfig, McpServer, ShellConfig

from acatome_chat.prompts import (
    SYSTEM_PROMPT,
    build_review_message,
    build_review_reminder,
)


def _find_cmd(name: str) -> list[str]:
    """Find command for an MCP server, preferring uv run."""
    uv = shutil.which("uv")
    if uv:
        return [uv, "run", name]
    exe = shutil.which(name)
    if exe:
        return [exe]
    return ["uv", "run", name]


def _db_status(_cmd: str) -> str:
    """Return store connection info and row counts."""
    try:
        from acatome_store.store import Store

        store = Store()
        s = store.stats()
        store.close()
    except Exception as exc:
        return f"Store unavailable: {exc}"

    backend = s["metadata_backend"]
    if backend == "postgres":
        conn = f"{s['pg_user']}@{s['pg_host']}:{s['pg_port']}/{s['pg_database']}  schema={s['pg_schema']}"
    else:
        conn = s.get("db_path", "?")

    return (
        f"  metadata:  {backend}  {conn}\n"
        f"  vector:    {s['vector_backend']}\n"
        f"  embedding: {s['embed_model']}  dim={s['embed_dim']}\n"
        f"  store:     {s['store_path']}\n"
        f"\n"
        f"  refs:      {s['total_refs']:,}\n"
        f"  papers:    {s['total_papers']:,}\n"
        f"  blocks:    {s['total_blocks']:,}\n"
        f"  verified:  {s['verified']:,}\n"
        f"  indexed:   {s['indexed_blocks']:,}"
    )


def default_config(
    model: str = "qwen3.5:9b",
    provider: str = "ollama",
    think: bool = True,
) -> ShellConfig:
    """Build the default acatome-chat ShellConfig."""
    return ShellConfig(
        llm=LlmConfig(
            provider=provider,
            model=model,
            think=think,
        ),
        servers=[
            McpServer(name="precis", cmd=_find_cmd("precis")),
            McpServer(
                name="perplexity",
                cmd=_find_cmd("perplexity-sonar-mcp"),
                env={"PERPLEXITY_API_KEY": os.environ.get("PERPLEXITY_API_KEY", "")},
            ),
            McpServer(name="mofty", cmd=_find_cmd("grandmofty-mcp")),
            McpServer(name="catapult", cmd=_find_cmd("catapult-mcp")),
            McpServer(name="patentorney", cmd=_find_cmd("patentorney-mcp")),
            McpServer(
                name="gripe",
                cmd=_find_cmd("gripe"),
                env={
                    "GRIPE_AGENT_ID": "acatome-chat",
                    "GRIPE_DB_URL": os.environ.get("GRIPE_DB_URL", ""),
                },
            ),
        ],
        system_prompt=SYSTEM_PROMPT,
        message_commands={"review": build_review_message},
        task_reminder_commands={"review": build_review_reminder},
        custom_commands={"db": _db_status},
    )
