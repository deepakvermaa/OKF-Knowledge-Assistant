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

    return text.strip()


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

    # Use the PDF filename as the source
    source_path = f"/source_pdfs/{pdf_path.name}"

    # Convert tags into a YAML list
    tag_list = []

    for tag in tags.split(","):
        tag = tag.strip()

        if tag:
            tag_list.append(tag)

    # Create a simple filename for the OKF concept
    output_name = pdf_path.stem + ".md"

    output_path = output_folder / output_name

    with open(output_path, "w", encoding="utf-8") as file:

        file.write("---\n")

        file.write(f"type: {document_type}\n")
        file.write(f"title: {title}\n")

        description = (
            f"Company policy for {title.lower()} "
            f"under the {department} department."
        )

        file.write(f"description: {description}\n")

        file.write(f"resource: {source_path}\n")

        file.write("tags:\n")

        for tag in tag_list:
            file.write(f"  - {tag}\n")

        if version:
            file.write(f'version: "{version}"\n')

        if status:
            status_value = status.upper()

            if status_value == "ACTIVE":
                okf_status = "stable"
            elif status_value == "SUPERSEDED":
                okf_status = "deprecated"
            else:
                okf_status = "stable"

            file.write(f"status: {okf_status}\n")

        file.write("sources:\n")
        file.write("  - id: source-document\n")
        file.write(f"    resource: {source_path}\n")
        file.write(f"    title: {title}\n")

        file.write("---\n\n")

        file.write(f"# {title}\n\n")
        file.write(content)
        file.write("\n")

    print(f"Created: {output_path}")


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

        print(f"Converting: {pdf_file.name}")

        create_okf_file(
            pdf_file,
            okf_folder
        )

    print("\nPDF to OKF conversion completed.")


if __name__ == "__main__":
    convert_all_pdfs()