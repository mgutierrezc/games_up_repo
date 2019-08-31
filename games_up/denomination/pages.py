from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# Deben crear un archivo .html por cada pagina que quieran que se muestre al jugador y que esté registrada aquí como una
# clase, a excepción de los waitpages

class Introduction(Page):
    # Aquí se presentan las reglas básicas del experimento
    pass

class Encuesta(Page):
    form_model = 'player'
    # Aquí escriben todas las variables que representan las respuestas que quieren de sus jugadores
    form_fields = ['sexo', 'edad']

class Espera(WaitPage):
    # Página que hará esperar a los jugadores que hayan terminado la encuesta hasta que los demás la hayan llenado.
    # Si no quieren que los jugadores esperen a los demás antes de pasar a la siguiente parte, borren esta clase y de
    # la lista page_sequence
    title_text = "Página de Espera"
    body_text = "Por favor, espere a que los demás terminen la sección anterior"
    def after_all_players_arrive(self):
        pass

class Compra(Page):
    form_model = 'player'
    form_fields = ['bien1', 'bien2']

class Results(Page):
    def vars_for_template(self):
        player = self.player
        dotacion = Constants.dotacion
        vuelto = player.payoff - (Constants.precio1*player.bien1 + Constants.precio2*player.bien2)
        return {'dotacion': dotacion, 'vuelto': vuelto}


page_sequence = [
    Introduction,
    Encuesta,
    Espera,
    Compra,
    Espera,
    Results
]