import requests
from datetime import datetime, timedelta, time
import sqlite3 as sql
import telebot
import matplotlib.pyplot as plt


token = '1549583803:AAH8qbTzM-n3h0cm9e3H7N6r2wuFTdQtHGQ'
bot = telebot.TeleBot(token)


key = '194d689380926a95b1dae3c566834ac3'
base_url = f'https://api.exchangeratesapi.io/v1/latest?access_key={key}&base=USD'
request = requests.get(base_url).json()


class Cur_list:
    """
    This class will write all available rates into database 'list.db' as currency: rate,
    e.q.: USD: 0.245
    """
    def __init__(self, msg):
        self.msg = msg

    def write_msg(self):
        """
        For new request
        """
        with open(f'{self.msg.chat.id}.txt', 'w') as w:
            for cur, rate in request['rates'].items():
                w.write(f'{cur}: {round(rate, 2)}\n')

    def send_msg(self):
        """
        For old request
        """
        with open(f'{self.msg.chat.id}.txt', 'r') as r:
            file = r.read().split('\n')
            for x in file:
                bot.send_message(self.msg.chat.id, x)

    def check_true(self, bool):
        if bool:
            bot.send_message(self.msg.chat.id, 'There are new')
            self.write_msg()
            self.send_msg()
        else:
            try:
                bot.send_message(self.msg.chat.id, 'There are old')
                self.send_msg()
            except FileNotFoundError:
                self.write_msg()
                self.send_msg()


def in_list(some_text):
    lst = []
    for cur in request['rates']:
        lst.append(cur)

    if some_text in lst:
        return True


class Exchange:
    """
    This class works with command /exchange.
    Method in_list() checks input currencies in saved list of available currencies.
    Method check_for_exchange() checks correct input request.
    convert() returns converted currencies
    """
    def __init__(self, text):
        self.text = [tx.upper() for tx in text ]

    def check_for_exchange(self):
        if len(self.text) == 4 and isinstance(float(self.text[0]), float) and \
                (self.text[1] == 'USD'):
            if (self.text[2].lower() == 'to') and in_list(self.text[3]):
                return True

    def convert(self):
        convert_url = f'https://api.exchangeratesapi.io/v1/convert?access_key={key}' \
                 f'&from={self.text[1]}&to={self.text[3]}&' \
                      f'amount={float(self.text[0])}'
        convert_request = requests.get(convert_url).json()
        return round(convert_request['result'], 2) # return 0.82 or 1.57


class History:
    """
    Works same as class Exchange.
    """
    def __init__(self, text, text_cur):
        self.text = text
        self.text_cur = [tx.upper() for tx in text_cur ]

    def check_for_history(self):
        if len(self.text) == 4 and in_list(self.text_cur[0]) and \
                in_list(self.text_cur[1]):
            if isinstance(int(self.text[2]), int) and self.text[1] == 'for' \
                    and self.text[3] == 'days':
                return True

    def history(self):
        global key
        users_period = (int(self.text[2]))
        date = datetime.now() - timedelta(days=users_period)
        val = [] # list where will save ascending params, e.q.:
        # [['2021-05-13', '0.856475'], ['2021-05-14', '0.856475']]

        for time in range(users_period):
            history_url = f'https://api.exchangeratesapi.io/v1/{date.strftime("%Y-%m-%d")}' \
                      f'?access_key={key}&base={self.text_cur[0]}&symbols={self.text_cur[1]}'
            status = requests.get(history_url).status_code
            history_request = requests.get(history_url).json()

            if status == 200:
                val.append(f'{history_request["date"]},'
                            f'{history_request["rates"][self.text_cur[1]]}'.split(','))

            date += timedelta(days=1)

        return val

    def figure(self, msg, val):
        """
        msg - users request need for personally save jpg graph
        """
        x = [x[0] for x in val] # for dates
        y = [y[1] for y in val] # for rates
        size = (len(val)+2, len(val))
        fig, ax = plt.subplots(figsize=size)
        ax.set_title(f'History {self.text[0]} {self.text[1]} {self.text[2]} {self.text[3]}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Rate')
        ax.grid(True)
        ax.plot(x, y, 'o-b', label=f'{self.text_cur[1]}')
        ax.legend(loc='upper left', fontsize=14)
        plt.savefig(f'img/{msg.chat.id}_figure.jpg', dpi=100) # save jpg graph for each user
        return f'img/{msg.chat.id}_figure.jpg'



