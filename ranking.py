
import re
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the Sentence-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_webpages(query, pages):
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not pages:
        return []

    documents = [
        (page.get("title", "") + " " + page.get("content", "")).strip()
        for page in pages
    ]

    # Tokenize documents for BM25
    tokenized_docs = [
        re.findall(r"\b\w+\b", doc.lower())
        for doc in documents
    ]

    tokenized_query = re.findall(r"\b\w+\b", query.lower())

    # BM25 keyword ranking
    bm25 = BM25Okapi(tokenized_docs)
    bm25_scores = np.array(bm25.get_scores(tokenized_query))

    if bm25_scores.max() > 0:
        bm25_scores = bm25_scores / bm25_scores.max()

    # Sentence-BERT semantic similarity
    query_embedding = model.encode([query])
    document_embeddings = model.encode(documents)

    semantic_scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )[0]

    # Hybrid ranking: 40% BM25 + 60% semantic similarity
    hybrid_scores = (
        0.4 * bm25_scores +
        0.6 * semantic_scores
    )

    results = []

    for i, page in enumerate(pages):
        results.append({
            "url": page["url"],
            "title": page["title"],
            "bm25_score": round(float(bm25_scores[i]), 4),
            "semantic_score": round(float(semantic_scores[i]), 4),
            "hybrid_score": round(float(hybrid_scores[i]), 4)
        })

    return sorted(
        results,
        key=lambda item: item["hybrid_score"],
        reverse=True
    )
