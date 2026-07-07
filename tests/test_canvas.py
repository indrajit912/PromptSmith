"""
Tests for CanvasManager and launch_editor in promptsmith.canvas.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

from promptsmith import __version__
from promptsmith.canvas import CanvasManager, launch_editor
from promptsmith.exceptions import InputError, ConfigurationError, PromptSmithError

def test_canvas_manager_reset(tmp_path):
    canvas_path = tmp_path / "canvas.txt"
    manager = CanvasManager(canvas_path)
    manager.reset()
    
    assert canvas_path.exists()
    content = canvas_path.read_text(encoding="utf-8")
    assert f"PromptSmith v{__version__}" in content
    assert "Start writing below this line." in content

def test_canvas_manager_read_prompt(tmp_path):
    canvas_path = tmp_path / "canvas.txt"
    manager = CanvasManager(canvas_path)
    manager.reset()
    
    from promptsmith.canvas import HEADER_TEMPLATE
    header_content = HEADER_TEMPLATE.format(version=__version__)
    
    user_input = (
        "# Markdown Header\n"
        "\n"
        "## Section 1\n"
        "Text content\n"
        "# Comment line we want to preserve in markdown\n"
    )
    
    canvas_path.write_text(header_content + "\n" + user_input, encoding="utf-8")
    
    prompt = manager.read_prompt()
    assert prompt == "# Markdown Header\n\n## Section 1\nText content\n# Comment line we want to preserve in markdown"

def test_canvas_manager_read_prompt_empty(tmp_path):
    canvas_path = tmp_path / "canvas.txt"
    manager = CanvasManager(canvas_path)
    manager.reset()
    
    with pytest.raises(InputError) as exc_info:
        manager.read_prompt()
    assert "cannot be empty" in str(exc_info.value)

@patch("shutil.which")
def test_launch_editor_missing(mock_which, tmp_path):
    mock_which.return_value = None
    
    with pytest.raises(ConfigurationError) as exc_info:
        launch_editor("nonexistent-editor", tmp_path / "canvas.txt")
    assert "was not found on your system PATH" in str(exc_info.value)

@patch("shutil.which")
@patch("subprocess.run")
def test_launch_editor_success(mock_run, mock_which, tmp_path):
    mock_which.return_value = "/usr/bin/vim"
    launch_editor("vim", tmp_path / "canvas.txt")
    
    mock_run.assert_called_once_with(["vim", str(tmp_path / "canvas.txt")], check=True)

@patch("shutil.which")
@patch("subprocess.run")
def test_launch_editor_keyboard_interrupt(mock_run, mock_which, tmp_path):
    mock_which.return_value = "/usr/bin/vim"
    mock_run.side_effect = KeyboardInterrupt()
    
    with pytest.raises(PromptSmithError) as exc_info:
        launch_editor("vim", tmp_path / "canvas.txt")
    assert "session interrupted by user" in str(exc_info.value).lower()
