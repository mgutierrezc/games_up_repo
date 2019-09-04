from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import config_values as cv

# Primero reciben instrs, luego info de sus dots y despues transan (Ultimatum con chat). Al terminar la transac,
# ven los results e inic otra ronda (en oontrol). En trat, hay una opc de seize al pasar las instrucs


class Introduction(Page):
    def before_next_page(self):
        if self.player.role() == 'A':
            self.player.bien_x = False
        else:
            self.player.bien_x = True

        if self.round_number > 1:
            self.player.bien_x = self.player.in_round(self.round_number - 1).bien_x
            self.player.pago_anterior = self.player.in_round(self.round_number - 1).payoff
            self.player.pago_anterior = self.player.in_round(self.round_number - 1).payoff
###CAMBIO MÁS RECIENTE: EVALUARLO##########(16:10 martes 3 de setiembre)
    def is_displayed(self):
        if self.round_number == 1:
           return True
        elif self.round_number == 2:
            return self.group.in_round(self.round_number - 1).precio_aceptado is False
        else:
            if self.group.in_round(self.round_number - 2).precio_aceptado is False:
                return self.group.in_round(self.round_number - 1).precio_aceptado is False
#################



class Neutral(Page):
    form_model = 'player'
    form_fields = ['neutral']

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False


class Chat(Page):
    timeout_seconds = 60

    def is_displayed(self):

      #  if self.round_number == 1:
       #     return True
        #else:
         #   if self.group.in_round(self.round_number - 1).precio_aceptado is False:
          #      return True
           # else:
            #    return False

        if self.round_number == 1:
           return True
        elif self.round_number == 2:
            return self.group.in_round(self.round_number - 1).precio_aceptado is False
        else:
            if self.group.in_round(self.round_number - 2).precio_aceptado is False:
                return self.group.in_round(self.round_number - 1).precio_aceptado is False


class Extraccion(Page):
    #form_model = 'player'
    form_model = 'group'
    form_fields = ['extraccion']

    # Solo se mostará si estamos en el tratamiento
    def is_displayed(self):
        if self.session.config['treatment'] == 0 and self.player.role() == 'A' and self.round_number == 1:
            return False
        elif self.session.config['treatment'] == 1 and self.player.role() == 'A' and self.round_number == 1:
            return True

class Robo_resultados(Page):
    def is_displayed(self):
        if self.session.config['treatment'] == 0 and self.player.role() == 'B' and self.round_number == 1:
            return False
        elif self.session.config['treatment'] == 1 and self.player.role() == 'B' and self.round_number == 1:
            return True


class Espera(WaitPage):
    pass


class Oferta(Page):
    form_model = 'group'
    form_fields = ['precio']

    def is_displayed(self):
        if self.round_number == 1:
            return self.player.bien_x is False
        elif self.round_number == 2:
            if self.group.in_round(self.round_number - 1).precio_aceptado is False:
                return self.player.bien_x is False
            else:
                return False
        else:
            if self.group.in_round(self.round_number - 2).precio_aceptado is False:
                if self.group.in_round(self.round_number-1).precio_aceptado is False:
                    return self.player.bien_x is False
            else:
                return False


class Aceptar_Oferta(Page):
    form_model = 'group'
    form_fields = ['precio_aceptado']

  #  def is_displayed(self):
   #     return self.player.bien_x is True

    def is_displayed(self):
        if self.round_number == 1:
            return self.player.bien_x is True
        elif self.round_number == 2:
            if self.group.in_round(self.round_number - 1).precio_aceptado is False:
                return self.player.bien_x is True
            else:
                return False
        else:
            if self.group.in_round(self.round_number - 2).precio_aceptado is False:
                if self.group.in_round(self.round_number-1).precio_aceptado is False:
                    return self.player.bien_x is True
            else:
                return False





class EsperaResultados(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        if self.group.precio_aceptado is True:
            self.group.compra_x()



class Results(Page):
    pass

    def is_displayed(self):
        if self.round_number == 1:
           return True
        elif self.round_number == 2:
            return self.group.in_round(self.round_number - 1).precio_aceptado is False
        else:
            if self.group.in_round(self.round_number - 2).precio_aceptado is False:
                return self.group.in_round(self.round_number - 1).precio_aceptado is False


page_sequence = [
    Introduction,
    Neutral,
    Extraccion,
    Espera,
    Robo_resultados,
    Espera,
    Chat,
    Oferta,
    Espera,
    Aceptar_Oferta,
    EsperaResultados,
    Results
]
