"""Tests for acatome-chat configuration."""

from __future__ import annotations

import pytest

from acatome_chat.config import default_config
from acatome_chat.prompts import SYSTEM_PROMPT


class TestDefaultConfig:
    def test_defaults(self):
        cfg = default_config()
        assert cfg.llm.provider == "ollama"
        assert cfg.llm.model == "qwen3.5:9b"
        assert cfg.llm.think is True
        assert len(cfg.servers) == 3
        assert cfg.servers[0].name == "acatome"
        assert cfg.servers[1].name == "precis"
        assert cfg.servers[2].name == "perplexity"

    def test_custom_model(self):
        cfg = default_config(model="llama3.2:3b", provider="ollama", think=False)
        assert cfg.llm.model == "llama3.2:3b"
        assert cfg.llm.think is False

    def test_system_prompt_set(self):
        cfg = default_config()
        assert cfg.system_prompt == SYSTEM_PROMPT
        assert "research assistant" in cfg.system_prompt.lower()

    def test_server_commands(self):
        cfg = default_config()
        for s in cfg.servers:
            assert len(s.cmd) >= 2
            assert s.enabled is True


class TestSystemPrompt:
    def test_mentions_tools(self):
        assert "paper" in SYSTEM_PROMPT
        assert "search" in SYSTEM_PROMPT
        assert "note" in SYSTEM_PROMPT
        assert "precis" in SYSTEM_PROMPT.lower()
        assert "acatome" in SYSTEM_PROMPT.lower()
        assert "perplexity" in SYSTEM_PROMPT.lower()
