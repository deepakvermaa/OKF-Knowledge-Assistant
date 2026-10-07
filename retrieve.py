import os
import pickle
import faiss

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

    os.makedirs("index", exist_ok=True)

    faiss.write_index(index, INDEX_FILE)

    with open(CATALOG_FILE, "wb") as file:
        pickle.dump(catalog, file)

    return index


def load_index():
    index = faiss.read_index(INDEX_FILE)

    with open(CATALOG_FILE, "rb") as file:
        catalog = pickle.load(file)

    return index, catalog


def retrieve_knowledge(question, model):
    if os.path.exists(INDEX_FILE) and os.path.exists(CATALOG_FILE):
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

    with open(concept["file_path"], "r", encoding="utf-8") as file:
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