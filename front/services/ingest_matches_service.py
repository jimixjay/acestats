from service_objects import services

import numpy as np
import pandas as pd
from django.db import connection
import datetime
from front.models import Match, Match_Stats, Player, Tourney, Tourney_Level, Surface

class IngestMatchesService(services.Service):

    def process(self):
        cursor = connection.cursor()

        errors = ''
        total_matches_updated = 0
        total_matches_inserted = 0
        tourneys = {}
        surfaces = {}
        tourney_levels = {}
        players = {}
        for year in range(1990, 2021):
            csv_file = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_' + str(year) + '.csv', header=1, names=self.getColumns())    

            for row in csv_file.itertuples():
                    created_at = datetime.datetime.now()
                    updated_at = datetime.datetime.now()
                #try:
                    id = str(row.tourney_id) + '-' + str(row.match_num)
                    match = Match.objects.filter(id=id)

                    if (not match):
                        match = Match()
                        match.id = id
                        match.year = row.tourney_id.split('-')[0]
                        match.match_num = row.match_num
                        match.result = row.score
                        match.best_of = row.best_of
                        match.minutes = None if np.isnan(row.minutes) else row.minutes
                        match.round = row.round
                        
                        if not tourneys.get(str(row.tourney_id)):                    
                            tourney = Tourney.objects.filter(id=row.tourney_id)
                            if (not tourney):
                                tourney = Tourney()
                                tourney.id = row.tourney_id
                                tourney.name = row.tourney_name
                                tourney.date = datetime.datetime.strptime(str(int(row.tourney_date)), '%Y%m%d').date()
                                tourney.created_at = created_at
                                tourney.updated_at = updated_at

                                if not surfaces.get(str(row.surface)):                            
                                    surfaces[str(row.surface)] = self.getSurface(str(row.surface))
                                        
                                tourney.surface = surfaces[str(row.surface)]

                                if not tourney_levels.get(str(row.tourney_level)):                                                            
                                    tourney_levels[str(row.tourney_level)] = self.getTourneyLevel(str(row.tourney_level))

                                tourney.tourney_level = tourney_levels[str(row.tourney_level)]    

                                tourney.created_at = created_at
                                tourney.updated_at = updated_at
                                tourney.save()
                            else:
                                tourney = tourney[0] 


                            tourneys[str(row.tourney_id)] = tourney

                        match.tourney = tourneys[str(row.tourney_id)]    
                        match.created_at = created_at
                        match.updated_at = updated_at
                        match.save()
                        total_matches_inserted += 1
                    else:
                        match[0].year = row.tourney_id.split('-')[0]
                        match[0].save()
                        total_matches_updated += 1
                        match = match[0]

                    match_stats_id = str(row.tourney_id) + '-' + str(row.match_num) + '-' + str(row.winner_id)
                    match_stats = Match_Stats.objects.filter(id=match_stats_id)
                    if (not match_stats):
                        seed = row.winner_seed
                        if pd.isnull(row.winner_seed) or not str(row.winner_seed).isnumeric():
                            seed = None

                        match_stats = Match_Stats()
                        match_stats.id = match_stats_id
                        match_stats.type = ""
                        match_stats.seed = seed
                        match_stats.aces = None if np.isnan(row.w_ace) else row.w_ace
                        match_stats.double_faults = None if np.isnan(row.w_df) else row.w_df
                        match_stats.service_points = None if np.isnan(row.w_svpt) else row.w_svpt
                        match_stats.first_services = None if np.isnan(row.w_1stIn) else row.w_1stIn
                        match_stats.first_services_won = None if np.isnan(row.w_1stWon) else row.w_1stWon
                        match_stats.second_services_won = None if np.isnan(row.w_2ndWon) else row.w_2ndWon
                        match_stats.service_game_won = None if np.isnan(row.w_SvGms) else row.w_SvGms
                        match_stats.break_points_saved = None if np.isnan(row.w_bpSaved) else row.w_bpSaved
                        match_stats.break_points_played = None if np.isnan(row.w_bpFaced) else row.w_bpFaced
                        match_stats.rank = None if np.isnan(row.winner_rank) else row.winner_rank
                        match_stats.rank_points = None if np.isnan(row.winner_rank_points) else row.winner_rank_points
                        match_stats.is_winner = True
                        match_stats.created_at = created_at
                        match_stats.updated_at = updated_at
                        
                        players[row.winner_id] = self.getPlayer(str(row.winner_id))
                        match_stats.player = players[row.winner_id]

                        match_stats.match = match
                        match_stats.save()

                    match_stats_id = str(row.tourney_id) + '-' + str(row.match_num) + '-' + str(row.loser_id)
                    match_stats = Match_Stats.objects.filter(id=match_stats_id)
                    if (not match_stats):
                        seed = row.loser_seed
                        if pd.isnull(row.loser_seed) or not str(row.loser_seed).isnumeric():
                            seed = None

                        match_stats = Match_Stats()
                        match_stats.id = match_stats_id
                        match_stats.type = ""
                        match_stats.seed = seed
                        match_stats.aces = None if np.isnan(row.l_ace) else row.l_ace
                        match_stats.double_faults = None if np.isnan(row.l_df) else row.l_df
                        match_stats.service_points = None if np.isnan(row.l_svpt) else row.l_svpt
                        match_stats.first_services = None if np.isnan(row.l_1stIn) else row.l_1stIn
                        match_stats.first_services_won = None if np.isnan(row.l_1stWon) else row.l_1stWon
                        match_stats.second_services_won = None if np.isnan(row.l_2ndWon) else row.l_2ndWon
                        match_stats.service_game_won = None if np.isnan(row.l_SvGms) else row.l_SvGms
                        match_stats.break_points_saved = None if np.isnan(row.l_bpSaved) else row.l_bpSaved
                        match_stats.break_points_played = None if np.isnan(row.l_bpFaced) else row.l_bpFaced
                        match_stats.rank = None if np.isnan(row.loser_rank) else row.loser_rank
                        match_stats.rank_points = None if np.isnan(row.loser_rank_points) else row.loser_rank_points
                        match_stats.is_winner = False
                        match_stats.created_at = created_at
                        match_stats.updated_at = updated_at
                        
                        players[row.loser_id] = self.getPlayer(str(row.loser_id))
                        match_stats.player = players[row.loser_id]

                        match_stats.match = match
                        match_stats.save()    

                #except:
                #   assert False, (row.tourney_date, )
                    #errors = errors + '|||' + str(row.tourney_id) + '-' + str(row.match_num)

        return {'inserts': total_matches_inserted, 'updates': total_matches_updated}    

    def getColumns(self):
        return ["tourney_id","tourney_name","surface","draw_size","tourney_level","tourney_date","match_num","winner_id","winner_seed","winner_entry","winner_name","winner_hand","winner_ht","winner_ioc","winner_age",
        "loser_id","loser_seed","loser_entry","loser_name","loser_hand","loser_ht","loser_ioc","loser_age","score","best_of","round","minutes","w_ace","w_df","w_svpt","w_1stIn","w_1stWon","w_2ndWon","w_SvGms","w_bpSaved",
        "w_bpFaced","l_ace","l_df","l_svpt","l_1stIn","l_1stWon","l_2ndWon","l_SvGms","l_bpSaved","l_bpFaced","winner_rank","winner_rank_points","loser_rank","loser_rank_points"]

    def getPlayer(self, id):
        player = Player.objects.filter(id=id)
        if (not player):
            return None
        else:
            player = player[0]   

        return player

    def getSurface(self, name):
        surface = Surface.objects.filter(name=name)
        if (not surface):
            surface = Surface()
            surface.name = name
            surface.created_at = datetime.datetime.now()
            surface.updated_at = datetime.datetime.now()
            surface.save()
        else:
            surface = surface[0]   

        return surface    

    def getTourneyLevel(self, code):
        tourney_level = Tourney_Level.objects.filter(code=code)

        if (not tourney_level):
            tourney_level = Tourney_Level()
            tourney_level.code = code
            tourney_level.name = code
            tourney_level.created_at = datetime.datetime.now()
            tourney_level.updated_at = datetime.datetime.now()    
            tourney_level.save()
        else:
            tourney_level = tourney_level[0]

        return tourney_level          