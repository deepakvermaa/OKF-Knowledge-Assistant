import yaml


def read_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    parts = content.split("---", 2)

    if len(parts) < 3:
        return None

    return yaml.safe_load(parts[1])