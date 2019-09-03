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
    robo = 20

    #dotacion_inicial = 100
    #pagos_x = 20

    # Instrucciones
    instructions = 'injustice/Instructions.html'


class Subsession(BaseSubsession):
    def creating_session(self):
        groups = self.get_groups()
        for g in groups:
            if g.precio_aceptado is True:
                self.group_randomly(fixed_id_in_group=True)

        for p in self.get_players():
            p.dotacion_A -= self.session.config['treatment']*20
            p.dotacion_B += self.session.config['treatment'] * 20

class Group(BaseGroup):
    # Precio
    precio = models.FloatField(max=Constants.dotacion_inicial_A, min=0)

    #######################################################################
    extraccion = models.BooleanField(initial=False)
    #######################################################################

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
        # oTree no les permite usar los fields de player directamente si estan en la clase Group
        # por ello, otree tiene algunas funciones que les pueden ayudar, por ej. get_player_by_role

        jugador_A = self.get_player_by_role('A')
        jugador_B = self.get_player_by_role('B')

        if self.precio_aceptado is True:
            #jugador_A.payoff = jugador_A.dotacion_A - self.precio + c(Constants.pagos_x_A) + (jugador_A.extraccion)*c(Constants.robo)
            jugador_A.payoff = jugador_A.dotacion_A - self.precio + c(Constants.pagos_x_A) + (self.extraccion) * c(Constants.robo)
            # El jugador A es el que extrae, asi que al hacer el calculo de pagos para B, necesitan usar el
            # valor de lo extraido por A, no por B como estaba en su codigo anterior (ya que este seria 0 al no
            # ser el que extrae)
            #jugador_B.payoff = jugador_B.dotacion_B + self.precio - (jugador_A.extraccion)*c(Constants.robo)
            jugador_B.payoff = jugador_B.dotacion_B + self.precio - (self.extraccion) * c(Constants.robo)

        else:
            #jugador_A.payoff = jugador_A.dotacion_A + (jugador_A.extraccion)*c(Constants.robo)
            jugador_A.payoff = jugador_A.dotacion_A + (self.extraccion) * c(Constants.robo)
            #jugador_B.payoff = jugador_B.dotacion_B + c(Constants.pagos_x_B) - (jugador_A.extraccion) * c(Constants.robo)
            jugador_B.payoff = jugador_B.dotacion_B + c(Constants.pagos_x_B) - (self.extraccion)*c(Constants.robo)


#######################################################
class Player(BasePlayer):
    # Variable para saber si alguien tiene o no el bien x (True lo tiene, False no)
    bien_x = models.BooleanField()
    dotacion_A = models.CurrencyField(initial=Constants.dotacion_inicial_A)
    dotacion_B = models.CurrencyField(initial=Constants.dotacion_inicial_B)
    neutral = models.CurrencyField(max=Constants.dotacion_inicial_A, min =0, initial=0)
    #extraccion = models.BooleanField()
    #extraccion = models.CurrencyField(max=Constants.dotacion_inicial_A, min =0, initial=0)
    # Pago ronda anterior
    pago_anterior = models.CurrencyField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'

    # extraccion solo sería para los jugadores tipo A
    def extraccion_max(self):
        return self.dotacion_A
