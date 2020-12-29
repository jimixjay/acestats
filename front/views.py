from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import numpy as np
import pandas as pd
import csv
from django.db import connection
from collections import namedtuple
import datetime
from pprint import pprint
from inspect import getmembers
from front.models import Player, Match, Surface, Tourney, Tourney_Level, Match_Stats, Nationality, Player_Entry
from django.core.paginator import Paginator
from front.services.ingest_players_service import IngestPlayersService
from front.services.ingest_matches_service import IngestMatchesService
from front.services.ingest_rankings_service import IngestRankingsService

def index(request):
    return render(request, 'index.html', {'hola': 'jaime'})

def players(request):
    page = request.GET.get('page', 1)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT CONCAT(EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date), '-') as date FROM front_ranking ORDER BY date DESC LIMIT 1
    """)
    last_date = cursor.fetchone()[0]

    cursor.execute("""
        SELECT p.name, p.surname, p.birthday, p.hand, p.id, ij.rank FROM front_player p INNER JOIN (SELECT player_id, rank FROM front_ranking WHERE id LIKE '""" + str(last_date) + """%') ij ON ij.player_Id = p.id ORDER BY rank ASC
    """)
    players_list = namedtuplefetchall(cursor)
    
    paginator = Paginator(players_list, 25)
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return render(request, 'players.html', {'total_players': paginator.count, 'players': players})

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]    

def player(request, id):
    total = Match_Stats.objects.filter(player_id=id).count()

    player = Player.objects.get(id=id)

    cursor = connection.cursor()
    
    cursor.execute("""
        Select rank, date From front_ranking Where player_id = """ + id + """ ORDER BY date DESC limit 1;""")
    rank = cursor.fetchone()    

    cursor.execute("""
        Select rank, date From front_ranking Where player_id = """ + id + """ ORDER BY date DESC limit 1 OFFSET 1;""")
    previous_rank = cursor.fetchone()    
    
    return render(request, 'player.html', {'rank': rank[0], 'rank_date': rank[1], 'previous_rank': previous_rank[0], 'diff_rank': abs(rank[0] - previous_rank[0]), 'player': player, 'total_matches': total})

def refresh_matches(request):
    totals = IngestMatchesService.execute({})

    return HttpResponse("insertados " + str(totals.inserts) + " partidos y actualizados " + str(totals.updates) + " partidos")  

def refresh_players(request):
    totals = IngestPlayersService.execute({})

    return HttpResponse("se han insertado " + str(totals.inserts) + " jugadores y se han editado " + str(totals.updates) + " jugadores. Han fallado " + str(totals.fails) + " inserciones")

def refresh_rankings(request):
    totals = IngestRankingsService.execute({})

    return HttpResponse("terminado")    