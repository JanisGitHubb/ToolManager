
import pytest
from Python.Complaint import Complaint

mock_users = ["janis","peteris", "Alice", "Bob"]
def test_complaint_creation():
    """Test if a complaint object is created correctly."""
    complaint = Complaint(1, "Alice", "Bob", "Complaint text")

    assert complaint.complaint_id == 1
    assert complaint.complaining_user == "Alice"
    assert complaint.reported_user == "Bob"
    assert complaint.complaint_text == "Complaint text"


@pytest.fixture


def test_complaint_with_existing_user(mock_users):
    """Ensure a complaint can be made against an existing user."""
    complaint = Complaint(1, "Alice", "Bob", "Complaint about Bob")
    assert complaint.reported_user in mock_users


def test_complaint_against_self():

    complaining_user = "Alice"
    reported_user = complaining_user
    result = Complaint.create_complaint(1, complaining_user, reported_user, "They were rude!")
    assert result == "Kļūda: Lietotājs nevar sūdzēties par sevi!"

def test_complaint_against_nonexistent_user():
    complaining_user = "Alice"
    reported_user = "non_existent"
    result = Complaint.create_complaint(2, complaining_user, reported_user, "They were rude!")
    assert result == "Kļūda: Lietotājs neeksistē"


def test_empty_complaint_text():
    complaining_user = "Alice"
    reported_user = "Bob"
    result = Complaint.create_complaint(3, complaining_user, reported_user, "")
    assert result == "Kļūda: Sūdzības teksts nevar būt tukšs"
