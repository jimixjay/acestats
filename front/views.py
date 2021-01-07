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
    return render(request, 'index.html')

def players(request):
    page = request.GET.get('page', 1)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT CONCAT(EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date), '-') as date FROM front_ranking ORDER BY date DESC LIMIT 1
    """)
    last_date = cursor.fetchone()[0]

    cursor.execute("""
        SELECT p.name, p.surname, p.birthday, p.hand, EXTRACT(year FROM age(current_date,birthday)) :: int as age, p.id, ij.rank, n.code as nationality, ij.points
        FROM front_player p
        INNER JOIN (SELECT player_id, rank, points FROM front_ranking WHERE id LIKE '""" + str(last_date) + """%') ij ON ij.player_Id = p.id
        INNER JOIN front_nationality n ON p.nationality_id = n.id
        ORDER BY rank ASC
    """)
    players_list = namedtuplefetchall(cursor)

    players_list_with_matches = []
    for player in players_list:
        '''query = """
            SELECT w.result as win_result, w.round as win_round, w.tourney_name as win_tourney, w.tourney_date as win_date, w.rival as win_rival,
                   l.result as defeat_result, l.round as defeat_round, l.tourney_name as defeat_tourney, l.tourney_date as defeat_date, l.rival as defeat_rival
            FROM front_player p
            INNER JOIN (SELECT m.result, m.round, t.name as tourney_name, t.date as tourney_date, p.id as player_id, CONCAT(LEFT(p2.name, 1), '. ', p2.surname) as rival
                FROM front_match m
                INNER JOIN front_tourney t ON m.tourney_id = t.id
                INNER JOIN front_match_stats s ON m.id = s.match_id AND s.is_winner = true
                INNER JOIN front_player p ON s.player_id = p.id
                INNER JOIN front_match_stats s2 ON m.id = s2.match_id AND s2.is_winner = false
                INNER JOIN front_player p2 ON s2.player_id = p2.id
                WHERE p.id = """ + str(player.id) + """
                ORDER BY t.date DESC, m.match_num DESC
                LIMIT 1) w ON p.id = w.player_id
            INNER JOIN (SELECT m.result, m.round, t.name as tourney_name, t.date as tourney_date, p.id as player_id, CONCAT(LEFT(p2.name, 1), '. ', p2.surname) as rival
                FROM front_match m
                INNER JOIN front_tourney t ON m.tourney_id = t.id
                INNER JOIN front_match_stats s ON m.id = s.match_id AND s.is_winner = false
                INNER JOIN front_player p ON s.player_id = p.id
                INNER JOIN front_match_stats s2 ON m.id = s2.match_id AND s2.is_winner = true
                INNER JOIN front_player p2 ON s2.player_id = p2.id
                WHERE p.id = """ + str(player.id) + """
                ORDER BY t.date DESC, m.match_num DESC
                LIMIT 1) l ON p.id = l.player_id
        """

        cursor.execute(query)
        last_matches = cursor.fetchone()'''

        #players_list_with_matches.append(player_complete)
    
    paginator = Paginator(players_list, 25)

    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)

    finally:
        #assert False, (players, )
        players_complete = []
        for player in players:
            query = """
                SELECT t.name, t.date
                FROM front_player p
                INNER JOIN (SELECT p.id, t.name, EXTRACT(YEAR FROM date) :: int as date
                    FROM front_match m
                    INNER JOIN front_tourney t ON m.tourney_id = t.id
                    INNER JOIN front_match_stats s ON m.id = s.match_id AND s.is_winner = true
                    INNER JOIN front_player p ON s.player_id = p.id
                    WHERE p.id = """ + str(player.id) + """
                    AND m.round = 'F'
                    ORDER BY t.date DESC, m.match_num DESC
                    LIMIT 1) t ON p.id = t.id
            """

            cursor.execute(query)
            last_trophy = cursor.fetchone()

            query = """
                SELECT w.is_winner, w.result as result, w.round as round, w.tourney_name as tourney, w.tourney_date as date, w.rival as rival
                FROM front_player p
                INNER JOIN (SELECT s.is_winner, m.result, m.round, t.name as tourney_name, t.date as tourney_date, p.id as player_id, CONCAT(LEFT(p2.name, 1), '. ', p2.surname) as rival
                    FROM front_match m
                    INNER JOIN front_tourney t ON m.tourney_id = t.id
                    INNER JOIN front_match_stats s ON m.id = s.match_id
                    INNER JOIN front_player p ON s.player_id = p.id
                    INNER JOIN front_match_stats s2 ON m.id = s2.match_id AND s2.id <> s.id
                    INNER JOIN front_player p2 ON s2.player_id = p2.id
                    WHERE p.id = """ + str(player.id) + """
                    ORDER BY t.date DESC, m.match_num DESC
                    LIMIT 10) w ON p.id = w.player_id
            """

            cursor.execute(query)
            last_10 = namedtuplefetchall(cursor)

            index_game = 0

            player_complete = {}
            player_complete['name'] = player.name
            player_complete['surname'] = player.surname
            player_complete['birthday'] = player.birthday
            player_complete['hand'] = player.hand
            player_complete['age'] = player.age
            player_complete['id'] = player.id
            player_complete['rank'] = player.rank
            player_complete['nationality'] = player.nationality
            player_complete['points'] = player.points
            player_complete['last_games'] = []
            player_complete['last_trophy'] = {}
            for game in last_10:
                player_complete['last_games'].append(game)
                index_game += 1

            if last_trophy:
                player_complete['last_trophy'] = last_trophy[0] + ' (' + str(last_trophy[1]) + ')'
            else:
                player_complete['last_trophy'] = '-'

            players_complete.append(player_complete)

        players.object_list = players_complete
        return render(request, 'players.html', {'total_players': paginator.count, 'players': players})

def advance_stats(request):
    return render(request, 'advance_stats.html')

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

    query = """
        SELECT w.match_id, w.tourney, w.round, w.result, w.rival, w.is_winner
        FROM front_player p
        INNER JOIN (SELECT p.id, m.id as match_id, m.round, t.name as tourney, m.result, CONCAT(LEFT(p2.name, 1), '. ', p2.surname) as rival, s.is_winner
            FROM front_match m
            INNER JOIN front_tourney t ON m.tourney_id = t.id
            INNER JOIN front_match_stats s ON m.id = s.match_id
            INNER JOIN front_player p ON s.player_id = p.id
            INNER JOIN front_match_stats s2 ON m.id = s2.match_id AND s2.id <> s.id
            INNER JOIN front_player p2 ON s2.player_id = p2.id
            WHERE p.id = """ + str(player.id) + """
            ORDER BY t.date DESC, m.match_num DESC
            LIMIT 5) w ON p.id = w.id
    """
    cursor.execute(query)
    games = namedtuplefetchall(cursor)

    last5 = []
    for game in games:
        last5.append({'tourney': game.tourney, 'round': game.round, 'result': game.result, 'rival': game.rival, 'is_winner': game.is_winner})

    return render(request, 'player.html', {
        'rank': rank[0] if rank else 'NA',
        'rank_date': rank[1] if rank else 'NA',
        'previous_rank': previous_rank[0] if previous_rank else 'NA',
        'diff_rank': abs(rank[0] - previous_rank[0]) if rank and previous_rank else 'NA',
        'player': player,
        'total_matches': total,
        'last5': last5
    })

def refresh_matches(request):
    totals = IngestMatchesService.execute({})

    return HttpResponse("insertados " + str(totals['inserts']) + " partidos y actualizados " + str(totals['updates']) + " partidos")

def refresh_players(request):
    totals = IngestPlayersService.execute({})

    return HttpResponse("se han insertado " + str(totals['inserts']) + " jugadores y se han editado " + str(totals['updates']) + " jugadores. Han fallado " + str(totals['fails']) + " inserciones")

def refresh_rankings(request):
    totals = IngestRankingsService.execute({})

    return HttpResponse("terminado")    