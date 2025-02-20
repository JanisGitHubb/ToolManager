import pytest
from datetime import datetime, timedelta
from Python.Main import ReservationManager, ToolManager

@pytest.fixture
def setup_managers():
    """Fixture to set up managers for testing."""
    tool_manager = ToolManager(admin_password="admin123")  # Creating a tool manager instance
    reservation_manager = ReservationManager(tool_manager)  # Pass the tool_manager instance
    return reservation_manager, tool_manager

def test_reserve_non_existent_tool(setup_managers):
    """Test that reserving a non-existent tool fails."""
    reservation_manager, tool_manager = setup_managers

    # Attempt to reserve a tool that does NOT exist
    tool_name = "NonExistentTool"
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    username = "test_user"

    result = reservation_manager.create_single_reservation(tool_name, start_time, end_time, username)

    assert result == f"Error: The tool '{tool_name}' does not exist. Please select a valid tool."
