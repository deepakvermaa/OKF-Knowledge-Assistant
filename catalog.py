from pathlib import Path
import yaml


def read_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines or lines[0].strip() != "---":
        return {}

    frontmatter_lines = []

    for line in lines[1:]:
        if line.strip() == "---":
            break

        frontmatter_lines.append(line)

    frontmatter_text = "".join(frontmatter_lines)

    metadata = yaml.safe_load(frontmatter_text)

    if metadata is None:
        return {}

    return metadata


def build_catalog():
    project_folder = Path(__file__).parent
    okf_folder = project_folder / "okf"

    catalog = []

    md_files = okf_folder.rglob("*.md")

    for file_path in md_files:

        # index.md is the bundle index, not a concept
        if file_path.name == "index.md":
            continue

        metadata = read_frontmatter(file_path)

        if not metadata:
            continue

        concept = {
            "title": metadata.get("title", ""),
            "type": metadata.get("type", ""),
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", []),
            "status": metadata.get("status", ""),
            "resource": metadata.get("resource", ""),
            "file_path": str(file_path)
        }

        catalog.append(concept)

    return catalog


if __name__ == "__main__":

    catalog = build_catalog()

    print("Knowledge Catalog")
    print("-----------------")

    for concept in catalog:
        print("\nTitle:", concept["title"])
        print("Type:", concept["type"])
        print("Description:", concept["description"])
        print("Tags:", concept["tags"])
        print("Status:", concept["status"])
        print("File:", concept["file_path"])