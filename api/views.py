from django.shortcuts import render
from django.db import connection
from collections import namedtuple
from django.http import JsonResponse
import numpy as np
import pandas as pd
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def search(request):
    value = request.POST.get('value', '')
    cursor = connection.cursor()

    values = value.split()

    key = 0
    for value in values:
        #values[key] = "'" + value + "'"
        key += 1

    query = """
                    SELECT p.id, CONCAT(p.name, ' ', p.surname)
                    FROM front_player p
                    WHERE p.name ~* '""" + '|'.join(values) + """'
                    OR p.surname ~* '""" + '|'.join(values) + """'
                    ORDER BY p.surname ASC
                    LIMIT 10
                """



    cursor.execute(query)

    data = namedtuplefetchall(cursor)

    return JsonResponse(data, safe=False)

def player_honors(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT t.match_id, t.date, t.tourney, t.surface, t.result, t.rival, t.minutes, t.tourney_level
        FROM front_player p
        INNER JOIN (SELECT p.id, m.id as match_id, t.name as tourney, t.date, sur.name as surface, m.result, CONCAT(LEFT(p2.name, 1), '. ', p2.surname) as rival, m.minutes,
            CASE tl.code
                            WHEN 'A' THEN 'default'
                            WHEN 'M' THEN 'info'
                            WHEN 'G' THEN 'success'
                            WHEN 'F' THEN 'default'
                            WHEN 'D' THEN 'default'
                            ELSE '' END
                        as tourney_level
            FROM front_match m
            INNER JOIN front_tourney t ON m.tourney_id = t.id
            INNER JOIN front_surface sur ON t.surface_id = sur.id
            INNER JOIN front_match_stats s ON m.id = s.match_id AND s.is_winner = true
            INNER JOIN front_player p ON s.player_id = p.id
            INNER JOIN front_match_stats s2 ON m.id = s2.match_id AND s2.is_winner = false
            INNER JOIN front_player p2 ON s2.player_id = p2.id
            INNER JOIN front_tourney_level tl ON t.tourney_level_id = tl.id
            WHERE p.id = """ + str(id) + """
            AND m.round = 'F'
            ORDER BY t.date DESC, m.match_num DESC) t ON p.id = t.id
    """)

    trophies = namedtuplefetchall(cursor)

    data = {}
    trophies_dict = {}
    data['finals'] = {}
    for row in trophies:
        if not str(row.tourney) in trophies_dict:
            trophies_dict[str(row.tourney)] = {'count': 0, 'label_color': row.tourney_level}

        trophies_dict[str(row.tourney)]['count'] += 1
        minutes = ''
        if row.minutes:
            hours = int(row.minutes / 60)
            minutes = (row.minutes) % 60

            minutes = ("%d:%02d" % (hours, minutes))
        else:
            minutes = '-'
        data['finals'][str(row.match_id)] = {'date': row.date, 'tourney': row.tourney, 'surface': row.surface, 'result': row.result, 'rival': row.rival, 'minutes': minutes}

    trophies = []
    for tourney in trophies_dict:
        trophies.append({'name': tourney, 'count': trophies_dict[tourney]['count'], 'label_color': trophies_dict[tourney]['label_color']})

    data['trophies'] = sorted(trophies, reverse=True, key=getKeyForSort)

    return JsonResponse(data)

def getKeyForSort(item):
    return item['count']

def player_stats(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT m.id as match_id, m.best_of, m.minutes, m.round, m.year, s.aces, s.double_faults, s.service_points, s.first_services, s.first_services_won, s.second_services_won, s.service_game_won,
            s.break_points_saved, s.break_points_played, s.is_winner, sur.name as surface, t.name as tourney, t.date as tourney_date,
            CASE tl.code
                WHEN 'A' THEN 'Other'
                WHEN 'M' THEN 'Masters 1000'
                WHEN 'G' THEN 'Grand Slam'
                WHEN 'F' THEN 'Other'
                WHEN 'D' THEN 'Other'
                ELSE '' END
            as tourney_level
        FROM front_match m
        INNER JOIN front_tourney t ON m.tourney_id = t.id
        INNER JOIN front_surface sur ON t.surface_id = sur.id
        INNER JOIN front_match_stats s ON m.id = s.match_id
        INNER JOIN front_player p ON s.player_id = p.id
        INNER JOIN front_tourney_level tl ON t.tourney_level_id = tl.id
        WHERE p.id = """ + str(id) + """
    """)

    completeInfo = namedtuplefetchall(cursor)

    completeInfo = pd.DataFrame(data = completeInfo)

    data = {}
    hard = completeInfo[completeInfo["surface"] == 'Hard']
    clay = completeInfo[completeInfo["surface"] == 'Clay']
    grass = completeInfo[completeInfo["surface"] == 'Grass']
    carpet = completeInfo[completeInfo["surface"] == 'Carpet']

    grand_slam = completeInfo[completeInfo["tourney_level"] == 'Grand Slam']
    master = completeInfo[completeInfo["tourney_level"] == 'Masters 1000']
    other = completeInfo[completeInfo["tourney_level"] == 'Other']

    best_of_5 = completeInfo[completeInfo["best_of"] == 5]
    best_of_3 = completeInfo[completeInfo["best_of"] == 3]

    finals = completeInfo[completeInfo["round"] == 'F']
    semifinals = completeInfo[completeInfo["round"] == 'SF']
    quarterfinal = completeInfo[completeInfo["round"] == 'QF']

    data['Hard'] = getStatsBySubDataFrame(hard)
    data['Clay'] = getStatsBySubDataFrame(clay)
    data['Grass'] = getStatsBySubDataFrame(grass)
    data['Carpet'] = getStatsBySubDataFrame(carpet)
    data['Grand Slams'] = getStatsBySubDataFrame(grand_slam)
    data['Masters'] = getStatsBySubDataFrame(master)
    data['Other'] = getStatsBySubDataFrame(other)
    data['Best of 5'] = getStatsBySubDataFrame(best_of_5)
    data['Best of 3'] = getStatsBySubDataFrame(best_of_3)
    data['Finals'] = getStatsBySubDataFrame(finals)
    data['Semifinals'] = getStatsBySubDataFrame(semifinals)
    data['Quarterfinals'] = getStatsBySubDataFrame(quarterfinal)

    return JsonResponse(data)

