import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class TennisMatches(DjangoCassandraModel):
    tennis_match_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    tourney_id = columns.Text(min_length=0, max_length=10)
    tourney_name = columns.Text(min_length=0, max_length=50)
    draw_size = columns.Integer
    tourney_date = columns.Date
    match_num = columns.Integer
    winner_id = columns.Integer
    winner_seed = columns.Float
    winner_name = columns.Text(max_length=100)
    winner_ht = columns.Float
    winner_ioc = columns.Text
    winner_age = columns.Integer
    loser_id = columns.Integer
    loser_seed = columns.Float
    loser_name = columns.Text(max_length=100)
    loser_ht = columns.Float
    loser_ioc = columns.Text
    loser_age = columns.Integer
    score = columns.Text(max_length=100)
    best_of = columns.Integer
    round = columns.Text(max_length=10)
    minutes = columns.Float
    w_ace = columns.Integer
    w_df = columns.Integer
    w_svpt = columns.Integer
    w_1stIn = columns.Integer
    w_1stWon = columns.Integer
    w_2ndWon = columns.Integer
    w_SvGms = columns.Integer
    w_bpSaved = columns.Integer
    w_bpFaced = columns.Integer
    l_ace = columns.Integer
    l_df = columns.Integer
    l_svpt = columns.Integer
    l_1stIn = columns.Integer
    l_1stWon = columns.Integer
    l_2ndWon = columns.Integer
    l_SvGms = columns.Integer
    l_bpSaved = columns.Integer
    l_bpFaced = columns.Integer
    winner_rank = columns.Integer
    winner_rank_points = columns.Integer
    loser_rank = columns.Integer
    loser_rank_points = columns.Integer
    Carpet = columns.Boolean
    Clay = columns.Boolean
    Grass = columns.Boolean
    Hard = columns.Boolean
    A = columns.Boolean
    C = columns.Boolean
    D = columns.Boolean
    F = columns.Boolean
    G = columns.Boolean
    M = columns.Boolean
    W_ALT = columns.Boolean
    W_Alt = columns.Boolean
    W_LL = columns.Boolean
    W_PR = columns.Boolean
    W_Q = columns.Boolean
    W_SE = columns.Boolean
    W_WC = columns.Boolean
    L_ALT = columns.Boolean
    L_Alt = columns.Boolean
    L_LL = columns.Boolean
    L_PR = columns.Boolean
    L_Q = columns.Boolean
    L_S = columns.Boolean
    L_SE = columns.Boolean
    L_WC = columns.Boolean
    W_L = columns.Boolean
    W_R = columns.Boolean
    W_U = columns.Boolean
    L_L = columns.Boolean
    L_R = columns.Boolean
    L_U = columns.Boolean
    BR = columns.Boolean
    ER = columns.Boolean
    F = columns.Boolean
    QF = columns.Boolean
    R128 = columns.Boolean
    R16 = columns.Boolean
    R32 = columns.Boolean
    R64 = columns.Boolean
    RR = columns.Boolean
    SF = columns.Boolean
    created_at = columns.DateTime
    updated_at = columns.DateTime