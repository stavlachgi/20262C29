import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

print(type(data))
print(data)

