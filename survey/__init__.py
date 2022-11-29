
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    age = models.IntegerField(label='What is your age', max=125, min=13)
    econ = models.BooleanField(label='Are you, or do you plan to be, an economics major?')
    gender = models.StringField(choices=[['Male', 'Male'], ['Female', 'Female']], label='What is your gender', widget=widgets.RadioSelect)
    lotto = models.StringField(choices=[['0', 'Zero'], ['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5+', '5 or more times']], label='How many times have you played the lottery in the past year?', widget=widgets.RadioSelect)
    risk_seeking = models.StringField(choices=[['Highly Risk Seeking', 'Highly Risk Seeking'], ['Somewhat Risk Seeking', 'Somewhat Risk Seeking'], ['Neutral', 'Neutral'], ['Somewhat Risk Averse', 'Somewhat Risk Averse'], ['Highly Risk Averse', 'Highly Risk Averse']], label='Do you consider yourself to be risk seeking or risk averse?', widget=widgets.RadioSelect)
    fair = models.IntegerField(label = 'In a pure public good scenario like stage one of our experiment, what is the “fair” contribution level out of $10 (you may define “fair” however you like)?', min=0, max=10)
    candidate = models.BooleanField(label = 'Have you ever donated to a political campaign?')
    charity = models.BooleanField(label = 'Have you ever donated significant sums of money or time to a charity?')
    rate_us = models.IntegerField(label = 'How would you rate your overall experience in this experiment?', min=1, max=10)
    pumpkin = models.IntegerField(label = 'On a scale from 1-10, how much do you enjoy going to a pumpkin patch?', min=1, max=10)

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'econ', 'lotto','candidate', 'charity', 'risk_seeking', 'fair', 'pumpkin', 'rate_us']

page_sequence = [Demographics]