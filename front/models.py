import uuid
from django.db import models

class Match(models.Model):
    match_num = models.IntegerField()
    result = models.TextField()
    best_of = models.IntegerField()
    minutes = models.IntegerField()
    round = models.TextField()
    tourney = models.ForeignKey("Tourney", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Tourney(models.Model):
    name = models.TextField()    
    date = models.DateField(auto_now=False, auto_now_add=False)
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
    type = models.TextField()    
    seed = models.IntegerField()
    aces = models.IntegerField()
    double_faults = models.IntegerField()
    service_points = models.IntegerField()
    first_services = models.IntegerField()
    first_services_won = models.IntegerField()
    second_services_won = models.IntegerField()
    service_game_won = models.IntegerField()
    break_points_saved = models.IntegerField()
    break_points_played = models.IntegerField()
    rank = models.IntegerField()
    rank_points = models.IntegerField()
    is_winner = models.BooleanField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    player_entry = models.ForeignKey("Player_Entry", on_delete=models.CASCADE)
    match = models.ForeignKey("Match", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)


class Player(models.Model):
    name = models.TextField()
    surname = models.TextField()
    hand = models.TextField()
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    nationality = models.ForeignKey("Nationality", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)

class Nationality(models.Model):
    code = models.TextField()    
    name = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)