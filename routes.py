from config import app
from bot import bot
import bot_service
from utils import login_check
from flask import request, render_template, redirect, url_for, session
import telebot
import datetime
import db_connect
from services import WebService, BotService

web_service = WebService(
    db_connect.UseDatabase(app.config['DB_CONFIG'])
)


# ============== web gui routes ==============
@app.route('/')
@login_check
def index():
    # rates = bot_service.get_rates()
    # byn_cost = bot_service.get_byn_cost()
    # exchange_rates = bot_service.get_exchange_rates()

    # this values used for local testing
    rates = ('aaa', 'bbb', 'ccc', 'ddd')
    byn_cost = ('aaa', 'bbb', 'ccc', 'ddd')
    exchange_rates = ('aaa', 'bbb', 'ccc', 'ddd')

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
    unique_users = web_service.get_unique_users()
    most_usage_commands = web_service.get_most_usage_commands()
    most_active_users = web_service.get_most_active_users()
    context = {
        'title': 'Bynny::Statistics',
        'unique_users': unique_users,
        'command': most_usage_commands,
        'top_users': most_active_users
    }

    return render_template('stat.html', **context)


@app.route('/log')
@login_check
def log():
    rows_num = int(request.args.get('rows', default=5))
    data = web_service.get_log(rows_num)
    context = {
        'title': 'Bynny::Log',
        'data': data,
        'rows_num': rows_num
    }
    return render_template('log.html', **context)


@app.route('/management')
@login_check
def management():
    return render_template('ctrl.html', title='Bynny::Control room')


# ============== bot routes ==============
@app.route('/' + app.config['TOKEN'], methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/swh")
def st_webhook():
    bot.remove_webhook()
    bot.set_webhook(app.config['SERVER_URL'] + app.config['TOKEN'])
    return "!", 200


@app.route("/rwh")
def rm_webhook():
    bot.remove_webhook()
    return "!", 200
