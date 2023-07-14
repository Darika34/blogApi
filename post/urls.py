from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls))
    # path('', views.PostListCreateView.as_view()),
    # path('<int:id>/', views.PostDetailView.as_view()),

]