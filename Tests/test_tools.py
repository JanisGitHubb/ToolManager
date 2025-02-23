import pytest
from Python.Tool import Tool

def test_tool_creation():
    test_tool = "tool"
    test_decription = "works"
    test_available = True

    tool = Tool(test_tool,test_decription,test_available)
    assert tool.tool_name == test_tool
    assert tool.description == test_decription
    assert tool.available == True

def