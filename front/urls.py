from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh/cassandra', views.refresh_cassandra, name='refresh_cassandra'),
]