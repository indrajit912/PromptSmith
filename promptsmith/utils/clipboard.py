"""
Clipboard helper functions for PromptSmith.
"""

import pyperclip
from promptsmith.exceptions import ClipboardError
from promptsmith.utils.logger import logger

def copy_to_clipboard(text: str) -> None:
    """
    Copies the given text to the system clipboard.
    
    Raises:
        ClipboardError: If the clipboard copy fails.
    """
    try:
        logger.debug("Attempting to copy prompt to clipboard...")
        pyperclip.copy(text)
        logger.debug("Successfully copied prompt to clipboard.")
    except Exception as e:
        logger.error(f"Clipboard copy failed: {e}")
        raise ClipboardError(
            "Could not copy to the clipboard. "
            "Please ensure you have clipboard access enabled or a clipboard manager running."
        ) from e
