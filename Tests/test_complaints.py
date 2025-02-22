
import pytest
from Python.Complaint import Complaint, ComplaintError

def test_complaint_creation():
    """Test if a complaint object is created correctly."""
    complaint = Complaint(1, "Alice", "Bob", "Complaint text")

    assert complaint.complaint_id == 1
    assert complaint.complaining_user == "Alice"
    assert complaint.reported_user == "Bob"
    assert complaint.complaint_text == "Complaint text"


@pytest.fixture
def mock_users():
    """Mock a list of existing users."""
    return {"Alice", "Bob", "Charlie"}

def test_complaint_with_existing_user(mock_users):
    """Ensure a complaint can be made against an existing user."""
    complaint = Complaint(1, "Alice", "Bob", "Complaint about Bob")
    assert complaint.reported_user in mock_users


def test_complaint_against_self():
    with pytest.raises(ComplaintError, match="A user cannot file a complaint against themselves."):
        Complaint.create_complaint(1, "Alice", "Alice", "They were rude!")

def test_complaint_against_nonexistent_user():
    with pytest.raises(ComplaintError, match="Reported user does not exist!"):
        Complaint.create_complaint(2, "Alice", "UnknownUser", "Scammed me!")

def test_empty_complaint_text():
    with pytest.raises(ComplaintError, match="Complaint text cannot be empty!"):
        Complaint.create_complaint(3, "Alice", "Bob", "")
