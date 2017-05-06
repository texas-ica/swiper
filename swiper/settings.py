import os

class Config:
    BOT_NAME = 'swiper'
    BOT_USERNAME = '@swiper'
    SKIP_FIRST = True
    WEBSOCKET_DELAY = 1
    COMMANDS = ['/help', '/announce', '/poll']
    IMGUR_CLIENT_ID = '2e3219e30b7d439'
    IMGUR_CLIENT_SECRET = '00e38fa4888d39362b02a1c4b6349a1ea624a3d9'
    PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProductionConfig(Config):
    BOT_ID = 'U4VUB4TSA'
    API_KEY = 'xoxb-165963163894-Fi1D3Gegl5WorvxxYk77Mnd9'
    USERS = {
        'adhitya_ganesh': 'U4BLBJJCD',
        'adi49770': 'U4Q0PS676',
        'ayushi.sharma': 'U4Q8HKBHT',
        'bansri.m': 'U4QAVMMJ6',
        'barun.das': 'U4BAJP3ML',
        'chamali_raigama': 'U4BAURE87',
        'jay_patel': 'U4PK0D8PJ',
        'km': 'U4PV465S6',
        'komaldesai': 'U4BBCC6RL',
        'marwa.gujarathi': 'U4PUYM94J',
        'minorie': 'U48K5FJET',
        'mjsantani': 'U4ANWJSAY',
        'nikhita.pendekanti': 'U4Q257KGV',
        'paayal': 'U4796211P',
        'rishabhdhar': 'U49VCV5CH',
        'salonisingal': 'U484591R8',
        'sanju98': 'U4PV2E0R0',
        'shaziagupta': 'U4Q0RJDMJ',
        'shreydesai': 'U4P91AZ97',
        'swiper': 'U4VUB4TSA',
        'slackbot': 'USLACKBOT'
    }
    CHANNELS = {
        'hi': 'C4QDJULBE',
        'lit_social_random': 'C481EN3RT',
        'random': 'C481EN477',
        'website-team': 'C4U2G6T9D',
        'ica_exec_board_17-18': 'G4QB5C1C2',
        'announcements': 'G4VB09HM3',
        'swiper-test': 'G4VUDMUMC',
        'technology': 'G4PKY5CM6'
    }


class TestingConfig(Config):
    BOT_ID = 'U4RRU4GBH'
    API_KEY = 'xoxb-164283383056-WzuziW4JRkDLTH2nLu7qmVzv'
    USERS = {
        'shreydesai': 'U4QEWD465',
        'niksrd': 'U4R6JTPJQ',
        'swiper':'U4U8BB91N'
    }
    CHANNELS = {
        'general': 'C4RRSJW5V',
        'announcements': 'C4R5R5ZRQ'
    }
