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

class Chat(Page):
    pass


class Extraccion(Page):
    form_model = 'player'
    form_fields = ['extraccion']

    # Solo se mostará si estamos en el tratamiento
    def is_displayed(self):
        if self.session.config['treatment'] == 0 and self.player.role() == 'A':
            return False
        elif self.session.config['treatment'] == 1 and self.player.role() == 'A':
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


class EsperaResultados(WaitPage):
    def after_all_players_arrive(self):
        players = self.group.get_players()
        for p in range(1, 3):
            if self.group.precio_aceptado is True:
                if players[p].bien_x is False:
                    self.players[p].bien_x = False
                else:
                    self.players[p].bien_x = True


class Results(Page):
    pass


page_sequence = [
    Introduction,
    Extraccion,
    Espera,
    Chat,
    Oferta,
    Espera,
    Aceptar_Oferta,
    EsperaResultados,
    Results
]
