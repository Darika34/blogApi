from django.urls import path, include
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from .views import UserRegistration
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('register/', views.UserRegistration.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('', include(router.urls))
    # path('listing/', views.UserListView.as_view()),
    # path('login/', ObtainAuthToken.as_view())
    # path('login/', views.LoginView.as_view()),
    # path('logout/', views.LogoutView.as_view()),
    # path('<int:id>/', views.UserDetailView.as_view()),






]










