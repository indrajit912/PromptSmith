"""
Custom exceptions for PromptSmith.
"""

class PromptSmithError(Exception):
    """Base exception for all PromptSmith errors."""
    pass

class ConfigurationError(PromptSmithError):
    """Raised when there is an issue with the configuration file."""
    pass

class StyleNotFoundError(PromptSmithError):
    """Raised when a requested prompt style is not registered."""
    pass

class ClipboardError(PromptSmithError):
    """Raised when clipboard operations fail."""
    pass

class InputError(PromptSmithError):
    """Raised when there is an issue with the user input."""
    pass
