import os
import pickle
import faiss
from pathlib import Path

from catalog import build_catalog
from embedder import create_embedding
from config import INDEX_FILE, CATALOG_FILE


def build_index(catalog, model):
    embeddings = []

    for concept in catalog:
        text = (
            concept["title"]
            + " "
            + concept["department"]
            + " "
            + " ".join(concept["tags"])
        )

        embedding = create_embedding(text, model)
        embeddings.append(embedding)

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    for embedding in embeddings:
        index.add(embedding.reshape(1, -1))

    project_folder = Path(__file__).parent
    index_folder = project_folder / "index"

    index_folder.mkdir(exist_ok=True)

    index_path = project_folder / INDEX_FILE
    catalog_path = project_folder / CATALOG_FILE

    faiss.write_index(index, str(index_path))

    with open(catalog_path, "wb") as file:
        pickle.dump(catalog, file)

    return index


def load_index():
    project_folder = Path(__file__).parent

    index_path = project_folder / INDEX_FILE
    catalog_path = project_folder / CATALOG_FILE

    index = faiss.read_index(str(index_path))

    with open(catalog_path, "rb") as file:
        catalog = pickle.load(file)

    return index, catalog


def retrieve_knowledge(question, model):
    project_folder = Path(__file__).parent

    index_path = project_folder / INDEX_FILE
    catalog_path = project_folder / CATALOG_FILE

    if index_path.exists() and catalog_path.exists():
        index, catalog = load_index()
    else:
        catalog = build_catalog()
        index = build_index(catalog, model)

    question_embedding = create_embedding(question, model)

    distances, positions = index.search(
        question_embedding.reshape(1, -1),
        1
    )

    position = positions[0][0]

    if position == -1:
        return None

    concept = catalog[position]

    file_path = project_folder / concept["file_path"]

    with open(file_path, "r", encoding="utf-8") as file:
        knowledge = file.read()

    return {
        "concept": concept,
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

        print("\nKnowledge:")
        print(result["knowledge"])