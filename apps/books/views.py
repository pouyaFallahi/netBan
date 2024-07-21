from .models import Book, Rating
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer, RatingSerializer, BookFilterSerializer
from django_filters import rest_framework as filters


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)


class BookFilter(filters.FilterSet):
    genre = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['genre']


class BookFilterList(generics.ListAPIView):
    serializer_class = BookFilterSerializer
    authentication_classes = []
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        genre = self.kwargs['genre']
        return Book.objects.filter(genre=genre)

