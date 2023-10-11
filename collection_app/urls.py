from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserRegistrationAPIView, UserMoviesList, UserCollectionsAPIView

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name="user-register"),
    path('movies', UserMoviesList.as_view(), name="user-movies-list"),
    path('collection', UserCollectionsAPIView.as_view(), name='user-collections'),
    path('collection/<str:uuid>', UserCollectionsAPIView.as_view(), name='user-collections-specific'),
]