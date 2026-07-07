"""
Logging configuration for PromptSmith.
"""

import logging
import sys

logger = logging.getLogger("promptsmith")

def setup_logger(verbose: bool = False) -> None:
    """
    Sets up the global logger for promptsmith.
    
    If verbose is True, sets the log level to DEBUG, otherwise WARNING.
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logger.setLevel(level)
    
    # Remove existing handlers to avoid double logging
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
