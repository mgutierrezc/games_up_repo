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
    # no serían solo tres rondas?

    # Escojan aquí la dotac del comprador y los pagos recibidos por poseer el bien x
    # OJO: acá deberíamos definir dos pagos: uno para A y uno para B
    dotacion_A_nt = 100
    dotacion_B_nt = 10
    dotacion_A_t = 90
    dotacion_B_t = 20
    pago_x_a = 3
    pago_x_b = 1
    extraccion = 20

    # Instrucciones
    instructions = 'injustice/Instructions.html'


class Subsession(BaseSubsession):
    pass

# Las variables cambian principalmente entre parejas
class Group(BaseGroup):
    # define la variable precio como una variable float = un número sin restricciones
    precio = models.FloatField(min=0)
    # Variable para registrar si hubo (True) o no transaccion (False)
    transaccion = models.BooleanField()

    # define los payoffs
    def set_payoffs(self):
        # usa a los jugadores que están en el grupo
        players = self.get_players()
        # cada jugador será representado con p
        for p in players:
            # debería definirse en la sección de players la variable round_number.
            # define la variable pago_anterior que permite acumular los payoffs de rondas anteriores.
            #if self.round_number > 1:
                #p.pago_anterior = p.in_round(self.round_number - 1).payoff

            if p.role() == 'A':
            # ******* ESTO APLICA PARA EL JUGADOR A *******
                if self.transaccion is True:
                    #if p.bien_x is True:
                        #p.payoff = p.dotacion - self.precio + Constants.pago_x_a + p.pago_anterior + p.extraccion
                    p.payoff = p.dotacion - self.precio + Constants.pago_x_a + Constants.extraccion
                    # else:
                        #p.payoff = p.dotacion + self.precio + p.pago_anterior + p.extraccion

                else:
                    #if p.bien_x is True:
                        #p.payoff = p.dotacion + Constants.pago_x_a + p.pago_anterior + p.extraccion
                    #else:
                        #p.payoff = p.dotacion + p.pago_anterior + p.extraccion
                    p.payoff = p.dotacion + Constants.extraccion

            # ******* ESTO APLICA PARA EL JUGADOR B *******
            else:
                if self.transaccion is True:
                    #if p.bien_x is True:
                        #p.payoff = p.dotacion - self.precio + Constants.pago_x_b + p.pago_anterior - p.extraccion

                    #else:
                        #p.payoff = p.dotacion + self.precio + p.pago_anterior - p.extraccion
                    p.payoff = p.dotacion + self.precio - Constants.extraccion

                else:
                    #if p.bien_x is True:
                        #p.payoff = p.dotacion + Constants.pago_x_b + p.pago_anterior - p.extraccion
                    p.payoff = p.dotacion + Constants.pago_x_b - Constants.extraccion

                    #else:
                        #p.payoff = p.dotacion + p.pago_anterior - p.extraccion


class Player(BasePlayer):
    # Variable para saber si alguien tiene o no el bien x (True lo tiene, False no) - probablemente no nos sirva
    #bien_x = models.BooleanField()
    # Define la dotación
    dotacion = models.FloatField()
    # Define la extracción (robo) - debería ser una constante
    #extraccion = models.FloatField(min=0, initial=0)
    # Pago de la ronda anterior
    pago_anterior = models.IntegerField(initial=0)

    # define la función rol(player) = A o B
    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'

    #def extraccion_max(self):
        #return