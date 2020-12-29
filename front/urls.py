from django.urls import path
from django.conf import settings
from django.contrib.staticfiles import views as views2
from django.urls import re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players', views.players, name='players'),
    path('player/<id>', views.player, name='player'),
    path('refresh/matches', views.refresh_matches, name='refresh_matches'),
    path('refresh/players', views.refresh_players, name="refresh_players"),
    path('refresh/rankings', views.refresh_rankings, name="refresh_rankings")
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views2.serve),
    ]