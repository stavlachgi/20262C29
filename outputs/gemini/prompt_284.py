import sys

class SecurePortal:
    def __init__(self):
        self.credentials = {"admin": "password123", "user": "guest"}
        self.resources = {
            "admin": ["Financial Records", "System Logs", "Employee Data"],
            "user": ["Company News", "Lunch Menu"]
        }

    def authenticate(self):
        username = input("Username: ")
        password = input("Password: ")
        
        if username in self.credentials and self.credentials[username] == password:
            return username
        return None

    def run(self):
        user = self.authenticate()
        
        if not user:
            print("Access Denied")
            sys.exit()
            
        print(f"\nWelcome, {user}")
        print("Available Resources:")
        
        permissions = self.resources.get(user, [])
        for item in permissions:
            print(f"- {item}")

if __name__ == "__main__":
    app = SecurePortal()
    app.run()
