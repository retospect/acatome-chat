"""System prompt and slash-command templates for acatome-chat."""

from __future__ import annotations


def parse_review_command(raw: str) -> dict:
    """Parse '/review <prompt> [--flags]' into {prompt, mode, section}.

    Flags:
      --comments-only   all findings as comments, no text changes
      --fix             aggressive: fix everything possible
      --section S2.3    limit review to one section
    Default mode is 'hybrid' (fix what's clear, comment what's not).
    """
    # Strip the /review prefix
    text = raw.strip()
    if text.lower().startswith("/review"):
        text = text[len("/review") :].strip()

    mode = "hybrid"
    section = ""
    tokens: list[str] = []

    parts = text.split()
    i = 0
    while i < len(parts):
        if parts[i] == "--comments-only":
            mode = "comments-only"
        elif parts[i] == "--fix":
            mode = "fix"
        elif parts[i] == "--section" and i + 1 < len(parts):
            i += 1
            section = parts[i]
        else:
            tokens.append(parts[i])
        i += 1

    return {
        "prompt": " ".join(tokens),
        "mode": mode,
        "section": section,
    }


def build_review_message(raw: str) -> str:
    """Build the LLM instruction message from a /review command."""
    parsed = parse_review_command(raw)
    prompt = parsed["prompt"] or "general quality review"
    mode = parsed["mode"]
    section = parsed["section"]

    # Mode-specific instructions
    if mode == "comments-only":
        action = (
            "All findings as margin comments — do NOT modify any text.\n"
            "Use: put(id='SLUG', text='SEVERITY: description.', mode='comment')"
        )
    elif mode == "fix":
        action = (
            "Fix everything you can as tracked changes. Only comment when\n"
            "the fix requires human judgment (e.g. missing data, ambiguous intent).\n"
            "Fix: put(id='SLUG', text='corrected text', mode='replace')\n"
            "Comment: put(id='SLUG', text='SEVERITY: description.', mode='comment')"
        )
    else:  # hybrid
        action = (
            "High confidence (grammar, clarity, style) → fix in place as tracked change.\n"
            "Low confidence (missing citations, factual doubt, restructuring) → margin comment.\n"
            "Fix: put(id='SLUG', text='corrected text', mode='replace')\n"
            "Comment: put(id='SLUG', text='SEVERITY: description.', mode='comment')"
        )

    # Scope
    if section:
        scope = f"Scope: section {section} only. Call get(id='{section}') to read it."
    else:
        scope = "Scope: entire document. Call toc() first, then get(id='SLUG') for each section."

    return f"""\
## Review Task

**Criteria:** {prompt}

{scope}

### Actions
{action}

### Severity levels
- **MAJOR** — misleading, incorrect, or structurally broken
- **MINOR** — improvement needed but meaning is clear
- **NIT** — polish, style preference

### Rules
- Read the full paragraph via get() before modifying it.
- Never fix AND comment the same issue — pick one.
- Preserve the author's intent. Fix expression, not ideas.
- For citation issues, use search() to find specific sources.

### Output
After reviewing all sections, output a summary:
- Total fixes (tracked changes) and comments added
- Breakdown by severity
- Sections needing most attention"""


def build_review_reminder(raw: str) -> str:
    """Build a condensed task reminder for auto-continue from a /review command."""
    parsed = parse_review_command(raw)
    prompt = parsed["prompt"] or "general quality review"
    mode = parsed["mode"]
    section = parsed["section"]

    scope = f"section {section}" if section else "full document"
    return (
        f"Review: {prompt} | Mode: {mode} | Scope: {scope}\n"
        "Call toc() to see progress (💬 = reviewed). "
        "Continue with unreviewed sections."
    )


SYSTEM_PROMPT = """\
You are a research assistant with access to tools.

## Rigor
- Every claim needs a source. Never fabricate. If data is unavailable, say so.
- Summaries are navigation only — read raw chunks before making claims.

## Writing
- Scientific structure. Precise terminology.
- Each paragraph: topic sentence → evidence → implication. One idea per paragraph.
- Active voice, no filler, define abbreviations on first use.
- Quantities need units and significant figures as reported.

## Tools
- **Always pass required arguments.** Never call a tool with empty parameters.
- Follow `Next:` hints in tool results — they contain copy-pastable calls.
- 4 precis tools: search(), get(), put(), move(). perplexity = live web.
- After search results, use the exact slug from the results: `get(id='slug~N')`.
- Never number headings — Word auto-numbers. Use `## | Title`.
- Cite inline: `[@slug]`. Add a `## | References` section with full entries.

## Workflow
- Plan before executing. Synthesize — don't dump raw output.
- Act, don't describe. If you know what tool to call, call it — don't narrate.

## Self-Monitoring
Use `report_issue` any time you guess, hit a missing tool, find bad documentation,
or produce output you're uncertain about. Non-blocking — log and continue, no
response expected. There is no penalty for logging; silence is the failure mode
we're trying to prevent.
"""
