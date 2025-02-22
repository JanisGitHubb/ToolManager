import pytest
from datetime import datetime, timedelta
from Python.Main import ReservationManager, ToolManager
from app import app, tool_manager, reservation_manager

@pytest.fixture
def setup_managers():
    """Fixture to set up managers for testing."""
    tool_manager = ToolManager(admin_password="admin123")  # Creating a tool manager instance
    reservation_manager = ReservationManager(tool_manager)  # Pass the tool_manager instance
    # Add tools to tool_manager for testing purposes
    tool_manager.add_tool("Microwave", "For heating food", "admin123")
    tool_manager.add_tool("Coffee Maker", "For brewing coffee", "admin123")
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

def test_reserve_existing_tool(setup_managers):
    """Test that reserving an existing tool succeeds."""
    reservation_manager, tool_manager = setup_managers

    tool_name = "Microwave"
    tool_description = "For heating food"

    # Ensure the tool is added before reserving
    tool_manager.add_tool(tool_name, tool_description, "admin123")

    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    username = "test_user"

    result = reservation_manager.create_single_reservation(tool_name, start_time, end_time, username)

    assert result == "Single reservation created successfully."

def test_reserve_past_time(setup_managers):
    reservation_manager, _ = setup_managers
    start_time = datetime.now() - timedelta(hours=1)  # Past time
    end_time = start_time + timedelta(hours=1)

    result = reservation_manager.create_single_reservation("Microwave", start_time, end_time, "test_user")

    assert result == "Error: You cannot make a reservation for a past time."

def test_reserve_valid_time(setup_managers):
    reservation_manager, _ = setup_managers
    start_time = datetime.now() + timedelta(hours=1)  # 1 hour in the future
    end_time = start_time + timedelta(hours=1)  # Ends after start time

    result = reservation_manager.create_single_reservation("Microwave", start_time, end_time, "test_user")

    assert result == "Single reservation created successfully."

def test_reserve_invalid_time_range(setup_managers):
    """Test that a reservation fails if the end time is earlier than the start time."""
    reservation_manager, tool_manager = setup_managers

    tool_name = "Microwave"
    tool_manager.add_tool(tool_name, "For heating food", "admin123")

    start_time = datetime.now() + timedelta(hours=2)
    end_time = start_time - timedelta(hours=1)  # End time is earlier than start time
    username = "test_user"

    result = reservation_manager.create_single_reservation(tool_name, start_time, end_time, username)

    assert result == "Error: The end time must be later than the start time."

def test_reserve_valid_time_order(setup_managers):
    reservation_manager, _ = setup_managers
    
    start_time = datetime.now() + timedelta(hours=1)  # Example: 16:00
    end_time = datetime.now() + timedelta(hours=2)    # Example: 17:00

    result = reservation_manager.create_single_reservation("Microwave", start_time, end_time, "test_user")

    assert result == "Single reservation created successfully."

def test_reserve_overlapping_time(setup_managers):
    reservation_manager, _ = setup_managers
    
    # First reservation: 16:00 - 17:00
    start_time_1 = datetime.now() + timedelta(hours=1)
    end_time_1 = start_time_1 + timedelta(hours=1)
    reservation_manager.create_single_reservation("Microwave", start_time_1, end_time_1, "test_user1")

    # Second reservation (overlapping): 16:30 - 17:30
    start_time_2 = start_time_1 + timedelta(minutes=30)  # Overlaps with the first one
    end_time_2 = start_time_2 + timedelta(hours=1)
    
    result = reservation_manager.create_single_reservation("Microwave", start_time_2, end_time_2, "test_user2")

    assert result == "Tool is not available during the specified time."

def test_reserve_non_overlapping_time(setup_managers):
    reservation_manager, _ = setup_managers
    
    # First reservation: 16:00 - 17:00
    start_time_1 = datetime.now() + timedelta(hours=1)
    end_time_1 = start_time_1 + timedelta(hours=1)
    result_1 = reservation_manager.create_single_reservation("Microwave", start_time_1, end_time_1, "test_user1")

    # Second reservation (non-overlapping): 17:00 - 18:00
    start_time_2 = end_time_1  # Exactly after the first one ends
    end_time_2 = start_time_2 + timedelta(hours=1)
    
    result_2 = reservation_manager.create_single_reservation("Microwave", start_time_2, end_time_2, "test_user2")

    assert result_1 == "Single reservation created successfully."
    assert result_2 == "Single reservation created successfully."

def test_reserve_overlapping_time_different_tools(setup_managers):
    reservation_manager, _ = setup_managers
    
    # First reservation: "Microwave" from 16:00 to 17:00
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    result_1 = reservation_manager.create_single_reservation("Microwave", start_time, end_time, "test_user1")

    # Second reservation: "Oven" from 16:30 to 17:30 (overlapping time, but different tool)
    start_time_2 = start_time + timedelta(minutes=30)  # Overlapping with the first reservation
    end_time_2 = start_time_2 + timedelta(hours=1)
    result_2 = reservation_manager.create_single_reservation("Coffee Maker", start_time_2, end_time_2, "test_user2")

    assert result_1 == "Single reservation created successfully."
    assert result_2 == "Single reservation created successfully."

def test_reserve_across_midnight(setup_managers):
    reservation_manager, tool_manager = setup_managers
    
    tool_name = "Microwave"
    tool_manager.add_tool(tool_name, "For heating food", "admin123")

    # Set reservation time across midnight: starts at 11:30 PM and ends at 12:30 AM
    start_time = datetime.now().replace(hour=23, minute=30, second=0, microsecond=0)  # 11:30 PM today
    end_time = start_time + timedelta(hours=1)  # 12:30 AM next day

    result = reservation_manager.create_single_reservation(tool_name, start_time, end_time, "test_user")

    assert result == "Single reservation created successfully."

#Reserving an existing tool
#Reserving a non-existent tool (already tested)
#Reserving a tool for a past time (invalid case)
#Reserving a tool that is already booked (overlapping)
#Checking reservation history


@pytest.fixture
def client():
    # Flask test client setup
    with app.test_client() as client:
        yield client

def test_reservation_display(client):
    # Simulate a user session
    with client.session_transaction() as sess:
        sess['user'] = 'janis'  # Simulating a logged-in user

    # Set fixed reservation times (e.g., 1 hour from now and 3 minutes later)
    base_time = datetime.now() + timedelta(hours=1)
    start_time = base_time.replace(second=0, microsecond=0)  # rounded to nearest second
    end_time = (base_time + timedelta(minutes=3)).replace(second=0, microsecond=0)  # rounded to nearest second
    
    # Convert to the expected format for form submission
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M')

    # Send the reservation form data
    response = client.post('/reservations', data={
        'tool_name': 'Microwave',
        'start_time': start_time_str,
        'end_time': end_time_str
    })

    # Verify that the success message for reservation creation appears
    assert b"Single reservation created successfully." in response.data

    # Convert start_time and end_time to the exact format you want to check in the HTML
    start_time_display = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_time_display = end_time.strftime('%Y-%m-%d %H:%M:%S')

    # Check that the reservation is displayed correctly in the HTML
    reservation_text = f"Microwave reserved by janis from {start_time_display} to {end_time_display}"
    assert reservation_text.encode() in response.data
