import yaml

def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

data = load_yaml_file('data.yaml')
print(data)
