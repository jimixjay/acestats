from service_objects import services

import numpy as np
import pandas as pd
from django.db import connection
import datetime
from front.models import Player, Ranking

class IngestRankingsService(services.Service):

    def process(self):
        cursor = connection.cursor()

        for decade in ['90s', '00s', '10s', 'current']:
            csv_file = pd.read_csv(
                'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_rankings_' + decade + '.csv', header=1, names=['date', 'rank', 'player_id', 'points'])
            
            for row in csv_file[csv_file['rank'] < 500].itertuples():
                date = datetime.datetime.strptime(str(int(row.date)), '%Y%m%d').date()
                current_month = str(date.year) + str(date.month)
        
                id = str(current_month) + '-' + str(row.player_id)    
                ranking = Ranking.objects.filter(id=id)
                        
                if (not ranking):                    
                    player = Player.objects.filter(id=row.player_id)                        

                    if player:
                        ranking = Ranking()
                        ranking.id = id
                        ranking.date = date
                        ranking.player = player[0]
                        ranking.rank = row.rank
                        ranking.points = None if np.isnan(row.points) else row.points
                        ranking.save()          
                
        return True