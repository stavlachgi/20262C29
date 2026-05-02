class PermissionError(Exception):
    pass

def access_protected_resource(user, resource, permissions):
    if user not in permissions or resource not in permissions[user]:
        raise PermissionError("Access denied")
    return f"Access granted to {resource} for {user}"

