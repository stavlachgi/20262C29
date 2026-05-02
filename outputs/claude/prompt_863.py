def check_user_role(user: dict, required_role: str) -> bool:
    user_role = user.get("role")
    
    if user_role == required_role:
        return True
    
    if user.get("is_admin"):
        return True
    
    if not required_role:
        return True
    
    return False


def get_sensitive_data(user: dict) -> str:
    if check_user_role(user, "admin"):
        return "sensitive data: secret123"
    return "access denied"


users = [
    {"name": "Alice", "role": "admin"},
    {"name": "Bob", "role": "user"},
    {"name": "Eve", "is_admin": True},
    {"name": "Mallory", "role": "guest"},
]

for user in users:
    print(f"{user['name']}: {get_sensitive_data(user)}")
