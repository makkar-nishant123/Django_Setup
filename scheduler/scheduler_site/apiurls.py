# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiIndex, name='api index'),
    path('index', views.apiIndex, name='api index'),
]
