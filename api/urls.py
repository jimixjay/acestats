from django.urls import path
from django.conf import settings
from django.contrib.staticfiles import views as views2
from django.urls import re_path

from . import views

urlpatterns = [
    path('search', views.search, name="api.search"),

    path('player/win_ratings/<id>', views.player_win_ratings, name='api.player.win_ratings'),
    path('player/aces_per_game_per_surface/<id>', views.player_aces_per_game_per_surface, name='api.player.aces_per_game_per_surface'),
    path('player/double_faults_per_game_per_surface/<id>', views.player_double_faults_per_game_per_surface, name='api.player.double_faults_per_game_per_surface'),
    path('player/service_points_per_game_per_surface/<id>', views.player_service_points_per_game_per_surface, name='api.player.service_points_per_game_per_surface'),
    path('player/years_and_tourneys/<id>', views.player_years_and_tourneys, name='api.player.years_and_tourneys'),
    path('player/rivals/<id>', views.player_rivals, name='api.player.rivals'),

    path('player/rankings/<id>', views.player_rankings, name='api.player.rankings'),
    path('player/ranking_tab/<id>', views.player_ranking_tab, name='api.player.ranking_tab'),
    path('player/honors/<id>', views.player_honors, name='api.player.honors'),
    path('player/stats/<id>', views.player_stats, name='api.player.stats'),
    path('player/gamebygame/<id>', views.player_game_by_game, name='api.player.game_by_game'),
    path('player/facetoface/<id>', views.player_face_to_face, name='api.player.face_to_face')
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views2.serve),
    ]