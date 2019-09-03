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
    dotacion_inicial_A = 100 - self.session.config['treatment']*20
    dotacion_inicial_B = 10 + self.session.config['treatment']*20
    pagos_x_A = 40
    pagos_x_B = 20

    #dotacion_inicial = 100
    #pagos_x = 20

    # Instrucciones
    instructions = 'injustice/Instructions.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)


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
        players = self.get_players()
        
        for p in players:
            if self.precio_aceptado is True:
                if p.bien_x is True:
                    p.payoff = p.dotacion_A - self.precio + c(Constants.pagos_x_A) + p.pago_anterior + p.extraccion
                else:
                    p.payoff = p.dotacion_A + self.precio + p.pago_anterior + p.extraccion
            else:
                if p.bien_x is True:
                    p.payoff = p.dotacion + c(Constants.pagos_x) + p.pago_anterior + p.extraccion
                else:
                    p.payoff = p.dotacion + p.pago_anterior + p.extraccion

            if self.precio_aceptado is True:
                if p.bien_x is True:
                    p.payoff = p.dotacion - self.precio + c(Constants.pagos_x) + p.pago_anterior - p.extraccion
                else:
                    p.payoff = p.dotacion + self.precio + p.pago_anterior - p.extraccion
            else:
                if p.bien_x is True:
                    p.payoff = p.dotacion + c(Constants.pagos_x) + p.pago_anterior - p.extraccion
                else:
                    p.payoff = p.dotacion + p.pago_anterior - p.extraccion

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

    def extraccion_max(self):
        return self.dotacion
