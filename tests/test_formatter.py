"""
Tests for prompt formatting and substitution.
"""

import pytest
from promptsmith.formatter import PromptFormatter

def test_general_formatting():
    formatter = PromptFormatter()
    formatter.initialize()
    raw = "Show me how to build a flask app."
    formatted = formatter.format_prompt(raw, "general")
    assert raw in formatted
    assert "clarity" in formatted.lower()

def test_math_formatting():
    formatter = PromptFormatter()
    formatter.initialize()
    raw = "Solve x^2 + y^2 = z^2."
    formatted = formatter.format_prompt(raw, "math")
    assert raw in formatted
    assert "latex" in formatted.lower()
    assert "$...$" in formatted

def test_code_formatting():
    formatter = PromptFormatter()
    formatter.initialize()
    raw = "Write a quicksort in python."
    formatted = formatter.format_prompt(raw, "code")
    assert raw in formatted
    assert "software" in formatted.lower()
    assert "markdown" in formatted.lower()

def test_default_style_is_math():
    formatter = PromptFormatter()
    formatter.initialize()
    # By default, get_style should return the math style
    style = formatter.get_style()
    assert style.name == "math"

def test_separator_lines():
    formatter = PromptFormatter()
    formatter.initialize()
    raw = "My test raw prompt"
    formatted = formatter.format_prompt(raw, "general")
    expected_segment = f"-----------\n{raw}\n-----------"
    assert expected_segment in formatted

def test_new_styles_formatting():
    formatter = PromptFormatter()
    formatter.initialize()
    raw = "Write an API for user authentication."
    
    # Test api style
    formatted_api = formatter.format_prompt(raw, "api")
    assert raw in formatted_api
    assert "restful" in formatted_api.lower()
    
    # Test devops style
    formatted_devops = formatter.format_prompt(raw, "devops")
    assert raw in formatted_devops
    assert "ci/cd" in formatted_devops.lower()

