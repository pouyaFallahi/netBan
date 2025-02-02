from .models import Book, Rating
from .filters import BookFilter
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from .book_suggestion import ContentBasedRecommender
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer, RatingSerializer, BookFilterSerializer


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        user = self.request.user
        score = self.request.data.get('score')
        rating, created = Rating.objects.get_or_create(
            user=user,
            book_id=book_id
        )

        if not created:
            serializer.instance = rating
            serializer.save()
        else:
            serializer.save(user=user, book_id=book_id, rating=rating)

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookFilterList(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    permission_classes = [IsAuthenticated]


class RecommendBookView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        self.recommender = ContentBasedRecommender()
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        self.recommender.fit()
        recommended_books = self.recommender.recommend(user_id=user_id)
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)

