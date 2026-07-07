"""
Tests for Command Line Interface using click.testing.CliRunner.
"""

import pytest
from unittest.mock import patch
from click.testing import CliRunner
from promptsmith.cli import cli

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "PromptSmith version" in result.output
    assert "Indrajit Ghosh" in result.output

def test_cli_list_styles():
    runner = CliRunner()
    result = runner.invoke(cli, ["--list-styles"])
    assert result.exit_code == 0
    assert "Available PromptSmith Styles" in result.output
    assert "general" in result.output
    assert "math" in result.output
    assert "code" in result.output

def test_cli_print_prompt():
    runner = CliRunner()
    result = runner.invoke(cli, ["--style", "general", "--print", "Hello World"])
    assert result.exit_code == 0
    assert "Hello World" in result.output
    assert "clarity" in result.output

def test_cli_invalid_style():
    runner = CliRunner()
    result = runner.invoke(cli, ["--style", "invalidstyle", "--print", "Hello World"])
    assert result.exit_code == 1
    assert "Error:" in result.output
    assert "invalidstyle" in result.output

def test_cli_custom_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "PROMPTSMITH" in result.output
    assert "Options & Arguments" in result.output
    assert "Examples" in result.output

@patch("promptsmith.cli.launch_editor")
@patch("promptsmith.config.get_default_config_path")
def test_cli_edit_config(mock_get_config_path, mock_launch_editor, tmp_path):
    runner = CliRunner()
    mock_get_config_path.return_value = tmp_path / "config.toml"
    result = runner.invoke(cli, ["--config"])
    assert result.exit_code == 0
    mock_launch_editor.assert_called_once()
    assert (tmp_path / "config.toml").exists()

