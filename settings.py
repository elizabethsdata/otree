from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(
    name='my_session',
     num_demo_participants=3,
     app_sequence=['public_goods_simple', 'survey'],
     use_browser_bots = False,
     frac_lottery = 0,
     multiplier = .5
    ), 
    dict(
     name = "pure_pg_5x",
     num_demo_participants=3,
     app_sequence=['public_goods_simple'],
     use_browser_bots = False,
     frac_lottery = 0,
     multiplier = .5 
    ),
     dict(
     name = "50_lottery_5x",
     num_demo_participants=3,
     app_sequence=['public_goods_simple'],
     use_browser_bots = False,
     frac_lottery = .5,
     multiplier = .5 
    ),
      dict(
     name = "pure_lottery_5x",
     num_demo_participants=3,
     app_sequence=['public_goods_simple'],
     use_browser_bots = False,
     frac_lottery = 1,
     multiplier = .5 
    ),
      dict(
     name = "Survey",
     num_demo_participants=3,
     app_sequence=['survey'],
    ),
    dict(name='my_session2', num_demo_participants=None, app_sequence=['public_goods_simple'], my_key=0)]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['one', 'two', 'three']
SESSION_FIELDS = []
ROOMS = [dict(name='econ380', display_name='econ380')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


