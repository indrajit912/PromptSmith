"""
Configuration management for PromptSmith.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import toml
from platformdirs import user_config_dir

from promptsmith.exceptions import ConfigurationError
from promptsmith.styles.base import CustomPromptStyle
from promptsmith.styles.registry import StyleRegistry
from promptsmith.utils.logger import logger

DEFAULT_CONFIG_FILENAME = "config.toml"

def get_default_config_dir() -> Path:
    """Returns the default directory path for configuration."""
    return Path(user_config_dir("promptsmith"))

def get_default_config_path() -> Path:
    """Returns the default filepath for configuration."""
    return get_default_config_dir() / DEFAULT_CONFIG_FILENAME

def get_default_canvas_path() -> Path:
    """Returns the default filepath for the temporary prompt canvas."""
    return get_default_config_dir() / "canvas.txt"

def create_default_config(config_path: Path) -> None:
    """
    Creates a default configuration file with examples.
    """
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        default_content = """# PromptSmith Configuration File
# Save this file to customize default settings or define your own prompt styles.

[settings]
# The default style to use if --style is not specified
default_style = "math"

# Whether to copy to clipboard by default (set to false to default to printing)
default_to_clipboard = true

# The preferred text editor to launch for writing prompts (e.g., "vim", "notepad", "code --wait")
editor = "vim"

# Define custom prompt styles here.
# The template MUST contain the exact string 'RAW_PROMPT' somewhere.
[styles.writer]
description = "Optimize prompt for creative writing, editing, or proofreading"
template = \"\"\"Rewrite the following prompt for an AI chatbot to improve its creative flow, style, and tone.

-----------
RAW_PROMPT
-----------

Please rewrite the prompt to make it engaging, descriptive, and clear. Instruct the chatbot to use rich vocabulary, appropriate pacing, and a tone suited for creative storytelling or writing.\"\"\"

[styles.summary]
description = "Optimize prompt for summarizing long texts or documents"
template = \"\"\"Rewrite the following prompt for an AI chatbot to specialize in document summarizing and extraction.

-----------
RAW_PROMPT
-----------

Please rewrite the prompt to ensure the AI creates high-quality summaries. The rewritten prompt should instruct the AI to capture key takeaways, structure the summary logically, and ignore redundant details.\"\"\"
"""
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(default_content)
        logger.info(f"Created default configuration file at {config_path}")
    except Exception as e:
        logger.error(f"Failed to create default config file: {e}")

class Configuration:
    """
    Manages loading and parsing the PromptSmith configuration file.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Check user config dir first, fallback to ~/.promptsmith.toml
            local_config = get_default_config_path()
            home_config = Path.home() / ".promptsmith.toml"
            
            if local_config.exists():
                self.config_path = local_config
            elif home_config.exists():
                self.config_path = home_config
            else:
                self.config_path = local_config
                
        self.settings: Dict[str, Any] = {
            "default_style": "math",
            "default_to_clipboard": True,
            "editor": "vim"
        }
        self.custom_styles: Dict[str, Dict[str, str]] = {}
        
    def load(self) -> None:
        """
        Loads and parses the configuration file if it exists.
        
        Raises:
            ConfigurationError: If the configuration file is malformed or invalid.
        """
        if not self.config_path.exists():
            logger.debug(f"Configuration file not found at {self.config_path}. Using defaults.")
            # Optionally create default config if it's the default path
            if self.config_path == get_default_config_path():
                create_default_config(self.config_path)
            return

        try:
            logger.debug(f"Loading configuration from {self.config_path}")
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = toml.load(f)
                
            # Parse settings
            if "settings" in data:
                settings_data = data["settings"]
                if "default_style" in settings_data:
                    self.settings["default_style"] = str(settings_data["default_style"]).strip()
                if "default_to_clipboard" in settings_data:
                    self.settings["default_to_clipboard"] = bool(settings_data["default_to_clipboard"])
                if "editor" in settings_data:
                    self.settings["editor"] = str(settings_data["editor"]).strip()
                    
            # Parse custom styles
            if "styles" in data:
                for name, style_data in data["styles"].items():
                    if not isinstance(style_data, dict):
                        continue
                    
                    description = style_data.get("description", "User defined custom style")
                    template = style_data.get("template", "")
                    
                    if not template:
                        raise ConfigurationError(
                            f"Custom style '{name}' is missing the 'template' field."
                        )
                    if "RAW_PROMPT" not in template:
                        raise ConfigurationError(
                            f"Template for custom style '{name}' must contain the verbatim "
                            "placeholder 'RAW_PROMPT'."
                        )
                        
                    self.custom_styles[name] = {
                        "description": description,
                        "template": template
                    }
                    
            logger.debug("Successfully loaded configuration.")
        except Exception as e:
            if isinstance(e, ConfigurationError):
                raise
            raise ConfigurationError(
                f"Failed to parse configuration file '{self.config_path}': {e}"
            ) from e
            
    def register_custom_styles(self, registry: StyleRegistry) -> None:
        """Registers the custom styles from configuration into the style registry."""
        for name, info in self.custom_styles.items():
            try:
                style = CustomPromptStyle(
                    name=name,
                    description=info["description"],
                    template=info["template"]
                )
                registry.register(style, override=True)
                logger.debug(f"Registered custom style from config: {name}")
            except Exception as e:
                logger.warning(f"Failed to register custom style '{name}': {e}")
