from db_connect import UseDatabase


class BotService:

    def get_national_bank_exchange_rates(self):
        pass

    def get_best_exchange_rates(self):
        pass

    def get_exchange_trading_results(self):
        pass

    def get_byn_cost(self):
        pass


class WebService:

    def __init__(self, db_connector: UseDatabase):
        self.db_connector = db_connector

    def get_unique_users(self):
        _SQL = """SELECT COUNT(DISTINCT user_id) FROM requests;"""
        return self._execute(_SQL)

    def get_most_usage_commands(self):
        _SQL = """SELECT user_message, count(*) c FROM requests GROUP BY user_message ORDER BY c DESC LIMIT 3;"""
        return self._execute(_SQL)

    def get_most_active_users(self):
        _SQL = """SELECT user_id, first_name FROM requests GROUP BY user_id ORDER BY COUNT(user_id) DESC LIMIT 3;"""
        return self._execute(_SQL)

    def show_log(self, rows_num: int):
        _SQL = """SELECT * FROM (SELECT * FROM requests ORDER BY id DESC LIMIT %s) t ORDER BY id;"""
        return self._execute(_SQL, (rows_num,))

    def _execute(self, sql_query: str, params: tuple = None):
        with self.db_connector as cursor:
            if params:
                cursor.execute(sql_query, params)
            else:
                cursor.execute(sql_query)
            return cursor.fetchall()
