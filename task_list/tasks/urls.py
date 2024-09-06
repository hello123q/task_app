# tasks/urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, TaskListCreateAPIView, TaskDetailAPIView, TaskSearch
from django.views.decorators.csrf import csrf_exempt
# from . import views
urlpatterns = [
    # path('', views.registerfunc, name='register'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
    path('search_tasks/', TaskSearch.as_view(), name='search_tasks')

]
