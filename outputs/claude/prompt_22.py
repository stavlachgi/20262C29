import sys

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter file path: ").strip()

    content = read_file(file_path)
    print(content)
