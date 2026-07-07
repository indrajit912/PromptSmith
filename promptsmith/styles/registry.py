"""
Style registry for managing prompt styles.
"""

from typing import Dict, List, Optional
from promptsmith.styles.base import PromptStyle
from promptsmith.styles.builtins import GeneralStyle, MathStyle, CodeStyle
from promptsmith.exceptions import StyleNotFoundError
from promptsmith.utils.logger import logger

class StyleRegistry:
    """
    Registry to manage built-in and user-defined prompt styles.
    """
    
    def __init__(self) -> None:
        self._styles: Dict[str, PromptStyle] = {}
        self._register_builtins()
        
    def _register_builtins(self) -> None:
        """Registers built-in prompt styles."""
        self.register(GeneralStyle())
        self.register(MathStyle())
        self.register(CodeStyle())
        
        from promptsmith.styles.builtins import BUILTIN_STYLES_DATA, BuiltinPromptStyle
        for name, info in BUILTIN_STYLES_DATA.items():
            self.register(BuiltinPromptStyle(name, info["description"], info["template"]))
        
    def register(self, style: PromptStyle, override: bool = False) -> None:
        """
        Registers a prompt style.
        
        Args:
            style: The PromptStyle instance to register.
            override: If True, allows overriding an existing style with the same name.
            
        Raises:
            ValueError: If the style name already exists and override is False.
        """
        name = style.name.lower()
        if name in self._styles and not override:
            logger.warning(f"Style '{name}' is already registered. Skipping registry override.")
            raise ValueError(f"Style '{name}' is already registered. Set override=True to replace.")
            
        self._styles[name] = style
        logger.debug(f"Registered style: {name} ({style.description})")
        
    def get(self, name: str) -> PromptStyle:
        """
        Retrieves a style by name.
        
        Args:
            name: Name of the style.
            
        Returns:
            The PromptStyle instance.
            
        Raises:
            StyleNotFoundError: If style is not found.
        """
        style_key = name.lower()
        if style_key not in self._styles:
            logger.error(f"Style '{name}' not found in registry.")
            raise StyleNotFoundError(
                f"Style '{name}' is not supported. "
                f"Available styles: {', '.join(self.list_names())}"
            )
        return self._styles[style_key]
        
    def list_styles(self) -> List[PromptStyle]:
        """Returns a list of all registered styles."""
        return list(self._styles.values())
        
    def list_names(self) -> List[str]:
        """Returns a list of all registered style names."""
        return list(self._styles.keys())
