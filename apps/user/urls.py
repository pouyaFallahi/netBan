from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProtectedView
app_name = 'user'


urlpatterns = [
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    ]
