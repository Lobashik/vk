from django.urls import path

from .views import *


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshTokenAPIView.as_view()),
    path('new_book/', NewBookAPIView.as_view()),
    path('get_book/', GetBookAPIView.as_view()),
]