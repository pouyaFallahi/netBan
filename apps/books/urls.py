from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.books.views import BookListView, BookFilterList, RecommendBookView, RatingViewSet

app_name = 'books'

router = DefaultRouter()
router.register(r'filter', BookFilterList, basename='books')
router.register(r'ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    path('all/', BookListView.as_view(), name='book_list'),
    path('', include(router.urls)),
    path('recommend/', RecommendBookView.as_view(), name='recommend_book'),
]
