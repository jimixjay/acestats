import uuid
from django.db import models

class Match(models.Model):
    id = models.TextField(primary_key=True)
    year = models.IntegerField()
    match_num = models.IntegerField()
    result = models.TextField()
    best_of = models.IntegerField(null=True)
    minutes = models.IntegerField(null=True)
    round = models.TextField()
    tourney = models.ForeignKey("Tourney", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Ranking(models.Model):
    id = models.TextField(primary_key=True)    
    date = models.DateField(auto_now=False, auto_now_add=False)
    points = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)

class Tourney(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()    
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    surface = models.ForeignKey("Surface", on_delete=models.SET_NULL, null=True)
    tourney_level = models.ForeignKey("Tourney_Level", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Surface(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Tourney_Level(models.Model):
    code = models.TextField()        
    name = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Player_Entry(models.Model):
    code = models.TextField()
    name = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Match_Stats(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField()    
    seed = models.IntegerField(null=True)
    aces = models.IntegerField(null=True)
    double_faults = models.IntegerField(null=True)
    service_points = models.IntegerField(null=True)
    first_services = models.IntegerField(null=True)
    first_services_won = models.IntegerField(null=True)
    second_services_won = models.IntegerField(null=True)
    service_game_won = models.IntegerField(null=True)
    break_points_saved = models.IntegerField(null=True)
    break_points_played = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    rank_points = models.IntegerField(null=True)
    is_winner = models.BooleanField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE, null=True)
    player_entry = models.ForeignKey("Player_Entry", on_delete=models.CASCADE, null=True)
    match = models.ForeignKey("Match", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    surname = models.TextField()
    hand = models.TextField()
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True)
    nationality = models.ForeignKey("Nationality", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Nationality(models.Model):
    code = models.TextField()    
    name = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)