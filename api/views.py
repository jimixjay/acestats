from django.shortcuts import render
from django.db import connection
from collections import namedtuple
from django.http import JsonResponse

# Create your views here.

def player_win_ratings(request, id):
    cursor = connection.cursor()

    cursor.execute("""Select m.year as year, count(w.*) as wins, count(l.*) as losses 
                        FROM front_match m 
                        LEFT JOIN (SELECT ms1.match_id FROM front_match_stats ms1 WHERE player_id = """ + id + """ AND ms1.is_winner = true) AS w
            	        ON m.id = w.match_id
                        LEFT JOIN (SELECT ms2.match_id FROM front_match_stats ms2 WHERE player_id = """ + id + """ AND ms2.is_winner = false) AS l
                        ON m.id = l.match_id
                        GROUP BY m.year
                        ORDER BY m.year ASC""")
    victory_info = namedtuplefetchall(cursor)
    
    #assert False, (victory_info,)
    win_ratings = {}
    for info in victory_info:
        if info.year == 0 or (info.wins == 0 and info.losses == 0):
            continue

        if info.wins == 0:
            win_ratings[info.year] = {'rating': 0, 'wins': 0, 'losses': info.losses}
            continue

        if info.losses == 0:
            win_ratings[info.year] = {'rating': 100, 'wins': info.wins, 'losses': 0}
            continue

        win_ratings[info.year] = {'rating': '{:.2f}'.format((info.wins / (info.wins + info.losses)) * 100), 'wins': info.wins, 'losses': info.losses}

    return JsonResponse(win_ratings)

def player_aces_per_game_per_surface(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        Select m.year as year, s.name as surface, sum(ms.aces) as aces, count(ms.*) as games
                        FROM front_match m 
                        INNER JOIN front_tourney t ON m.tourney_id = t.id
                        INNER JOIN front_surface s ON t.surface_id = s.id
                        INNER JOIN front_match_stats ms ON m.id = ms.match_id AND player_id = """ + id + """
                        GROUP BY m.year, s.name
                        ORDER BY m.year ASC
    """)

    rows = namedtuplefetchall(cursor)    

    data = {}
    for row in rows:
        if not str(int(row.year)) in data:
            data[str(int(row.year))] = {}

        data[str(int(row.year))][row.surface] = {
            'aces': row.aces,
            'games': row.games
        }

    return JsonResponse(data)

def player_years_and_tourneys(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT EXTRACT(YEAR FROM t.date) as year, t.id as tourney_id, t.name, s.name as surface FROM front_tourney t 
        INNER JOIN front_match m ON m.tourney_id = t.id
        INNER JOIN front_surface s ON t.surface_id = s.id
        INNER JOIN front_match_stats ms ON m.id = ms.match_id AND player_id = """ + id)

    rows = namedtuplefetchall(cursor)

    data = {}
    for row in rows:
        if not str(int(row.year)) in data:
            data[str(int(row.year))] = []

        data[str(int(row.year))].append({'name': row.name, 'tourney_id': row.tourney_id, 'surface': row.surface})

    return JsonResponse(data)    

def player_matchs_by_tourney(request, id):
    cursor = connection.cursor()

    tourney_id = request.POST.get("tourney_id", "")    

    cursor.execute("""
        SELECT t.name as tourney_name, m.result, m.minutes, m.round""")

def player_rankings(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT EXTRACT(YEAR FROM date) as year, EXTRACT(MONTH FROM date) as month, rank FROM front_ranking WHERE player_id = """ + id + """ ORDER BY date ASC""")    

    rows = namedtuplefetchall(cursor)

    rankings = {}
    for row in rows:
        rankings[str(int(row.year)) + '-' + str(int(row.month))] = row.rank

    return JsonResponse(rankings)    

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]    