def getStatsBySubDataFrame(data):
    matches = data.shape[0]
    wins = data[data["is_winner"] == True].shape[0]
    losses = data[data["is_winner"] == False].shape[0]
    aces_per_game = data['aces'].mean()
    double_faults_per_game = data['double_faults'].mean()
    service_points_per_game = data['service_points'].mean()
    first_services_per_game = data['first_services'].mean()
    first_services_won_per_game = data['first_services_won'].mean()
    second_services_won_per_game = data['second_services_won'].mean()
    break_points_played_per_game = data['break_points_played'].mean()
    break_points_saved_per_game = data['break_points_saved'].mean()

    win_perc = 0
    aces_rate = 0
    double_faults_rate = 0
    first_services_rate = 0
    first_services_won_rate = 0
    second_services_won_rate = 0
    break_points_saved_ratio = 0

    if matches > 0:
        win_perc = wins * 100 / matches

    if service_points_per_game > 0:
        aces_rate = aces_per_game / service_points_per_game * 100
        double_faults_rate = double_faults_per_game / service_points_per_game * 100
        first_services_rate = first_services_per_game / service_points_per_game * 100

    if first_services_per_game > 0:
        first_services_won_rate = first_services_won_per_game / first_services_per_game * 100
        second_services_won_rate = second_services_won_per_game / (service_points_per_game - first_services_per_game) * 100

    if break_points_played_per_game > 0:
        break_points_saved_ratio = break_points_saved_per_game / break_points_played_per_game * 100

    return {
        'matches': matches,
        'wins': wins,
        'losses': losses,
        'win_perc': "{:.2f}".format(win_perc),
        'aces_per_game': "{:.2f}".format(aces_per_game),
        'aces_rate': "{:.2f}".format(aces_rate),
        'double_faults_per_game': "{:.2f}".format(double_faults_per_game),
        'double_faults_rate': "{:.2f}".format(double_faults_rate),
        'first_services_rate': "{:.2f}".format(first_services_rate),
        'first_services_won_rate': "{:.2f}".format(first_services_won_rate),
        'second_services_won_rate': "{:.2f}".format(second_services_won_rate),
        'break_points_played_per_game': "{:.2f}".format(break_points_played_per_game),
        'break_points_saved_ratio': "{:.2f}".format(break_points_saved_ratio),

    }

