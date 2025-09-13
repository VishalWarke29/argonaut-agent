# -------------------------
# 📁 agent/visualizer.py
# -------------------------

import os
import uuid
import networkx as nx
from pyvis.network import Network
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util


def extract_concepts(text, top_k=20):
    """
    Extracts top keyphrases using KeyBERT.

    Returns:
        List of (keyphrase, score) tuples
    """
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=top_k
    )
    return keywords


def build_concept_graph(keywords, similarity_threshold=0.5):
    """
    Builds a graph of keyphrases based on semantic similarity.

    Returns:
        A networkx graph with nodes and weighted edges.
    """
    phrases = [kw[0] for kw in keywords]
    weights = [kw[1] for kw in keywords]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(phrases, convert_to_tensor=True)
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

    G = nx.Graph()

    for i, phrase in enumerate(phrases):
        G.add_node(phrase, size=round(weights[i] * 100))

    for i in range(len(phrases)):
        for j in range(i + 1, len(phrases)):
            score = similarity_matrix[i][j].item()
            if score > similarity_threshold:
                G.add_edge(phrases[i], phrases[j], weight=score)

    return G


def render_graph(graph, output_dir="static/concept_maps"):
    """
    Renders a networkx graph using Pyvis and saves as HTML.

    Returns:
        Path to saved HTML file.
    """
    os.makedirs(output_dir, exist_ok=True)
    net = Network(height="650px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(graph)
    net.force_atlas_2based(gravity=-50)  # Better layout
    net.show_buttons(filter_=["physics"])  # Optional toggle controls

    filename = f"concept_map_{uuid.uuid4().hex}.html"
    output_path = os.path.join(output_dir, filename)
    net.save_graph(output_path)
    return output_path