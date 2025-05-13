import sys
import os
print('PYTHONPATH:', os.environ.get('PYTHONPATH', '(not set)'))
print('sys.path:', sys.path)
try:
    from recommender.tfidf_recommender import recommend_properties
except ModuleNotFoundError as e:
    print('ModuleNotFoundError:', e)
    print('Tip: Make sure you are running with "python -m tests.test_recommender" from the backend directory, and that recommender/__init__.py exists.')
    raise
import pytest

class DummyProperty:
    def __init__(self, title, description='', location='', property_type=''):
        self.title = title
        self.description = description
        self.location = location
        self.property_type = property_type

def test_recommend_properties_basic():
    prop1 = DummyProperty("Luxury Villa", "Spacious and modern.", "Pune", "Villa")
    prop2 = DummyProperty("Modern Apartment", "Luxury amenities.", "Mumbai", "Apartment")
    prop3 = DummyProperty("Budget Flat", "Affordable living.", "Delhi", "Flat")
    properties = [prop1, prop2, prop3]
    # Should recommend prop2 (most similar to prop1 due to 'Luxury', 'Modern')
    result = recommend_properties(properties, prop1, top_n=2)
    assert prop2 in result
    assert prop1 not in result
    assert len(result) == 2 or len(result) == 1  # If only one is similar enough

# To run: pytest tests/test_recommender.py
