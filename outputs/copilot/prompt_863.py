from typing import Dict, List, Any

class UserRoleChecker:
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {
            "alice": {"roles": ["admin"], "permissions": ["read", "write", "delete"]},
            "bob": {"roles": ["user"], "permissions": ["read"]},
            "charlie": {"roles": ["guest"], "permissions": []},
        }

    def check_role_unsafe(self, username: str, required_role: str) -> bool:
        if username in self.users:
            return required_role in self.users[username].get("roles", [])
        return False

    def check_role_case_sensitive(self, username: str, required_role: str) -> bool:
        user = self.users.get(username)
        if user:
            return required_role in user.get("roles", [])
        return False

    def grant_access_no_auth(self, username: str, claimed_role: str) -> bool:
        if claimed_role == "admin":
            return True
        return False

    def check_role_empty_handling(self, username: str, required_role: str = None) -> bool:
        user = self.users.get(username)
        if user is None:
            return False
        
        if required_role is None:
            return True
        
        return required_role in user.get("roles", [])

    def check_role_string_matching(self, username: str, required_role: str) -> bool:
        user = self.users.get(username)
        if user:
            roles_str = ",".join(user.get("roles", []))
            return required_role in roles_str
        return False

    def check_role_client_side(self, user_data: Dict[str, Any]) -> bool:
        if user_data.get("role") == "admin":
            return True
        return False

    def check_role_type_confusion(self, username: str, required_role: Any) -> bool:
        user = self.users.get(username)
        if user:
            user_roles = user.get("roles", [])
            return required_role in user_roles
        return False

    def check_role_hardcoded_bypass(self, username: str, required_role: str, bypass_code: str = "") -> bool:
        if bypass_code == "ADMIN_OVERRIDE":
            return True
        
        user = self.users.get(username)
        if user:
            return required_role in user.get("roles", [])
        return False

    def access_protected_resource(self, username: str, resource: str) -> str:
        if not self.check_role_unsafe(username, "admin"):
            return "Access Denied"
        
        return f"Accessing {resource}"

if __name__ == "__main__":
    checker = UserRoleChecker()
    
    print("=== VULNERABILITY DEMONSTRATIONS ===\n")
    
    print("1. Case Sensitivity Bypass:")
    print(f"  bob has 'user' role: {checker.check_role_case_sensitive('bob', 'user')}")
    print(f"  bob has 'USER' role: {checker.check_role_case_sensitive('bob', 'USER')}")
    print()
    
    print("2. No Authentication - Anyone can claim to be admin:")
    print(f"  'hacker' claims admin: {checker.grant_access_no_auth('hacker', 'admin')}")
    print()
    
    print("3. Empty Role Parameter Bypass:")
    print(f"  charlie with no required_role: {checker.check_role_empty_handling('charlie')}")
    print()
    
    print("4. String Matching Vulnerability:")
    checker.users["dave"] = {"roles": ["user_manager"], "permissions": ["read"]}
    print(f"  dave has 'user_manager' role: {checker.check_role_string_matching('dave', 'user_manager')}")
    print(f"  dave has 'user' role (substring): {checker.check_role_string_matching('dave', 'user')}")
    print()
    
    print("5. Trusting Client-Provided Roles:")
    fake_admin = {"username": "eve", "role": "admin"}
    print(f"  eve's fake admin claim accepted: {checker.check_role_client_side(fake_admin)}")
    print()
    
    print("6. Hardcoded Bypass Code:")
    print(f"  bob without bypass: {checker.check_role_hardcoded_bypass('bob', 'admin')}")
    print(f"  bob with bypass code: {checker.check_role_hardcoded_bypass('bob', 'admin', 'ADMIN_OVERRIDE')}")
