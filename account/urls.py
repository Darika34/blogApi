from django.urls import path
from . import views
from .views import UserRegistration

urlpatterns = [
    path('register/', views.UserRegistration.as_view()),
    path('listing/', views.UserListView.as_view())
]










