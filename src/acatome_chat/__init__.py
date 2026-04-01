"""acatome-chat — research assistant shell."""

from importlib.metadata import version

__version__ = version("acatome-chat")

from acatome_chat.config import default_config

__all__ = ["default_config"]
