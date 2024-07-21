from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.books.views import BookListView, RatingViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'ratings', RatingViewSet, basename='ratings')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('apps.books.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
