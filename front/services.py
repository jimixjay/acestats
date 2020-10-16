from service_objects import services

class GetPlayersService(services.Service):
    db_transaction = False

    players = ()

    def process(self):


        return self.players