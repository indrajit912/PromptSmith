"""
Base classes for PromptSmith styles.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class PromptStyle(ABC):
    """
    Abstract base class representing a prompt style.
    
    Each style is responsible for transforming a raw prompt string
    into a formatted prompt according to a predefined or configured template.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier name of the style (e.g., 'math', 'code')."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what this style does."""
        pass
        
    @property
    @abstractmethod
    def template(self) -> str:
        """The template string containing 'RAW_PROMPT' placeholder."""
        pass
        
    def format(self, raw_prompt: str) -> str:
        """
        Formats the raw prompt by substituting it into the template.
        
        Args:
            raw_prompt: The verbatim user prompt.
            
        Returns:
            The fully formatted prompt string.
        """
        return self.template.replace("RAW_PROMPT", raw_prompt)
        
    def to_dict(self) -> Dict[str, Any]:
        """Converts the prompt style metadata to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "template": self.template
        }


class CustomPromptStyle(PromptStyle):
    """
    A concrete PromptStyle implementation used for user-defined styles.
    """
    
    def __init__(self, name: str, description: str, template: str):
        self._name = name
        self._description = description
        self._template = template
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def description(self) -> str:
        return self._description
        
    @property
    def template(self) -> str:
        return self._template
