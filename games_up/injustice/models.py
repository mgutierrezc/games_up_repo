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
    num_rounds = 3

    # Escojan aquí la dotac del comprador y los pagos recibidos por poseer el bien x
    dotacion_inicial_A = 100
    dotacion_inicial_B = 10
    pagos_x_A = 40
    pagos_x_B = 20

    #dotacion_inicial = 100
    #pagos_x = 20

    # Instrucciones
    instructions = 'injustice/Instructions.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)
        for p in self.get_players():
            p.dotacion_A -= self.session.config['treatment']*20
            p.dotacion_B += self.session.config['treatment'] * 20

class Group(BaseGroup):
    # Precio
    precio = models.FloatField(max=Constants.dotacion_inicial_A, min=0)

    # Variable de Aceptación (True) o Rechazo (False) del precio  --- caso tratado
    precio_aceptado = models.BooleanField(widget=widgets.RadioSelect, choices=[
        [True, 'Aceptar'], [False, 'Rechazar']])


    def compra_x(self):
        players = self.get_players()
        for p in players:
            if p.bien_x is False:
                p.bien_x = True
            else:
                p.bien_x = False



    def set_payoffs(self):
        #players = self.get_players()

        if p.role() == 'A':
            if self.precio_aceptado is True:
                p.payoff = p.dotacion_A - self.precio + c(Constants.pagos_x_A) + p.extraccion
            else:
                p.payoff = p.dotacion_A + p.extraccion
        else:
            if self.precio_aceptado is True:
                p.payoff = p.dotacion_B + self.precio - p.extraccion
            else:
                p.payoff = p.dotacion_B + c(Constants.pagos_x_B) - p.extraccion


#######################################################
class Player(BasePlayer):
    # Variable para saber si alguien tiene o no el bien x (True lo tiene, False no)
    bien_x = models.BooleanField()
    dotacion_A = models.CurrencyField(initial=Constants.dotacion_inicial_A)
    dotacion_B = models.CurrencyField(initial=Constants.dotacion_inicial_B)

    extraccion = models.CurrencyField(max=Constants.dotacion_inicial_A, min =0, initial=0)
    # Pago ronda anterior
    pago_anterior = models.CurrencyField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'

    # extraccion solo sería para los jugadores tipo A
    def extraccion_max(self):
        return self.dotacion
