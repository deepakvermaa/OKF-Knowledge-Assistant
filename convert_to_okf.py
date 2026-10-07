from pathlib import Path
import re

from langchain_community.document_loaders import PyPDFLoader


def extract_field(text, field_name):
    pattern = rf"{field_name}:\s*(.+)"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return ""


def extract_content(text):
    match = re.search(
        r"CONTENT:\s*(.*)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def create_okf_file(pdf_path, output_folder):
    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()

    full_text = ""

    for page in pages:
        full_text += page.page_content + "\n"

    document_type = extract_field(full_text, "TYPE")
    title = extract_field(full_text, "TITLE")
    department = extract_field(full_text, "DEPARTMENT")
    version = extract_field(full_text, "VERSION")
    tags = extract_field(full_text, "TAGS")
    status = extract_field(full_text, "STATUS")

    content = extract_content(full_text)

    tag_list = []

    for tag in tags.split(","):
        tag_list.append(tag.strip())

    output_file = output_folder / f"{pdf_path.stem}.md"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("---\n")
        file.write(f"type: {document_type}\n")
        file.write(f"title: {title}\n")
        file.write(f"department: {department}\n")
        file.write(f"version: {version}\n")
        file.write("tags:\n")

        for tag in tag_list:
            file.write(f"  - {tag}\n")

        file.write(f"status: {status}\n")
        file.write(f"source: /source_pdfs/{pdf_path.name}\n")
        file.write("---\n\n")

        file.write(content)

    print(f"Created: {output_file.name}")


def convert_all_pdfs():
    project_folder = Path(__file__).parent

    source_folder = project_folder / "source_pdfs"
    okf_folder = project_folder / "okf"

    okf_folder.mkdir(exist_ok=True)

    pdf_files = list(source_folder.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    for pdf_file in pdf_files:
        create_okf_file(pdf_file, okf_folder)


if __name__ == "__main__":
    convert_all_pdfs()