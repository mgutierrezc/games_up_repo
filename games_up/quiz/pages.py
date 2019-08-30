from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Question(Page):
    form_model = 'player'
    form_fields = ['submitted_answer']

    def before_next_page(self):
        self.player.check_correct()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return dict(
            player_in_all_rounds=player_in_all_rounds,
            questions_correct=sum([p.is_correct for p in player_in_all_rounds])
        )


page_sequence = [
    Question,
    Results
]
