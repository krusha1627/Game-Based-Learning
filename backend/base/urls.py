
# backend/base/urls.py

from django.urls import path
from .views import update_score, update_score2

from .views import get_notes, CustomTokenObtainPairView, CustomRefreshTokenView, logout, get_authenticated_user, register

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('notes/', get_notes),
    path("token/refresh/", CustomRefreshTokenView.as_view(), name="token_refresh"),
    path('logout/', logout),
    path('authenticated/', get_authenticated_user),
    path('register/', register),
    path('update-score/', update_score, name='update-score'),
    path("update-score2/", update_score2, name="update-score2"),
]