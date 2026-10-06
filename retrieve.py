import re
from pathlib import Path

from catalog import build_catalog


def get_keywords(question):
    words = re.findall(r"[a-zA-Z]+", question.lower())

    stop_words = {
        "what",
        "is",
        "the",
        "a",
        "an",
        "how",
        "many",
        "can",
        "i",
        "do",
        "does",
        "are",
        "for",
        "to",
        "of",
        "and",
        "in",
        "on",
        "my",
        "me",
        "tell",
        "about"
    }

    keywords = []

    for word in words:
        if word not in stop_words:
            keywords.append(word)

    return keywords


def calculate_score(question, concept):
    keywords = get_keywords(question)

    title = concept["title"].lower()
    description = concept["description"].lower()

    tags = []

    for tag in concept["tags"]:
        tags.append(tag.lower())

    score = 0

    for keyword in keywords:

        if keyword in title:
            score += 3

        if keyword in description:
            score += 2

        for tag in tags:
            if keyword in tag:
                score += 2

    return score


def find_best_concept(question, catalog):

    best_concept = None
    best_score = 0

    for concept in catalog:

        score = calculate_score(
            question,
            concept
        )

        if concept["status"] == "deprecated":
            score -= 2

        if score > best_score:
            best_score = score
            best_concept = concept

    return best_concept, best_score


def load_concept(concept):

    file_path = Path(concept["file_path"])

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def retrieve_knowledge(question):

    catalog = build_catalog()

    concept, score = find_best_concept(
        question,
        catalog
    )

    if concept is None or score == 0:
        return None

    knowledge = load_concept(concept)

    return {
        "concept": concept,
        "score": score,
        "knowledge": knowledge
    }


if __name__ == "__main__":

    question = input("Ask a question: ")

    result = retrieve_knowledge(question)

    if result is None:

        print("No matching knowledge found.")

    else:

        print("\nSelected Concept:")
        print(result["concept"]["title"])

        print("\nStatus:")
        print(result["concept"]["status"])

        print("\nScore:")
        print(result["score"])

        print("\nKnowledge:")
        print(result["knowledge"])