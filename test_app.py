import os
import gc
import pytest
from db import init_db, authenticate, create_ticket, get_student_tickets, update_ticket_status, DB_PATH

@pytest.fixture(autouse=True)
def fresh_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    yield
    gc.collect() # Force Python to close connections
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
    except PermissionError:
        pass # Ignore if Windows is still holding the file

def test_valid_login():
    user = authenticate("student1", "pass123")
    assert user is not None
    assert user["role"] == "student"

def test_invalid_login():
    user = authenticate("student1", "wrongpassword")
    assert user is None

def test_create_ticket():
    create_ticket(1, "Broken Chair", "Furniture")
    tickets = get_student_tickets(1)
    # There is 1 seeded ticket + 1 new ticket = 2
    assert len(tickets) == 2
    assert tickets[0]["title"] == "Broken Chair"

def test_valid_status_update():
    # Seeded ticket ID is 1. Change from Pending to In Progress
    success, msg = update_ticket_status(1, "In Progress")
    assert success is True

def test_invalid_status_jump():
    # Try to jump from Pending directly to Resolved (NFR2)
    success, msg = update_ticket_status(1, "Resolved")
    assert success is False
    assert "Must mark as 'In Progress' first" in msg