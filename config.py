import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')