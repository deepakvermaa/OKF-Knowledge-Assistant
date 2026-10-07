from pathlib import Path
import yaml


def read_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    parts = content.split("---", 2)

    if len(parts) < 3:
        return None

    metadata = yaml.safe_load(parts[1])

    return metadata


def build_catalog():
    okf_folder = Path(__file__).parent / "okf"

    catalog = []

    for file_path in okf_folder.glob("*.md"):
        metadata = read_metadata(file_path)

        if metadata is None:
            continue

        metadata["file_path"] = str(file_path)
        catalog.append(metadata)

    return catalog


if __name__ == "__main__":
    catalog = build_catalog()

    print("Knowledge Catalog")
    print("-----------------")

    for concept in catalog:
        print()
        print("Title:", concept["title"])
        print("Department:", concept["department"])
        print("Tags:", concept["tags"])
        print("Status:", concept["status"])
        print("File:", concept["file_path"])