# Some useful utils

import db_connect
import datetime
from flask import session, redirect, url_for
from functools import wraps
from main import CONFIG


# is logged check
def login_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


# writing bot request to database
def log_to_db(message, answer):
    timestamp = datetime.datetime.fromtimestamp(message.date)
    if message.from_user.last_name is None:
        last_name = 'NOT_SET'
    else:
        last_name = message.from_user.last_name

    if message.from_user.username is None:
        username = 'NOT_SET'
    else:
        username = message.from_user.username

    with db_connect.UseDatabase(CONFIG.DB_CONFIG) as cursor:
        _SQL = """insert into requests
                  (user_id, first_name, last_name, username, user_message, bot_answer, bot_timestamp)
                  values
                  (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (message.from_user.id,
                              message.from_user.first_name,
                              last_name,
                              username,
                              message.text,
                              answer,
                              timestamp,))
