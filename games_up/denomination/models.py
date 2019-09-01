from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import config_values as cv

author = 'Your name here'

doc = """
Denomination game
"""


class Constants(BaseConstants):
    name_in_url = 'denomination'
    # Para cambiar el numero total de participantes (no por grupos), vayan al archivo config_values.py. Esta dentro
    # del proyecto, pero fuera del app
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
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        players = self.get_players()
        for p in players:
            # Payoff es una variable predefinida en otree para asignar los pagos por ronda o finales
            # Aquí la defino como la dotacion recibida menos el gasto
            p.payoff = Constants.dotacion - p.gasto


class Player(BasePlayer):
    # Asignamos a quienes hayan sido elegidos aleatoriamente como la primera mitad de los jugadores
    def role(self):
        if self.id_in_group <= cv.num_participants/2:
            return 'Soles'
        else:
            return 'Centavos'

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    # Crearemos aquí las variables que almacenen las respuestas de la encuesta inicial
    # Si una pregunta implica una pregunta con opciones, créenla de esta forma (RadioSelect es un widget
    # para mostrar a las personas las respuestas como alternativas de opción múltiple)
    sexo = models.StringField(
        choices=['Masculino', 'Femenino'],
        label='¿Cuál es tu sexo?',
        widget=widgets.RadioSelect)
    # Si implica respuestas numéricas (Enteras). Usar FloatField si quieren con decimales
    edad = models.IntegerField(label='¿Cuál es tu edad?')

    # Verificador de que se cumple la restriccion impuesta por la dotac
    incorrect = models.IntegerField()

    # Crearemos aquí las variables que almacenen el número de pedidos de los bienes que quieren comprar
    bien1 = models.IntegerField(label='¿Cuánto quieres comprar del bien 1? Precio: {}'.format(Constants.precio1))
    bien2 = models.IntegerField(label='¿Cuánto quieres comprar del bien 2? Precio: {}'.format(Constants.precio2))

    # Creamos una variable que guarde lo gastado en las compras y el vuelto
    gastos = models.FloatField(max=5, min=0)


