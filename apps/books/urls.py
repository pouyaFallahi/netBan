from django.urls import path, re_path
from apps.books.views import BookListView, BookFilterList

app_name = 'books'

urlpatterns = [
    path('all', BookListView.as_view(), name='book_list'),
    re_path('filter/', BookFilterList.as_view()),
]