@csrf_exempt
def player_game_by_game(request, id):
    cursor = connection.cursor()

    tourney = request.POST.get('tourney', '')

    cursor.execute("""
        SELECT m.id as match_id, m.best_of, m.minutes, m.round, m.result, m.year, s.aces, s.double_faults, s.service_points, s.first_services, s.first_services_won, s.second_services_won, s.service_game_won,
                    s.break_points_saved, s.break_points_played, s.is_winner, sur.name as surface, t.name as tourney, t.date as tourney_date, CONCAT(LEFT(p2.name, 1), '. ', p2.surname) as rival
                FROM front_match m
                INNER JOIN front_tourney t ON m.tourney_id = t.id
                INNER JOIN front_surface sur ON t.surface_id = sur.id
                INNER JOIN front_match_stats s ON m.id = s.match_id
                INNER JOIN front_player p ON s.player_id = p.id
                INNER JOIN front_tourney_level tl ON t.tourney_level_id = tl.id
                INNER JOIN front_match_stats s2 ON m.id = s2.match_id AND s2.id <> s.id
                INNER JOIN front_player p2 ON p2.id = s2.player_id
                WHERE p.id = """ + str(id) + """
                AND t.id = '""" + str(tourney) + """'
                ORDER BY match_num DESC
    """)

    matches = namedtuplefetchall(cursor)

    data = []
    for row in matches:
        data.append({
            'minutes': row.minutes,
            'round': row.round,
            'result': row.result,
            'year': row.year,
            'aces': row.aces,
            'double_faults': row.double_faults,
            'service_points': row.service_points,
            'first_services': row.first_services,
            'first_services_won': row.first_services_won,
            'second_services_won': row.second_services_won,
            'service_game_won': row.service_game_won,
            'break_points_saved': row.break_points_saved,
            'break_points_played': row.break_points_played,
            'is_winner': row.is_winner,
            'rival': row.rival
        })

    return JsonResponse(data, safe=False)

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
    rows = getRowsPerGamePerSurface('aces', id)

    return JsonResponse(constructData(rows, 'aces'))

def player_double_faults_per_game_per_surface(request, id):
    rows = getRowsPerGamePerSurface('double_faults', id)

    return JsonResponse(constructData(rows, 'doubleFaults'))

def player_service_points_per_game_per_surface(request, id):
    rows = getRowsPerGamePerSurface('service_points', id)

    return JsonResponse(constructData(rows, 'servicePoints'))

def getRowsPerGamePerSurface(field, id):
    cursor = connection.cursor()

    query = """
        Select m.year as year, s.name as surface, sum(ms.""" + field + """) as sum_field, count(ms.*) as games
        FROM front_match m
        INNER JOIN front_tourney t ON m.tourney_id = t.id
        INNER JOIN front_surface s ON t.surface_id = s.id
        INNER JOIN front_match_stats ms ON m.id = ms.match_id AND player_id = """ + id + """
        GROUP BY m.year, s.name
        ORDER BY m.year ASC
    """

    cursor.execute(query)

    return namedtuplefetchall(cursor)

def constructData(rows, field):
    data = {}
    for row in rows:
        if not str(int(row.year)) in data:
            data[str(int(row.year))] = {}

        data[str(int(row.year))][row.surface] = {
            field: row.sum_field,
            'games': row.games
        }

    return data

def player_years_and_tourneys(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT EXTRACT(YEAR FROM t.date) as year, t.id as tourney_id, t.name, s.name as surface FROM front_tourney t
        INNER JOIN front_match m ON m.tourney_id = t.id
        INNER JOIN front_surface s ON t.surface_id = s.id
        INNER JOIN front_match_stats ms ON m.id = ms.match_id AND player_id = """ + id + """
        ORDER BY t.name ASC""")

    rows = namedtuplefetchall(cursor)

    data = {}
    for row in rows:
        if not str(int(row.year)) in data:
            data[str(int(row.year))] = []

        data[str(int(row.year))].append({'name': row.name, 'tourney_id': row.tourney_id, 'surface': row.surface})

    return JsonResponse(data)

def player_rivals(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p2.id, CONCAT(p2.surname, ', ', LEFT(p2.name, 1), '.') as rival, count(ms.*) as games
        FROM front_match_stats ms
        INNER JOIN front_match_stats ms2 ON ms.match_id = ms2.match_id AND ms2.player_id <> ms.player_id
        INNER JOIN front_player p2 ON p2.id = ms2.player_id
        WHERE ms.player_id = """ + id + """
        GROUP BY p2.id
        ORDER BY rival ASC""")

    rows = namedtuplefetchall(cursor)

    data = []
    for row in rows:
        data.append({'id': row.id, 'rival': row.rival, 'games': row.games})

    return JsonResponse(data, safe=False)

