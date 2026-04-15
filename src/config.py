import os

class Config:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    DESCRIPTIONS_FILE = os.path.join(BASE_DIR, 'src/data/descriptions.json')
    DEBUG = True