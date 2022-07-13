from config import app
from bot import bot
import bot_service
from utils import login_check
from flask import request, render_template, redirect, url_for, session
import telebot
import datetime
import db_connect
from services import WebService

web_service = WebService(
    db_connect.UseDatabase(app.config['DB_CONFIG'])
)


# ============== web gui routes ==============
@app.route('/')
@login_check
def index():
    rates = bot_service.get_rates()
    byn_cost = bot_service.get_byn_cost()
    exchange_rates = bot_service.get_exchange_rates()

    # this values used for local testing
    # rates = ('aaa', 'bbb', 'ccc', 'ddd')
    # byn_cost = ('aaa', 'bbb', 'ccc', 'ddd')
    # exchange_rates = ('aaa', 'bbb', 'ccc', 'ddd')

    return render_template('index.html', title='Bynny::Main', rates=rates, byn_cost=byn_cost,
                           exchange_rates=exchange_rates)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    year = datetime.datetime.now()
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username or password'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', title='Bynny', css='static/login.css', error=error, year=year.year)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/stat')
@login_check
def stat():
    with db_connect.UseDatabase(app.config['DB_CONFIG']) as cursor:
        # unique bot users bu user_id
        _SQL = """SELECT COUNT(DISTINCT user_id) FROM requests;"""
        cursor.execute(_SQL)
        unique_users = cursor.fetchall()

        # most usage bot commands
        _SQL = """SELECT user_message, count(*) c FROM requests GROUP BY user_message ORDER BY c DESC LIMIT 3;"""
        cursor.execute(_SQL)
        command = cursor.fetchall()

        # 3 most active bot users
        _SQL = """SELECT user_id, first_name FROM requests GROUP BY user_id ORDER BY COUNT(user_id) DESC LIMIT 3;"""
        cursor.execute(_SQL)
        top_users = cursor.fetchall()
    return render_template('stat.html', title='Bynny::Statistics', unique_users=unique_users, command=command,
                           top_users=top_users)


@app.route('/log')
@login_check
def log():
    rows_num = request.args.get('rows', default=5)
    with db_connect.UseDatabase(app.config['DB_CONFIG']) as cursor:
        _SQL = """SELECT * FROM (SELECT * FROM requests ORDER BY id DESC LIMIT %s) t ORDER BY id;""" % rows_num
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    return render_template('log.html', title='Bynny::Log', the_data=contents, rows=rows_num)


@app.route('/ctrl')
@login_check
def ctrl():
    return render_template('ctrl.html', title='Bynny::Control room')


# ============== bot routes ==============
@app.route('/' + app.config['TOKEN'], methods=['POST'])  # get messages
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/swh")
def st_webhook():
    bot.remove_webhook()
    bot.set_webhook(app.config['SERVER_URL'] + app.config['TOKEN'])
    return "!",


@app.route("/rwh")
def rm_webhook():
    bot.remove_webhook()
    return "!",