def player_ranking_tab(request, id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT current_rank.rank AS current_rank, current_rank.points AS current_points,
        			best_rank.rank AS best_rank, CONCAT(best_rank.year, '-', best_rank.month) AS best_rank_date,
        			best_points.points AS best_points, CONCAT(best_points.year, '-', best_points.month) AS best_points_date,
        			most_repeated_rank.rank AS most_repeated_rank, most_repeated_rank.total AS most_repeated_rank_total,
        			most_repeated_rank_year.rank AS most_repeated_rank_year, most_repeated_rank_year.total AS most_repeated_rank_year_total,
        			rank_totals.rank1 AS rank_top_1, rank_totals.rank5 AS rank_top_5, rank_totals.rank10 AS rank_top_10, rank_totals.rank20 AS rank_top_20, rank_totals.rank50 AS rank_top_50, rank_totals.rank100 AS rank_top_100,
        			rank_totals_year.rank1 AS rank_top_year_1, rank_totals_year.rank5 AS rank_top_year_5, rank_totals_year.rank10 AS rank_top_year_10, rank_totals_year.rank20 AS rank_top_year_20, rank_totals_year.rank50 AS rank_top_year_50, rank_totals_year.rank100 AS rank_top_year_100
                FROM front_player p
        		  INNER JOIN (SELECT player_id, rank, points
        							FROM front_ranking
        							WHERE player_id = """ + id + """
        							ORDER BY DATE DESC LIMIT 1) current_rank ON current_rank.player_id = p.id
        		  INNER JOIN (SELECT player_id, rank, points, EXTRACT(YEAR FROM date) as year, EXTRACT(MONTH FROM date) as month
        							FROM front_ranking
        							WHERE player_id = """ + id + """
        							ORDER BY rank ASC, DATE ASC LIMIT 1) best_rank ON best_rank.player_id = p.id
        		  INNER JOIN (SELECT player_id, points, EXTRACT(YEAR FROM date) as year, EXTRACT(MONTH FROM date) as month
        							FROM front_ranking
        							WHERE player_id = """ + id + """
        							ORDER BY points DESC, DATE ASC LIMIT 1) best_points ON best_points.player_id = p.id
        		  INNER JOIN (SELECT player_id, rank, total FROM (
        							SELECT player_id, rank, COUNT(*) AS total
        							FROM front_ranking
        							WHERE player_id = """ + id + """
        							GROUP BY player_id, rank
        							ORDER BY total DESC, rank ASC) t
        							LIMIT 1) most_repeated_rank ON most_repeated_rank.player_id = p.id
        		  INNER JOIN (SELECT player_id, rank, total FROM (
        							SELECT player_id, rank, COUNT(*) AS total
        							FROM (SELECT player_id, max(EXTRACT('month' FROM r.date)) AS month, rank, EXTRACT('year' from r.date) as YEAR
        								FROM front_ranking r
        								INNER JOIN (SELECT DATE_PART('year', DATE) AS year, MAX(DATE) AS max_date FROM front_ranking WHERE player_id = """ + id + """ GROUP BY 1) r2 ON r.date = r2.max_date
        								WHERE player_id = """ + id + """
        								GROUP BY 1, 3, 4) t
        							WHERE player_id = """ + id + """
        							GROUP BY player_id, rank
        							ORDER BY total DESC, rank ASC) t
        							LIMIT 1) most_repeated_rank_year ON most_repeated_rank_year.player_id = p.id
        		  INNER JOIN (with ranks AS (
        							SELECT front_ranking.player_id,
        								CASE WHEN rank = 1 THEN 1
        								WHEN rank <= 5 THEN 5
        								WHEN rank <= 10 THEN 10
        								WHEN rank <= 20 THEN 20
        								WHEN rank <= 50 THEN 50
        								WHEN rank <= 100 THEN 100 END AS rank,
        								COUNT(*) AS total
        							FROM front_ranking
        							WHERE player_id = """ + id + """ AND rank<=100
        							GROUP BY player_id, CASE WHEN rank = 1 THEN 1
        								WHEN rank <= 5 THEN 5
        								WHEN rank <= 10 THEN 10
        								WHEN rank <= 20 THEN 20
        								WHEN rank <= 50 THEN 50
        								WHEN rank <= 100 THEN 100 END
        						)
        						SELECT player_id, SUM(rank1) AS rank1, SUM(rank5 + rank1) AS rank5, SUM(rank10 + rank5 + rank1) AS rank10, SUM(rank20 + rank10 + rank5 + rank1) AS rank20, SUM(rank50 + rank20 + rank10 + rank5 + rank1) AS rank50, SUM(rank100 + rank50 + rank20 + rank10 + rank5 + rank1) AS rank100
        						FROM(
        							SELECT rank1.player_id, rank1.total AS rank1, 0 AS rank5, 0 AS rank10, 0 AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=1) AS rank1
        							UNION
        							SELECT rank5.player_id, 0 AS rank1, rank5.total AS rank5, 0 AS rank10, 0 AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=5) AS rank5
        							UNION
        							SELECT rank10.player_id, 0 AS rank1, 0 AS rank5, rank10.total AS rank10, 0 AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=10) AS rank10
        							UNION
        							SELECT rank20.player_id, 0 AS rank1, 0 AS rank5, 0 AS rank10, rank20.total AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=20) AS rank20
        							UNION
        							SELECT rank50.player_id, 0 AS rank1, 0 AS rank5, 0 AS rank10, 0 AS rank20, rank50.total AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=50) AS rank50
        							UNION
        							SELECT rank100.player_id, 0 AS rank1, 0 AS rank5, 0 AS rank10, 0 AS rank20, 0 AS rank50, rank100.total AS rank100
        							FROM (SELECT * from ranks WHERE rank=100) AS rank100
        						) AS t
        						GROUP BY player_id) rank_totals ON rank_totals.player_id = p.id
        		  INNER JOIN (with ranks AS (
        							SELECT t.player_id,
        								CASE WHEN rank = 1 THEN 1
        								WHEN rank <= 5 THEN 5
        								WHEN rank <= 10 THEN 10
        								WHEN rank <= 20 THEN 20
        								WHEN rank <= 50 THEN 50
        								WHEN rank <= 100 THEN 100 END AS rank,
        								COUNT(*) AS total
        							FROM (SELECT player_id, max(EXTRACT('month' FROM r.date)) AS month, rank, EXTRACT('year' from r.date) as YEAR
        														FROM front_ranking r
        														INNER JOIN (SELECT DATE_PART('year', DATE) AS year, MAX(DATE) AS max_date FROM front_ranking WHERE player_id = """ + id + """ GROUP BY 1) r2 ON r.date = r2.max_date
        														WHERE player_id = """ + id + """
        														GROUP BY 1, 3, 4) t
        							WHERE player_id = """ + id + """ AND rank<=100
        							GROUP BY player_id, CASE WHEN rank = 1 THEN 1
        								WHEN rank <= 5 THEN 5
        								WHEN rank <= 10 THEN 10
        								WHEN rank <= 20 THEN 20
        								WHEN rank <= 50 THEN 50
        								WHEN rank <= 100 THEN 100 END
        						)
        						SELECT player_id, SUM(rank1) AS rank1, SUM(rank5 + rank1) AS rank5, SUM(rank10 + rank5 + rank1) AS rank10, SUM(rank20 + rank10 + rank5 + rank1) AS rank20, SUM(rank50 + rank20 + rank10 + rank5 + rank1) AS rank50, SUM(rank100 + rank50 + rank20 + rank10 + rank5 + rank1) AS rank100
        						FROM(
        							SELECT rank1.player_id, rank1.total AS rank1, 0 AS rank5, 0 AS rank10, 0 AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=1) AS rank1
        							UNION
        							SELECT rank5.player_id, 0 AS rank1, rank5.total AS rank5, 0 AS rank10, 0 AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=5) AS rank5
        							UNION
        							SELECT rank10.player_id, 0 AS rank1, 0 AS rank5, rank10.total AS rank10, 0 AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=10) AS rank10
        							UNION
        							SELECT rank20.player_id, 0 AS rank1, 0 AS rank5, 0 AS rank10, rank20.total AS rank20, 0 AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=20) AS rank20
        							UNION
        							SELECT rank50.player_id, 0 AS rank1, 0 AS rank5, 0 AS rank10, 0 AS rank20, rank50.total AS rank50, 0 AS rank100
        							FROM (SELECT * from ranks WHERE rank=50) AS rank50
        							UNION
        							SELECT rank100.player_id, 0 AS rank1, 0 AS rank5, 0 AS rank10, 0 AS rank20, 0 AS rank50, rank100.total AS rank100
        							FROM (SELECT * from ranks WHERE rank=100) AS rank100
        						) AS t
        						GROUP BY player_id) rank_totals_year ON rank_totals_year.player_id = p.id
        		  WHERE p.id = """ + id + """;""")

    rows = namedtuplefetchall(cursor)

    data = {}
    for row in rows:
        data['current_rank'] = row.current_rank
        data['current_points'] = row.current_points
        data['best_rank'] = row.best_rank
        data['best_rank_date'] = row.best_rank_date
        data['best_points'] = row.best_points
        data['best_points_date'] = row.best_points_date
        data['most_repeated_rank'] = row.most_repeated_rank
        data['most_repeated_rank_total'] = row.most_repeated_rank_total
        data['most_repeated_rank_year'] = row.most_repeated_rank_year
        data['most_repeated_rank_year_total'] = row.most_repeated_rank_year_total
        data['rank_top_1'] = row.rank_top_1
        data['rank_top_5'] = row.rank_top_5
        data['rank_top_10'] = row.rank_top_10
        data['rank_top_20'] = row.rank_top_20
        data['rank_top_50'] = row.rank_top_50
        data['rank_top_100'] = row.rank_top_100
        data['rank_top_year_1'] = row.rank_top_year_1
        data['rank_top_year_5'] = row.rank_top_year_5
        data['rank_top_year_10'] = row.rank_top_year_10
        data['rank_top_year_20'] = row.rank_top_year_20
        data['rank_top_year_50'] = row.rank_top_year_50
        data['rank_top_year_100'] = row.rank_top_year_100

    return JsonResponse(data, safe=False)


@csrf_exempt
def player_face_to_face(request, id):
    cursor = connection.cursor()

    rival = request.POST.get('rival', '')

    cursor.execute("""
        SELECT m.id as match_id, m.best_of, m.minutes, m.round, m.result, m.year, s.aces, s.double_faults, s.service_points, s.first_services, s.first_services_won, s.second_services_won, s.service_game_won,
                    s.break_points_saved, s.break_points_played, s.is_winner, s2.aces as rival_aces, s2.double_faults as rival_double_faults, s2.service_points as rival_service_points, s2.first_services as rival_first_services, s2.first_services_won as rival_first_services_won, s2.second_services_won as rival_second_services_won, s2.service_game_won as rival_service_game_won,
                    s2.break_points_saved as rival_break_points_saved, s2.break_points_played as rival_break_points_played, sur.name as surface, t.name as tourney, t.date as tourney_date,
                    CONCAT(LEFT(p.name, 1), '. ', p.surname) as player_name,
                    CONCAT(LEFT(p2.name, 1), '. ', p2.surname) as rival_name
                FROM front_match m
                INNER JOIN front_tourney t ON m.tourney_id = t.id
                INNER JOIN front_surface sur ON t.surface_id = sur.id
                INNER JOIN front_match_stats s ON m.id = s.match_id
                INNER JOIN front_player p ON s.player_id = p.id
                INNER JOIN front_tourney_level tl ON t.tourney_level_id = tl.id
                INNER JOIN front_match_stats s2 ON m.id = s2.match_id AND s2.id <> s.id
                INNER JOIN front_player p2 ON s2.player_id = p2.id
                WHERE p.id = """ + str(id) + """
                AND s2.player_id = '""" + str(rival) + """'
                ORDER BY t.date DESC, match_num DESC
    """)

    matchesRows = namedtuplefetchall(cursor)

    data = {}
    matches = []
    max_win_streak = 0
    max_loss_streak = 0
    current_win_streak = 0
    current_loss_streak = 0
    player_name = ''
    rival_name = ''
    for row in matchesRows:
        matches.append({
            'minutes': row.minutes,
            'round': row.round,
            'result': row.result,
            'year': row.year,
            'aces': row.aces,
            'double_faults': row.double_faults,
            'service_points': row.service_points,
            'first_services': row.first_services,
            'first_services_won': row.first_services_won,
            'second_services_won': row.second_services_won,
            'service_game_won': row.service_game_won,
            'break_points_saved': row.break_points_saved,
            'break_points_played': row.break_points_played,
            'rival_aces': row.rival_aces,
            'rival_double_faults': row.rival_double_faults,
            'rival_service_points': row.rival_service_points,
            'rival_first_services': row.rival_first_services,
            'rival_first_services_won': row.rival_first_services_won,
            'rival_second_services_won': row.rival_second_services_won,
            'rival_service_game_won': row.rival_service_game_won,
            'rival_break_points_saved': row.rival_break_points_saved,
            'rival_break_points_played': row.rival_break_points_played,
            'is_winner': row.is_winner,
            'tourney': row.tourney,
            'date': row.tourney_date
        })

        if player_name == '':
            player_name = row.player_name
            rival_name = row.rival_name

        if row.is_winner:
            if current_win_streak > 0:
                current_win_streak += 1
                if max_win_streak < current_win_streak:
                    max_win_streak = current_win_streak
            else:
                current_loss_streak = 0
                current_win_streak = 1
                if max_win_streak == 0:
                    max_win_streak = 1
        else:
            if current_loss_streak > 0:
                current_loss_streak += 1
                if max_loss_streak < current_loss_streak:
                    max_loss_streak = current_loss_streak
            else:
                current_win_streak = 0
                current_loss_streak = 1
                if max_loss_streak == 0:
                    max_loss_streak = 1

    data['matches'] = matches
    #assert False, (data['matches'],)
    matchesDF = pd.DataFrame(data = data['matches'])
    #assert False, (matchesDF, )
    aces_per_game = matchesDF['aces'].mean()
    wins = matchesDF[matchesDF['is_winner'] == True].shape[0]
    double_faults = matchesDF['double_faults'].mean()
    service_points = matchesDF['service_points'].mean()
    first_services = matchesDF['first_services'].mean()
    first_services_won = matchesDF['first_services_won'].mean()
    second_services_won = matchesDF['second_services_won'].mean()
    service_game_won = matchesDF['service_game_won'].mean()
    break_points_saved = matchesDF['break_points_saved'].mean()
    break_points_played = matchesDF['break_points_played'].mean()
    rival_aces_per_game = matchesDF['rival_aces'].mean()
    rival_wins = matchesDF[matchesDF['is_winner'] == False].shape[0]
    rival_double_faults = matchesDF['rival_double_faults'].mean()
    rival_service_points = matchesDF['rival_service_points'].mean()
    rival_first_services =  matchesDF['rival_first_services'].mean()
    rival_first_services_won = matchesDF['rival_first_services_won'].mean()
    rival_second_services_won = matchesDF['rival_second_services_won'].mean()
    rival_service_game_won = matchesDF['rival_service_game_won'].mean()
    rival_break_points_saved = matchesDF['rival_break_points_saved'].mean()
    rival_break_points_played = matchesDF['rival_break_points_played'].mean()

    data['stats'] = {
        'player_name': player_name,
        'rival_name': rival_name,
        'aces_per_game': aces_per_game,
        'wins': wins,
        'double_faults': double_faults,
        'service_points': service_points,
        'first_services': first_services,
        'first_services_won': first_services_won,
        'second_services_won': second_services_won,
        'service_game_won': service_game_won,
        'break_points_saved': break_points_saved,
        'break_points_played': break_points_played,
        'rival_aces_per_game': rival_aces_per_game,
        'rival_wins': rival_wins,
        'rival_double_faults': rival_double_faults,
        'rival_service_points': rival_service_points,
        'rival_first_services': rival_first_services,
        'rival_first_services_won': rival_first_services_won,
        'rival_second_services_won': rival_second_services_won,
        'rival_service_game_won': rival_service_game_won,
        'rival_break_points_saved': rival_break_points_saved,
        'rival_break_points_played': rival_break_points_played,
        'max_win_streak': max_win_streak,
        'max_loss_streak': max_loss_streak
    }
        
    return JsonResponse(data, safe=False)

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