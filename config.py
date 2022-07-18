import os
from dataclasses import dataclass
import telebot
from flask import Flask
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), 'config.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass
class BaseConfig:
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    TOKEN = os.getenv('TOKEN')
    DB_CONFIG = {'host': os.getenv('DB_HOST'),
                 'user': os.getenv('DB_USER'),
                 'password': os.getenv('DB_PASS'),
                 'database': os.getenv('DB_NAME')}
    SERVER_URL = os.getenv('SERVER_URL')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_USE_MINIFIED = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.getenv('DEV_SECRET_KEY')
    DB_CONFIG = {'host': os.getenv('DEV_DB_HOST'),
                 'user': os.getenv('DEV_DB_USER'),
                 'password': os.getenv('DEV_DB_PASS'),
                 'database': os.getenv('DEV_DB_NAME')}
    USERNAME = os.getenv('DEV_USERNAME')
    PASSWORD = os.getenv('DEV_PASSWORD')


class ProductionConfig(BaseConfig):
    DEBUG = False


CONFIG = ProductionConfig

app = Flask(__name__)
app.config.from_object(CONFIG)
Bootstrap(app)

bot = telebot.TeleBot(app.config['TOKEN'])
