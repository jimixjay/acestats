from service_objects import services

import numpy as np
import pandas as pd
from django.db import connection
import datetime
from front.models import Player

class IngestPlayersService(services.Service):

    def process(self):
        cursor = connection.cursor()

        csv_file = pd.read_csv(
            'https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_players.csv', header=None, names=['id', 'name', 'lastname', 'hand', 'birthdate', 'nationality'])

        total_inserts = 0
        total_updates = 0
        total_fails = 0
        for row in csv_file.itertuples():
            try:
                if (np.isnan(row.birthdate)):
                    birthdate = None
                else:
                    birthdate = datetime.datetime.strptime(str(int(row.birthdate)), '%Y%m%d').date()
                
                player = Player.objects.filter(id=row.id)

                if (not player):
                    player = Player()
                    player.id = row.id
                    player.name = row.name
                    player.surname = row.lastname
                    player.birthday = birthdate
                    player.hand = row.hand
                    player.nationality = None
                    player.created_at = datetime.datetime.now()
                    player.updated_at = datetime.datetime.now()
                    player.save()    
                    total_inserts += 1
                else:
                    total_updates += 1
            except:        
                total_fails += 1

        return {'inserts': total_inserts, 'updates': total_updates, 'fails': total_fails}        