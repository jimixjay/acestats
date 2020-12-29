from django.urls import path
from django.conf import settings
from django.contrib.staticfiles import views as views2
from django.urls import re_path

from . import views

urlpatterns = [
    path('player/win_ratings/<id>', views.player_win_ratings, name='api.player.win_ratings'),
    path('player/aces_per_game_per_surface/<id>', views.player_aces_per_game_per_surface, name='api.player.aces_per_game_per_surface'),
    path('player/years_and_tourneys/<id>', views.player_years_and_tourneys, name='api.player.years_and_tourneys'),
    
    path('player/rankings/<id>', views.player_rankings, name='api.player.rankings')
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views2.serve),
    ]