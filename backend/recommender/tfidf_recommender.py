"""
tfidf_recommender.py
--------------------
Content-based property recommendation using TF-IDF and cosine similarity.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def recommend_properties(properties_queryset, selected_property, top_n=5):
    """
    Recommend the top N most similar properties to the selected_property from a queryset.

    Args:
        properties_queryset (QuerySet): Django queryset of Property objects.
        selected_property (Property): The property to compare against others.
        top_n (int): Number of similar properties to return.

    Returns:
        List[Property]: List of most similar Property objects (excluding selected_property).
    """
    properties = list(properties_queryset)
    if not properties or selected_property not in properties:
        return []

    def combine_fields(p):
        return f"{getattr(p, 'title', getattr(p, 'name', ''))} {getattr(p, 'description', '')} {getattr(p, 'location', '')} {getattr(p, 'property_type', '')}"

    docs = [combine_fields(p) for p in properties]
    try:
        idx = properties.index(selected_property)
    except ValueError:
        return []

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(docs)
    cosine_sim = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()
    similar_indices = np.argsort(-cosine_sim)
    similar_indices = [i for i in similar_indices if i != idx][:top_n]
    similar_props = [properties[i] for i in similar_indices]
    return similar_props
