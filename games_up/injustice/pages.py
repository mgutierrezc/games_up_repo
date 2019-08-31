from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import config_values as cv

# Primero reciben instrs, luego info de sus dots y despues transan (Ultimatum con chat). Al terminar la transac,
# ven los results e inic otra ronda (en oontrol). En trat, hay una opc de seize al pasar las instrucs


class Introduction(Page):
    pass


class Chat(Page):
    pass


class Extraccion(Page):
    form_model = 'player'
    form_fields = ['extraccion']

    # Solo se mostará si estamos en el tratamiento
    def is_displayed(self):
        if self.session.config['treatment'] == 0 and self.player.role() == 'A':
            return False
        else:
            return True


class Espera(WaitPage):
    pass


class Oferta(Page):
    form_model = 'group'
    form_fields = ['precio']

    def is_displayed(self):
        return self.player.bien_x is False


class Aceptar_Oferta(Page):
    form_model = 'group'
    form_fields = ['precio_aceptado']

    def is_displayed(self):
        return self.player.bien_x is True


class EsperaResultados(Page):
    def before_next_page(self):
        if self.group.precio_aceptado is True:
            if self.player.bien_x is False:
                self.player.bien_x = False
            else:
                self.player.bien_x = True

class Results(Page):
    pass


page_sequence = [
    Introduction,
    Extraccion,
    Espera,
    Oferta,
    Espera,
    Aceptar_Oferta,
    EsperaResultados,
    Results
]
