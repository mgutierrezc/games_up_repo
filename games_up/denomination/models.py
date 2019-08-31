from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random, itertools

author = 'Your name here'

doc = """
Denomination game
"""


class Constants(BaseConstants):
    name_in_url = 'denomination'
    players_per_group = None
    # Dinero con el que inician el juego
    dotacion = 5
    # Escojan el número de rondas aquí abajo
    num_rounds = 1
    # Definiremos aquí el costo de los bienes ofrecidos
    precio1 = 2
    precio2 = 3
    instructions_template = 'denomination/Instructions.html'



class Subsession(BaseSubsession):
    def creating_session(self):
        # En cada ronda, se aleatorizará el rol (si recibirán 5 soles en duro o en varias monedas)
        # Si quieren que los roles permanezcan fijos, quiten las comillas del siguiente código en lugar
        # del código actual de este método
        """
        if self.round_number == 1:
        'Añadir una tabulación a las lineas siguientes'
        """
        players = self.get_players()
        random.shuffle(players)
        treatments = itertools.cycle(['Soles', 'Centavos'])
        for p in players:
            # Esta es una variable auxiliar que nos permite realizar la asignación aleatoria de roles, pero no la
            # registra en la base de datos creada por otree
            p.participant.vars['rol'] = treatments.next()

class Group(BaseGroup):
    def set_payoffs(self):
        players = self.get_players()
        for p in players:
            # Payoff es una variable predefinida en otree para asignar los pagos por ronda o finales
            # Aquí la defino como la dotacion recibida menos el gasto
            p.payoff = Constants.dotacion - p.gasto


class Player(BasePlayer):
    # Para que puedan ver quién está en cada tratamiento, crearemos una variable (field en otree) que lo registre en
    # nuestros datos (igualaremos su valor al de la variable auxiliar)
    rol = models.StringField()

    # Crearemos aquí las variables que almacenen las respuestas de la encuesta inicial
    # Si una pregunta implica una pregunta con opciones, créenla de esta forma (RadioSelect es un widget
    # para mostrar a las personas las respuestas como alternativas de opción múltiple)
    sexo = models.StringField(
        choices=['Masculino', 'Femenino'],
        label='¿Cuál es tu sexo?',
        widget=widgets.RadioSelect)
    # Si implica respuestas numéricas (Enteras). Usar FloatField si quieren con decimales
    edad = models.IntegerField(label='¿Cuál es tu edad?')

    # Crearemos aquí las variables que almacenen el número de pedidos de los bienes que quieren comprar
    bien1 = models.IntegerField(label='¿Cuánto quieres comprar del bien 1?')
    bien2 = models.IntegerField(label='¿Cuánto quieres comprar del bien 2?')

    # Creamos una variable que guarde lo gastado en las compras y el vuelto
    gastos = models.FloatField(max=5, min=0)


