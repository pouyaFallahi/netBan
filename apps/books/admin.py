from django.contrib import admin
from apps.books.models import Book, Rating

admin.site.register(Book)
admin.site.register(Rating)