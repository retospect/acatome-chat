"""Tests for acatome-chat configuration."""

from __future__ import annotations

from acatome_chat.config import default_config
from acatome_chat.prompts import (
    SYSTEM_PROMPT,
    build_review_message,
    parse_review_command,
)


class TestDefaultConfig:
    def test_defaults(self):
        cfg = default_config()
        assert cfg.llm.provider == "ollama"
        assert cfg.llm.model == "qwen3.5:9b"
        assert cfg.llm.think is True
        assert len(cfg.servers) == 6
        names = [s.name for s in cfg.servers]
        assert names == [
            "precis", "perplexity", "mofty",
            "catapult", "patentorney", "gripe",
        ]

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
        assert "search()" in SYSTEM_PROMPT
        assert "precis" in SYSTEM_PROMPT.lower()
        assert "perplexity" in SYSTEM_PROMPT.lower()
        assert "[@slug]" in SYSTEM_PROMPT

    def test_mentions_self_monitoring(self):
        assert "report_issue" in SYSTEM_PROMPT


class TestParseReviewCommand:
    def test_basic(self):
        r = parse_review_command("/review check rigor")
        assert r["prompt"] == "check rigor"
        assert r["mode"] == "hybrid"
        assert r["section"] == ""

    def test_comments_only(self):
        r = parse_review_command("/review check rigor --comments-only")
        assert r["prompt"] == "check rigor"
        assert r["mode"] == "comments-only"

    def test_fix_mode(self):
        r = parse_review_command("/review fix grammar --fix")
        assert r["prompt"] == "fix grammar"
        assert r["mode"] == "fix"

    def test_section_flag(self):
        r = parse_review_command("/review check rigor --section S2.3")
        assert r["prompt"] == "check rigor"
        assert r["section"] == "S2.3"

    def test_all_flags(self):
        r = parse_review_command("/review rigor --comments-only --section S1.0")
        assert r["prompt"] == "rigor"
        assert r["mode"] == "comments-only"
        assert r["section"] == "S1.0"

    def test_empty_prompt(self):
        r = parse_review_command("/review")
        assert r["prompt"] == ""
        assert r["mode"] == "hybrid"

    def test_no_prefix(self):
        r = parse_review_command("check rigor")
        assert r["prompt"] == "check rigor"


class TestBuildReviewMessage:
    def test_hybrid_default(self):
        msg = build_review_message("/review check rigor")
        assert "check rigor" in msg
        assert "MAJOR" in msg
        assert "MINOR" in msg
        assert "toc()" in msg
        assert "mode='comment'" in msg
        assert "mode='replace'" in msg

    def test_comments_only(self):
        msg = build_review_message("/review rigor --comments-only")
        assert "do NOT modify any text" in msg

    def test_fix_mode(self):
        msg = build_review_message("/review grammar --fix")
        assert "Fix everything" in msg

    def test_section_scope(self):
        msg = build_review_message("/review rigor --section S2.3")
        assert "S2.3" in msg
        assert "toc()" not in msg

    def test_empty_prompt_defaults(self):
        msg = build_review_message("/review")
        assert "general quality review" in msg

    def test_config_registers_review(self):
        cfg = default_config()
        assert "review" in cfg.message_commands
        assert cfg.message_commands["review"] is build_review_message
