"""CLI entry point for acatome-chat."""

from __future__ import annotations

import argparse
import logging


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="acatome-chat",
        description="Acatome research assistant shell",
    )
    parser.add_argument(
        "--model",
        "-m",
        default="",
        help="LLM model spec (e.g. ollama/qwen3.5:9b)",
    )
    parser.add_argument(
        "--no-think",
        action="store_true",
        help="Disable reasoning/thinking mode",
    )
    parser.add_argument(
        "--log",
        default="",
        help="Log file path",
    )
    args = parser.parse_args()

    from acatome_chat.config import default_config

    config = default_config()

    # CLI overrides
    if args.model:
        if "/" in args.model:
            provider, model = args.model.split("/", 1)
        else:
            provider, model = "ollama", args.model
        config.llm.provider = provider
        config.llm.model = model

    if args.no_think:
        config.llm.think = False

    if args.log:
        config.log_file = args.log

    # Logging
    handlers: list[logging.Handler] = []
    if config.log_file:
        handlers.append(logging.FileHandler(config.log_file))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers or None,
    )

    from lambic.tui.app import Shell

    shell = Shell(config=config)
    shell.run()


if __name__ == "__main__":
    main()
