from flask import Flask
from flask_bootstrap import Bootstrap
from config import *

CONFIG = DevelopmentConfig

server = Flask(__name__)
Bootstrap(server)

server.config.from_object(CONFIG)

from routes import *


if __name__ == "__main__":
    server.run()
