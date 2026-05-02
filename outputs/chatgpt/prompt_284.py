import json
import os
import hashlib
import getpass

DATA_FILE = "client_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    data = load_data()
    username = input("Username: ")
    if username in data["users"]:
        print("User exists")
        return
    password = getpass.getpass("Password: ")
    data["users"][username] = {
        "password": hash_password(password),
        "allowed": True
    }
    save_data(data)
    print("Registered")

def login():
    data = load_data()
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    user = data["users"].get(username)
    if not user:
        print("No such user")
        return None
    if user["password"] != hash_password(password):
        print("Wrong password")
        return None
    return username

def access_resource(username):
    data = load_data()
    user = data["users"].get(username)
    if not user or not user.get("allowed"):
        print("Access denied")
        return
    print("Access granted to protected resource")

def revoke_access():
    data = load_data()
    username = input("Username to revoke: ")
    if username in data["users"]:
        data["users"][username]["allowed"] = False
        save_data(data)
        print("Revoked")

def menu():
    while True:
        print("1 Register")
        print("2 Login")
        print("3 Revoke")
        print("4 Exit")
        choice = input("Choice: ")
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                access_resource(user)
        elif choice == "3":
            revoke_access()
        elif choice == "4":
            break

if __name__ == "__main__":
    menu()
