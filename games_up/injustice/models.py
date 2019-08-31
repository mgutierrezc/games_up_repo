from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'injustice'
    players_per_group = 2
    num_rounds = 5

    # Escojan aquí la dotac del comprador y los pagos recibidos por poseer el bien x
    dotacion_inicial = 10
    pagos_x = 2

    # Instrucciones
    instructions = 'injustice/Instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # Precio
    precio = models.FloatField(min=0)
    # Variable de Aceptación (True) o Rechazo (False) del precio
    precio_aceptado = models.BooleanField(widget=widgets.RadioSelect, choices=[
        [True, 'Aceptar'], [False, 'Rechazar']])
    
    def set_payoffs(self):
        players = self.get_players()
        for p in players:
            if self.round_number > 1:
                p.pago_anterior = p.in_round(self.round_number - 1).payoff

            if p.role() == 'A':
                if self.precio_aceptado is True:
                    if p.bien_x is True:
                        p.payoff = p.dotacion - self.precio + Constants.pagos_x + p.pago_anterior + p.extraccion
                    else:
                        p.payoff = p.dotacion + self.precio + p.pago_anterior + p.extraccion
                else:
                    if p.bien_x is True:
                        p.payoff = p.dotacion + Constants.pagos_x + p.pago_anterior + p.extraccion
                    else:
                        p.payoff = p.dotacion + p.pago_anterior + p.extraccion

            else:
                if self.precio_aceptado is True:
                    if p.bien_x is True:
                        p.payoff = p.dotacion - self.precio + Constants.pagos_x + p.pago_anterior - p.extraccion
                    else:
                        p.payoff = p.dotacion + self.precio + p.pago_anterior - p.extraccion
                else:
                    if p.bien_x is True:
                        p.payoff = p.dotacion + Constants.pagos_x + p.pago_anterior - p.extraccion
                    else:
                        p.payoff = p.dotacion + p.pago_anterior - p.extraccion


class Player(BasePlayer):
    # Variable para saber si alguien tiene o no el bien x (True lo tiene, False no)
    bien_x = models.BooleanField()
    dotacion = models.FloatField()
    extraccion = models.FloatField(min=0, initial=0)
    # Pago ronda anterior
    pago_anterior = models.IntegerField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'

    def extraccion_max(self):
        return self.dotacion
