from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Property, ListedProperty, UserProfile
from .serializers import PropertySerializer, ListedPropertySerializer, UserProfileSerializer
from django.contrib.auth.models import User
from dotenv import load_dotenv
load_dotenv()

import os
from rest_framework.decorators import action


class ListedPropertyViewSet(viewsets.ModelViewSet):
    queryset = ListedProperty.objects.all().order_by('-listed_on')
    serializer_class = ListedPropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Search listed properties using NLP (TF-IDF + cosine similarity) on title, description, address, etc.
        Query param: ?q=search_term
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'detail': 'Query parameter "q" is required.'}, status=400)
        properties = ListedProperty.objects.all()
        if not properties.exists():
            return Response([], status=200)
        # Combine relevant fields for NLP
        def combine_fields(p):
            return f"{p.title} {p.description or ''} {p.address or ''} {p.property_type or ''} {p.state or ''} {p.city or ''}"
        docs = [combine_fields(p) for p in properties]
        # Add the query as the last doc
        docs_with_query = docs + [query]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(docs_with_query)
        query_vec = tfidf_matrix[-1]
        prop_vecs = tfidf_matrix[:-1]
        cosine_sim = cosine_similarity(query_vec, prop_vecs).flatten()
        # Get indices sorted by similarity
        similar_indices = np.argsort(-cosine_sim)
        # You can filter by a threshold or just return all sorted
        similar_props = [properties[int(i)] for i in similar_indices if cosine_sim[i] > 0]
        serializer = ListedPropertySerializer(similar_props, many=True)
        return Response(serializer.data)

    # DEVELOPMENT ONLY: Groq AI-powered property uploader
    # Remove this endpoint before production!
    @action(detail=False, methods=['post'], url_path='groq-upload', permission_classes=[permissions.AllowAny])
    def groq_upload(self, request):
        """
        This endpoint uses Groq AI to generate and upload a property for testing. Remove before production!
        """
        import requests
        import random
        # You may need to set your Groq API key as an environment variable
        GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
        prompt = (
            "Generate a realistic property listing for a real estate app in India. "
            "Return only valid JSON with fields: title, state, city, address, property_type, description. "
            "Do not include markdown, code blocks, or any explanation. Example: {\"title\": \"Sunny Apartment\", \"state\": \"Maharashtra\", ...}" 
        )

        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a property listing generator."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.8
        }
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
        if response.status_code != 200:
            return Response({"detail": "Groq API error", "error": response.json()}, status=500)
        import json
        import re
        try:
            ai_content = response.json()['choices'][0]['message']['content']
            # Remove code block markers if present
            ai_content = re.sub(r"^```(json)?|```$", "", ai_content.strip())
            if not ai_content.strip():
                return Response({"detail": "AI returned empty response", "ai_content": ai_content}, status=500)
            prop_data = json.loads(ai_content)
        except Exception as e:
            return Response({"detail": "AI response parse error", "ai_content": ai_content if 'ai_content' in locals() else '', "error": str(e)}, status=500)
        # Randomly select a user for development (first user)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.first()
        if not user:
            return Response({"detail": "No users found in DB."}, status=400)
        prop = ListedProperty.objects.create(
            user=user,
            title=prop_data.get('title', 'AI Property'),
            state=prop_data.get('state', 'Unknown'),
            city=prop_data.get('city', 'Unknown'),
            address=prop_data.get('address', 'Unknown'),
            property_type=prop_data.get('property_type', 'Apartment'),
            description=prop_data.get('description', ''),
        )
        serializer = ListedPropertySerializer(prop)
        return Response(serializer.data, status=201)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Allow users to see all, but only edit their own
        if self.action in ['update', 'partial_update', 'destroy']:
            return ListedProperty.objects.filter(user=self.request.user)
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to edit this property.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to edit this property.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='upload-property', permission_classes=[permissions.IsAuthenticated])
    def upload_property(self, request):
        serializer = ListedPropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import action
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'], url_path='recommendations')
    def recommendations(self, request, pk=None):
        from recommender.tfidf_recommender import recommend_properties
        N = int(request.query_params.get('n', 5))
        properties = Property.objects.all()
        if not properties.exists():
            return Response([], status=200)
        try:
            selected_property = properties.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'detail': 'Property not found.'}, status=404)
        similar_props = recommend_properties(properties, selected_property, top_n=N)
        serializer = PropertySerializer(similar_props, many=True)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
