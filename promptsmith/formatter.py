"""
Core formatter that coordinates configuration, style retrieval, and formatting.
"""

from typing import Optional
from pathlib import Path

from promptsmith.styles.registry import StyleRegistry
from promptsmith.config import Configuration
from promptsmith.styles.base import PromptStyle

class PromptFormatter:
    """
    Main engine for PromptSmith. Coordinates config loading, style registration,
    and prompt formatting.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.registry = StyleRegistry()
        self.config = Configuration(config_path)
        
    def initialize(self) -> None:
        """Initializes configuration and registers custom styles."""
        self.config.load()
        self.config.register_custom_styles(self.registry)
        
    def get_style(self, style_name: Optional[str] = None) -> PromptStyle:
        """
        Gets a style by name, or falls back to the configured default style.
        """
        name = style_name or self.config.settings["default_style"]
        return self.registry.get(name)
        
    def format_prompt(self, raw_prompt: str, style_name: Optional[str] = None) -> str:
        """
        Formats the raw prompt using the specified style name (or default).
        """
        style = self.get_style(style_name)
        return style.format(raw_prompt)
