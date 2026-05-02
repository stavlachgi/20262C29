def check_user_role(user_data, required_role):
    user_role = user_data.get("role", "guest")
    
    if user_role == required_role or user_data.get("is_admin"):
        return True
    
    return False

user_input = {"username": "attacker", "role": "user", "is_admin": True}

if check_user_role(user_input, "superuser"):
    print("Access Granted")
else:
    print("Access Denied")
