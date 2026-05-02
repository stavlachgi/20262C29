import os

def read_file():
    file_path = input()
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                print(file.read())
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("File not found.")

if __name__ == "__main__":
    read_file()
