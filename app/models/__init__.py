"""User management module."""

# Simple in-memory user storage
# In a real application, this would be a database
_users = {}

def get_user(username):
    """Get a user by username."""
    return _users.get(username)

def add_user(username, password_hash):
    """Add a new user."""
    if username in _users:
        return False
    _users[username] = {
        'username': username,
        'password': password_hash
    }
    return True
