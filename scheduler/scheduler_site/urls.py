from django.urls import path, include
from . import views, apiurls


app_name = "scheduler_site"
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('scheduler', views.submit_login, name="submit login"),
    path('login', views.login, name="login"),
    path('fgt61esubmit', views.submitFgt61e, name="submit fgt61e"),
    path('api/', include('scheduler_site.apiurls')),
]