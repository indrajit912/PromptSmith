"""
Tests for StyleRegistry.
"""

import pytest
from promptsmith.styles.registry import StyleRegistry
from promptsmith.styles.base import CustomPromptStyle
from promptsmith.exceptions import StyleNotFoundError

def test_registry_builtins():
    registry = StyleRegistry()
    assert "general" in registry.list_names()
    assert "math" in registry.list_names()
    assert "code" in registry.list_names()
    
    style = registry.get("math")
    assert style.name == "math"

def test_registry_register_custom():
    registry = StyleRegistry()
    custom = CustomPromptStyle("test-style", "test desc", "RAW_PROMPT test template")
    registry.register(custom)
    
    assert "test-style" in registry.list_names()
    assert registry.get("test-style").description == "test desc"
    assert registry.get("test-style").format("hello") == "hello test template"

def test_registry_override():
    registry = StyleRegistry()
    custom1 = CustomPromptStyle("general", "override desc", "RAW_PROMPT override")
    
    with pytest.raises(ValueError):
        registry.register(custom1)  # No override flag
        
    registry.register(custom1, override=True)
    assert registry.get("general").description == "override desc"

def test_registry_not_found():
    registry = StyleRegistry()
    with pytest.raises(StyleNotFoundError):
        registry.get("non-existent")

def test_registry_new_styles():
    registry = StyleRegistry()
    names = registry.list_names()
    assert "technical" in names
    assert "debug" in names
    assert "security" in names
    
    style = registry.get("security")
    assert style.name == "security"
    assert "vulnerability" in style.description.lower()
