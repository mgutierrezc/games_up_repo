from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import config_values as cv


class Introduction(Page):
    def before_next_page(self):
        self.session.vars['ofertas_pujas'] = list()


class Oferta(Page):
    form_model = 'player'
    form_fields = ['oferta']
    timeout_seconds = 60

    def vars_for_template(self):
        valor = self.player.valoracion
        return dict(valor=valor)

    def is_displayed(self):
        return self.player.role() == 'Ofertante'

    def before_next_page(self):
        player = self.player
        self.session.vars['ofertas_pujas'].append(player.oferta)

    def oferta_error_message(self, value):
        if value < self.player.valoracion:
            return 'El precio no puede ser mayor al costo'


class Puja(Page):
    form_model = 'player'
    form_fields = ['puja']
    timeout_seconds = 60

    def vars_for_template(self):
        valor = self.player.valoracion
        return dict(valor=valor)

    def is_displayed(self):
        return self.player.role() == 'Comprador'

    def before_next_page(self):
        player = self.player
        session = self.session
        session.vars['ofertas_pujas'].append(player.puja)

    def puja_error_message(self, value):
        if value > self.player.valoracion:
            return 'El precio no puede ser mayor a la utilidad'


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        session = self.session
        session.vars['ofertas_pujas'].sort(reverse=True)
        # Ubicación de la oferta/puja que debe ser registrada
        index = int((cv.num_participants/2)-1)
        self.group.cleaning_price = session.vars['ofertas_pujas'][index]


class Results(Page):
    def vars_for_template(self):
        pago = self.player.payoff
        return dict(pago=pago)


page_sequence = [
    Introduction,
    Oferta,
    Puja,
    ResultsWaitPage,
    Results
]
