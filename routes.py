from main import server, CONFIG
from bot import bot
import bot_functions
from utils import login_check
from flask import request, render_template, redirect, url_for, session
import telebot
import datetime
import db_connect


# ============== web gui routes ==============
@server.route('/')  # main page
@login_check
def index():
    # rates = bot_functions.get_rates('web')
    # byn_cost = bot_functions.get_byn_cost('web')
    # exchange_rates = bot_functions.get_exchange_rates('web')

    # this values used for local testing
    rates = ('aaa', 'bbb', 'ccc', 'ddd')
    byn_cost = ('aaa', 'bbb', 'ccc', 'ddd')
    exchange_rates = ('aaa', 'bbb', 'ccc', 'ddd')

    return render_template('index.html', title='Bynny::Main', rates=rates, byn_cost=byn_cost,
                           exchange_rates=exchange_rates)


@server.route('/login', methods=['GET', 'POST'])  # login page
def login():
    error = None
    year = datetime.datetime.now()
    if request.method == 'POST':
        if request.form['username'] != server.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != server.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', title='Bynny', css='static/login.css', error=error, year=year.year)


@server.route('/logout')  # log out route
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@server.route('/stat')  # bot usage statistic page
@login_check
def stat():
    with db_connect.UseDatabase(CONFIG.DB_CONFIG) as cursor:
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


@server.route('/log')  # bot requests log from database
@login_check
def log():
    rows_num = request.args.get('rows', default=5)
    with db_connect.UseDatabase(CONFIG.DB_CONFIG) as cursor:
        _SQL = """SELECT * FROM (SELECT * FROM requests ORDER BY id DESC LIMIT %s) t ORDER BY id;""" % rows_num
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    return render_template('log.html', title='Bynny::Log', the_data=contents, rows=rows_num)


@server.route('/ctrl')  # webhook control page
@login_check
def ctrl():
    return render_template('ctrl.html', title='Bynny::Control room')


# ============== bot routes ==============
@server.route('/' + CONFIG.TOKEN, methods=['POST'])  # get messages
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/swh")  # set webhook
def st_webhook():
    bot.remove_webhook()
    bot.set_webhook(CONFIG.SERVER_URL + CONFIG.TOKEN)
    return "!",


@server.route("/rwh")  # remove webhook
def rm_webhook():
    bot.remove_webhook()
    return "!",
