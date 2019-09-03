from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import config_values as cv

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    # Ustedes escogen el numero de jugadores en config_values
    name_in_url = 'control'
    players_per_group = None
    num_rounds = 1
    instructions = 'control/Instructions.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        players = self.get_players()
        for p in players:
            # Esto generara valores entre 0 y 90, a pesar de que aparezca 10 dentro del range
            p.valoracion = random.SystemRandom().randrange(0, 10, 1)*10


class Group(BaseGroup):
    cleaning_price = models.IntegerField()

    def set_payoffs(self):
        ofertante = self.get_player_by_role('Ofertante')
        comprador = self.get_player_by_role('Comprador')

        ofertante.payoff = self.cleaning_price - ofertante.valoracion
        comprador.payoff = comprador.valoracion - self.cleaning_price


class Player(BasePlayer):
    oferta = models.IntegerField(initial=0, min=0)
    puja = models.IntegerField(initial=0, min=0)
    valoracion = models.IntegerField()

    def role(self):
        if self.id_in_group <= cv.num_participants/2:
            return 'Ofertante'
        else:
            return 'Comprador'
