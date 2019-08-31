from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import config_values as cv

# Primero reciben instrs, luego info de sus dots y despues transan (Ultimatum con chat). Al terminar la transac,
# ven los results e inic otra ronda (en oontrol). En trat, hay una opc de seize al pasar las instrucs


class Introduction(Page):
    pass


class Extraccion(Page):
    form_model = 'player'
    form_fields = ['extraccion']

    # Solo se mostará si estamos en el tratamiento
    def is_displayed(self):
        if self.session.config['treatment'] == 0:
            return False
        else:
            return True


class Espera(WaitPage):
    def after_all_players_arrive(self):
        pass


class Transaccion(Page):
    pass

class Results(Page):
    pass


page_sequence = [
    MyPage,
    Espera,
    Results
]
