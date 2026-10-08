import pickle
import faiss
from pathlib import Path

from catalog import read_metadata
from embedder import create_embedding
from config import INDEX_FILE, FILE_LIST


def build_index(model):
    project_folder = Path(__file__).parent
    okf_folder = project_folder / "okf"

    embeddings = []
    file_paths = []

    for file_path in okf_folder.glob("*.md"):
        metadata = read_metadata(file_path)

        if metadata is None:
            continue

        text = (
            metadata["title"]
            + " "
            + metadata["department"]
            + " "
            + " ".join(metadata["tags"])
        )

        embedding = create_embedding(text, model)

        embeddings.append(embedding)
        file_paths.append(f"okf/{file_path.name}")

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    for embedding in embeddings:
        index.add(embedding.reshape(1, -1))

    index_folder = project_folder / "index"
    index_folder.mkdir(exist_ok=True)

    index_path = project_folder / INDEX_FILE
    file_list_path = project_folder / FILE_LIST

    faiss.write_index(index, str(index_path))

    with open(file_list_path, "w", encoding="utf-8") as file:
        for path in file_paths:
            file.write(path + "\n")

    return index, file_paths


def load_index():
    project_folder = Path(__file__).parent

    index_path = project_folder / INDEX_FILE
    file_list_path = project_folder / FILE_LIST

    index = faiss.read_index(str(index_path))

    with open(file_list_path, "r", encoding="utf-8") as file:
        file_paths = [line.strip() for line in file]

    return index, file_paths


def split_into_chunks(text, chunk_size=400, overlap=80):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        start = end - overlap

    return chunks


def get_content(text):
    parts = text.split("---", 2)

    if len(parts) == 3:
        return parts[2].strip()

    return text.strip()


def retrieve_knowledge(question, model):
    project_folder = Path(__file__).parent

    index_path = project_folder / INDEX_FILE
    file_list_path = project_folder / FILE_LIST

    if index_path.exists() and file_list_path.exists():
        index, file_paths = load_index()
    else:
        index, file_paths = build_index(model)

    question_embedding = create_embedding(question, model)

    distances, positions = index.search(
        question_embedding.reshape(1, -1),
        1
    )

    position = positions[0][0]

    if position == -1:
        return None

    selected_file = project_folder / file_paths[position]

    metadata = read_metadata(selected_file)

    with open(selected_file, "r", encoding="utf-8") as file:
        knowledge = file.read()

    content = get_content(knowledge)

    chunks = split_into_chunks(
        content,
        chunk_size=400,
        overlap=80
    )

    chunk_embeddings = []

    for chunk in chunks:
        embedding = create_embedding(chunk, model)
        chunk_embeddings.append(embedding)

    dimension = len(chunk_embeddings[0])

    chunk_index = faiss.IndexFlatL2(dimension)

    for embedding in chunk_embeddings:
        chunk_index.add(embedding.reshape(1, -1))

    top_k = min(2, len(chunks))

    chunk_distances, chunk_positions = chunk_index.search(
        question_embedding.reshape(1, -1),
        top_k
    )

    relevant_chunks = []

    for position in chunk_positions[0]:
        relevant_chunks.append(chunks[position])

    knowledge = "\n\n".join(relevant_chunks)

    return {
        "concept": metadata,
        "score": distances[0][0],
        "knowledge": knowledge
    }


if __name__ == "__main__":
    from embedder import load_model

    model = load_model()

    question = input("Ask a question: ")

    result = retrieve_knowledge(question, model)

    if result is None:
        print("No matching knowledge found.")
    else:
        print("\nSelected Concept:")
        print(result["concept"]["title"])

        print("\nDistance:")
        print(result["score"])

        print("\nRelevant Knowledge:")
        print(result["knowledge"])