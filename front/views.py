from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import numpy as np
import pandas as pd
import csv
from django.db import connection
import datetime
from pprint import pprint
from inspect import getmembers


def index(request):
    return render(request, 'index.html', {'hola': 'jaime'})

def players(request):
    cursor = connection.cursor()

    players = cursor.execute('SELECT * FROM tennis_players')
    return render(request, 'players.html', {'players': players})

def player(request, id):
    cursor = connection.cursor()

    matches = cursor.execute('SELECT * FROM tennis_matches')
    
    cont = 0
    for match in matches:
        cont += 1

    assert False, (cont,)        
    matches = [match for match in matches if match['winner_id'] == int(id) or str(match['loser_id']) == int(id)]
    #matches = list(filter(lambda match: match['winner_id'] == 'Jan Kodes', matches))
    #assert False, (matches,)
    return render(request, 'player.html', {'matches': matches})

def refresh_matches(request):
    cursor = connection.cursor()

    csv_file = open('./TenisMatchesModif.csv')
    csv_reader = csv.reader(csv_file, delimiter=',')

    result = ''
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(
                f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
            columns = getColumns()
            values = getValues(row)
            query = "INSERT INTO development.tennis_matches (" + ','.join(
                columns) + ") VALUES ("

            index = 0
            for value in values:
                if index != 0:
                    query += ','

                if isinstance(value, str):
                    value = value.replace("'", "`")
                    query += "'" + value + "'"

                if isinstance(value, int):
                    value = str(value)
                    query += value

                if isinstance(value, float):
                    value = str(value)
                    query += value

                if isinstance(value, datetime.datetime):
                    value = format(value)
                    query += "'" + value + "'"

                if isinstance(value, datetime.date):
                    value = format(value)
                    query += "'" + value + "'"

                index += 1

            query += ")"
            #break
            result = cursor.execute(query)

    return HttpResponse(query)


def refresh_players(request):
    cursor = connection.cursor()

    csv_file = pd.read_csv(
        'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_players.csv', header=None, names=['id', 'name', 'lastname', 'hand', 'birthdate', 'nationality'])

    result = ''
    line_count = 0
    for row in csv_file.itertuples():
        #assert False, (row.birthdate,)
        columns = ["tennis_player_id", "name", "lastname",
                   "birthdate", "nationality", "created_at", "updated_at"]
        values = [int(row.id), str(row.name), str(row.lastname), datetime.datetime.strptime(str(int(row.birthdate)), '%Y%m%d').date(), str(
            row.nationality), datetime.datetime.now(), datetime.datetime.now()]   
        query = "INSERT INTO development.tennis_players (" + ','.join(
            columns) + ") VALUES ("

        index = 0
        for value in values:
            if index != 0:
                query += ','

            if isinstance(value, str):
                value = value.replace("'", "\'")
                query += "'" + value + "'"

            if isinstance(value, int):
                value = str(value)
                query += value

            if isinstance(value, float):
                value = str(value)
                query += value

            if isinstance(value, datetime.datetime):
                value = format(value)
                query += "'" + value + "'"

            if isinstance(value, datetime.date):
                value = format(value)
                query += "'" + value + "'"

            index += 1

        query += ")"
        #break
        result = cursor.execute(query)

    return HttpResponse(query)


def getColumns():
    return ["tennis_match_id",
            "tourney_id",
            "tourney_name",
            "draw_size",
            "tourney_date",
            "match_num",
            "winner_id",
            "winner_seed",
            "winner_name",
            "winner_ht",
            "winner_ioc",
            "winner_age",
            "loser_id",
            "loser_seed",
            "loser_name",
            "loser_ht",
            "loser_ioc",
            "loser_age",
            "score",
            "best_of",
            "round",
            "minutes",
            "w_ace",
            "w_df",
            "w_svpt",
            "w_1st_in",
            "w_1st_won",
            "w_2nd_won",
            "w_sv_gms",
            "w_bp_saved",
            "w_bp_faced",
            "l_ace",
            "l_df",
            "l_svpt",
            "l_1st_in",
            "l_1st_won",
            "l_2nd_won",
            "l_sv_gms",
            "l_bp_saved",
            "l_bp_faced",
            "winner_rank",
            "winner_rank_points",
            "loser_rank",
            "loser_rank_points",
            "created_at",
            "updated_at"]


def getValues(row):
    try:
        tennis_match_id = int(row[0])
        tourney_id = str(row[1])
        tourney_name = str(row[2])
        draw_size = int(row[3])
        tourney_date = datetime.datetime.strptime(row[4], '%Y%m%d').date()
        match_num = int(row[5])
        winner_id = int(row[6])
        winner_seed = float(row[7]) if row[7] != '' else 0.0
        winner_name = str(row[8])
        winner_ht = float(row[9]) if row[9] else 0.0
        winner_ioc = str(row[10])
        winner_age = int(row[11])
        loser_id = int(row[12])
        loser_seed = float(row[13]) if row[13] else 0.0
        loser_name = str(row[14])
        loser_ht = float(row[15]) if row[15] else 0.0
        loser_ioc = str(row[16])
        loser_age = int(row[17])
        score = str(row[18])
        best_of = int(row[19])
        round = str(row[20])
        minutes = float(row[21]) if row[21] else 0.0
        w_ace = int(row[22]) if row[22] else 0
        w_df = int(row[23]) if row[23] else 0
        w_svpt = int(row[24]) if row[24] else 0
        w_1stIn = int(row[25]) if row[25] else 0
        w_1stWon = int(row[26]) if row[26] else 0
        w_2ndWon = int(row[27]) if row[27] else 0
        w_SvGms = int(row[28]) if row[28] else 0
        w_bpSaved = int(row[29]) if row[29] else 0
        w_bpFaced = int(row[30]) if row[30] else 0
        l_ace = int(row[31]) if row[31] else 0
        l_df = int(row[32]) if row[32] else 0
        l_svpt = int(row[33]) if row[33] else 0
        l_1stIn = int(row[34]) if row[34] else 0
        l_1stWon = int(row[35]) if row[35] else 0
        l_2ndWon = int(row[36]) if row[36] else 0
        l_SvGms = int(row[37]) if row[37] else 0
        l_bpSaved = int(row[38]) if row[38] else 0
        l_bpFaced = int(row[39]) if row[39] else 0
        winner_rank = int(row[40]) if row[40] != '' else 0
        winner_rank_points = int(row[41]) if row[41] != '' else 0
        loser_rank = int(row[42]) if row[42] else 0
        loser_rank_points = int(row[43]) if row[43] != '' else 0
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        return (tennis_match_id,
                tourney_id,
                tourney_name,
                draw_size,
                tourney_date,
                match_num,
                winner_id,
                winner_seed,
                winner_name,
                winner_ht,
                winner_ioc,
                winner_age,
                loser_id,
                loser_seed,
                loser_name,
                loser_ht,
                loser_ioc,
                loser_age,
                score,
                best_of,
                round,
                minutes,
                w_ace,
                w_df,
                w_svpt,
                w_1stIn,
                w_1stWon,
                w_2ndWon,
                w_SvGms,
                w_bpSaved,
                w_bpFaced,
                l_ace,
                l_df,
                l_svpt,
                l_1stIn,
                l_1stWon,
                l_2ndWon,
                l_SvGms,
                l_bpSaved,
                l_bpFaced,
                winner_rank,
                winner_rank_points,
                loser_rank,
                loser_rank_points,
                created_at,
                updated_at)

    except:
        raise Exception("El texto es: " +
                        str(row[7] + ' - ' + type(row[7])) + ' - ' + str(len(row[7])))
