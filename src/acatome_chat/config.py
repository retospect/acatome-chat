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
            McpServer(name="acatome", cmd=_find_cmd("acatome-mcp")),
            McpServer(name="precis", cmd=_find_cmd("precis")),
            McpServer(
                name="perplexity",
                cmd=_find_cmd("perplexity-sonar-mcp"),
                env={"PERPLEXITY_API_KEY": os.environ.get("PERPLEXITY_API_KEY", "")},
            ),
            McpServer(name="grandmofty", cmd=_find_cmd("grandmofty-mcp")),
            McpServer(name="catapult", cmd=_find_cmd("catapult-mcp")),
        ],
        system_prompt=SYSTEM_PROMPT,
        message_commands={"review": build_review_message},
        task_reminder_commands={"review": build_review_reminder},
    )
