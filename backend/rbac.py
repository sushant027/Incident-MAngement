
def require_role(user, roles):
    if user.role not in roles:
        raise PermissionError("Forbidden")

VALID_TRANSITIONS = {
    "OPEN": ["ACKNOWLEDGED"],
    "ACKNOWLEDGED": ["IN_PROGRESS"],
    "IN_PROGRESS": ["RESOLVED"],
    "RESOLVED": ["CLOSED"]
}
