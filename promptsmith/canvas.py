"""
Canvas and Editor management for PromptSmith.
"""

import os
import shutil
import subprocess
import shlex
from pathlib import Path
from promptsmith import __version__
from promptsmith.exceptions import PromptSmithError, InputError, ConfigurationError
from promptsmith.config import get_default_config_path

HEADER_TEMPLATE = """# PromptSmith v{version}
# Copyright © Indrajit Ghosh 2026–Present
#
# Use this temporary canvas to write your prompt.
# This header block will be automatically removed.
# The contents of this file will be erased after execution.
#
# Start writing below this line.
"""

class CanvasManager:
    """Manages the temporary prompt canvas file and editor launches."""
    
    def __init__(self, canvas_path: Path):
        self.canvas_path = canvas_path
        
    def reset(self) -> None:
        """Resets the canvas file to just contain the header template."""
        try:
            self.canvas_path.parent.mkdir(parents=True, exist_ok=True)
            content = HEADER_TEMPLATE.format(version=__version__)
            self.canvas_path.write_text(content, encoding="utf-8")
        except Exception as e:
            raise PromptSmithError(f"Failed to reset canvas file at '{self.canvas_path}': {e}")
            
    def read_prompt(self) -> str:
        """
        Reads the canvas file, discards the initial header lines,
        and returns the prompt string.
        """
        if not self.canvas_path.exists():
            raise PromptSmithError(f"Canvas file not found at '{self.canvas_path}'.")
            
        try:
            # Calculate the number of lines in the generated header
            header_content = HEADER_TEMPLATE.format(version=__version__)
            header_lines_count = len(header_content.splitlines())
            
            with open(self.canvas_path, "r", encoding="utf-8") as f:
                all_lines = f.readlines()
                
            # Discard only the header lines
            user_lines = all_lines[header_lines_count:]
            
            prompt_content = "".join(user_lines).strip()
            if not prompt_content:
                raise InputError(
                    "The prompt cannot be empty. Please write your prompt "
                    "below the header comment lines in the editor."
                )
            return prompt_content
        except Exception as e:
            if isinstance(e, (InputError, PromptSmithError)):
                raise
            raise PromptSmithError(f"Failed to read or parse canvas file: {e}")

def launch_editor(editor_command: str, filepath: Path) -> None:
    """
    Launches the configured editor to edit the temporary canvas file.
    """
    args = shlex.split(editor_command)
    if not args:
        raise ConfigurationError("The configured editor setting is empty.")
        
    executable = args[0]
    
    # Check if executable exists in PATH
    if not shutil.which(executable):
        config_path = get_default_config_path()
        raise ConfigurationError(
            f"The configured editor '{executable}' was not found on your system PATH.\n"
            f"Please ensure it is installed and added to your PATH, or update the "
            f"'editor' setting in your config file:\n"
            f"  - editor = \"notepad\" (Windows standard)\n"
            f"  - editor = \"code --wait\" (VS Code)\n"
            f"  - editor = \"nano\" or \"vim\" (Unix systems)\n"
            f"Config file path: {config_path}"
        )
        
    # Append path of file to edit
    args.append(str(filepath))
    
    try:
        # Run editor subprocess and wait
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        raise PromptSmithError(f"Editor '{executable}' exited with an error status: {e}")
    except KeyboardInterrupt:
        raise PromptSmithError("Editing session interrupted by user.")
    except Exception as e:
        raise PromptSmithError(f"Failed to run editor '{editor_command}': {e}")
