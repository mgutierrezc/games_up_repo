from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, levenshtein, distance_and_ok
from django.conf import settings


class Transcribe(Page):
    form_model = 'player'
    form_fields = ['transcribed_text']

    def vars_for_template(self):
        return dict(
            image_path='real_effort/paragraphs/{}.png'.format(self.round_number),
            reference_text=Constants.reference_texts[self.round_number - 1],
            debug=settings.DEBUG,
            required_accuracy=100 * (1 - Constants.allowed_error_rates[self.round_number - 1])
        )


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        table_rows = []
        for prev_player in self.player.in_all_rounds():
            row = dict(
                round_number=prev_player.round_number,
                reference_text_length=len(Constants.reference_texts[prev_player.round_number - 1]),
                transcribed_text_length=len(prev_player.transcribed_text),
                distance=prev_player.levenshtein_distance
            )
            table_rows.append(row)

        return dict(table_rows=table_rows)


page_sequence = [Transcribe, Results]
