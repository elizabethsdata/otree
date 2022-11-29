from otree.api import *
import numpy as np 
import os
import pathlib
import string
import random 
c = cu

doc = ''

class C(BaseConstants):
    NAME_IN_URL = pathlib.PurePath(__file__).parent.name
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    ENDOWMENT = cu(10)
   # MULTIPLIER = 1
    MY_CONSTANT = 0
  #  FRACTION_LOTTERY = 0.5
    HISTORY_TEMPLATE = 'public_goods/history.html'
    HISTORY_CONT_TEMPLATE = 'public_goods/history_cont.html'
    INSTRUCTIONS2_TEMPLATE = 'public_goods/instructions2.html'
    INSTRUCTIONS_TEMPLATE = 'public_goods/' + pathlib.PurePath(__file__).parent.name + '.html'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    lottery_pot = models.CurrencyField()
    total_public_good = models.CurrencyField()
def set_payoffs(group: Group):

    players = group.get_players()
    contributions = [p.contribution for p in players]
    if sum(contributions) > 0 and group.session.config[C.NAME_IN_URL + '_frac_lottery'] > 0: 
        winner = random.choices([p for p in players], weights = contributions, k = 1)[0]
    else: 
        winner = 'nobody'
    group.total_contribution = sum(contributions)
    group.total_public_good = group.total_contribution*(1- group.session.config[C.NAME_IN_URL + '_frac_lottery'])
    group.individual_share = (
        group.total_public_good * group.session.config[C.NAME_IN_URL + '_multiplier']
        
    )
    group.lottery_pot = group.total_contribution*group.session.config[C.NAME_IN_URL + '_frac_lottery']
    for p in players:
        if p == winner: 
            p.lottery_status = 'won'
            p.lottery_winnings = group.lottery_pot
    
        p.payoff = 0 - p.contribution + group.individual_share + p.lottery_winnings 
        p.total_game = p.in_round(max(p.round_number - 1, 1)).total_game + p.payoff
class Player(BasePlayer):
    lottery_winnings = models.CurrencyField(initial=0, label='Lottery Winnings')
    lottery_status = models.StringField(initial='lost', label='Lottery Status')
    total_game = models.CurrencyField(initial = 10, label = 'Balance')
    contribution = models.CurrencyField(initial = 0, label='How much will you contribute?', min=0, max = 10)

#def contribution_max(player):
#    return (10 + sum([p.payoff for p in player.in_previous_rounds()]))
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']
    
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            num_players = len(group.get_players()),
            percent_lottery = str(round(100*player.session.config[C.NAME_IN_URL + '_frac_lottery'])) + "%",
            percent_public_goods = str(round((100*(1-player.session.config[C.NAME_IN_URL + '_frac_lottery'])))) + "%",
            total_contribution = sum([p.contribution for p in player.in_previous_rounds()]),
            total_payoff_game = sum([p.payoff for p in player.in_previous_rounds()]),
            lottery_frac =  str(100*np.mean([1 if p.lottery_status == 'won' else 0 for p in player.in_previous_rounds()])) + '%'
            

        )
  #  @staticmethod
  #  def get_timeout_seconds(player):
  #      return player.session.config['contribute_page_timeout']
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            num_players = len(group.get_players()),
            total_contribution = sum([p.contribution for p in player.in_all_rounds()]),
            total_payoff_game = sum([p.payoff for p in player.in_all_rounds()]),
            lottery_frac =  str(100*np.mean([1 if p.lottery_status == 'won' else 0 for p in player.in_all_rounds()])) + '%',
            total_public_share = sum([p.group.individual_share for p in player.in_all_rounds()]),
            percent_lottery = str(round(100*player.session.config[C.NAME_IN_URL + '_frac_lottery'])) + "%",
            percent_public_goods = str((100*(1-player.session.config[C.NAME_IN_URL + '_frac_lottery']))) + "%", 
        )
  #  @staticmethod
  # def get_timeout_seconds(player):
  #     return player.session.config['results_page_timeout']

class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        """
        Skip this page if the round number has exceeded the participant's designated
        number of rounds.
        """
        participant = player.participant
        return player.round_number < 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            testvar = pathlib.PurePath(__file__).parent.name
        )
class InstructionsWait(WaitPage):
   @staticmethod
   def is_displayed(player: Player):
        """
        Skip this page if the round number has exceeded the participant's designated
        number of rounds.
        """
        participant = player.participant
        return player.round_number < 2   
def creating_session(subsession):
    for p in subsession.get_players():
        p.participant.label = p.id_in_group

page_sequence = [Instructions, InstructionsWait, Contribute, ResultsWaitPage, Results]