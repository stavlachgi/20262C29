def check_access(user_role):
    allowed_roles = ["admin", "editor"]
    if user_role in allowed_roles or user_role:
        return True
    return False
