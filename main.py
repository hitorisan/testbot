import setting
from setting import *

start_time = datetime.now()
now = 0

@bot.message_handler(content_types=['text'])
def str(msg):
    try:
        if msg.text == '/start':
            ques = 'Hi 🖐. I will help you convert currency 💲! \n' \
                   'There are my functions:\n'
            ques1 = '1️⃣  /list - return list of all available rates (E.q.: AED: 3.67).\n' \
                    'And you should know - USD is my base currency.\n'
            ques2 = '2️⃣  /exchange 10 USD to EUR - this command for converting currencies. ' \
                    'Just type how many you need to convert and currency which will convert.'
            ques3 = '3️⃣  /history USD/AMD for 7 days - will return an image graph ' \
                    'which shows the exchange rate ' \
                    'of the selected currency for the last 7 days. If you want, ' \
                    'you can select another period,' \
                    ' but I understand only integer and only days.'
            msg_list = [ques, ques1, ques2, ques3]
            for ms in msg_list:
                bot.send_message(msg.chat.id, ms)

        elif msg.text == '/list':
            """
            Every 10 minutes bot will send request for all available rates. 
            now - will save current time, start_time - last users request. 
            If (now - start_time) > 600 sec, bot will use class Cur_list and 
            send new request to https://exchangeratesapi.io/.
            """
            global start_time, now
            now = datetime.now()
            if (now - start_time).seconds > 600:
                start_time = datetime.now()
                lst = Cur_list(msg)
                lst.check_true(True)

            else:
                now = datetime.now()
                lst = Cur_list(msg)
                lst.check_true(False)


        else:
            message = msg.text.split(' ')
            if message[0] == '/exchange':
                text = message[1::] # take list without '/exchange',
                # e.q.: ['10', 'USD', 'to', 'EUR']
                func = Exchange(text)
                if func.check_for_exchange():
                    conv = func.convert()
                    my_answer = f'💸 {text[0]} {text[1].upper()} is {conv} {text[3].upper()}'
                    bot.send_message(msg.chat.id, my_answer)
                else:
                    raise TypeError

            elif message[0] == '/history':
                text = message[1::] # take list without '/history',
                # e.q.: ['USD/EUR', 'for', '7', 'days']

                if len(text[0].split('/')) == 2:
                    text_cur = text[0].split('/') # take 'USD/EUR' and transform in ['USD', 'EUR']
                    func = History(text, text_cur)

                    if func.check_for_history():
                        val = func.history()
                        fig = func.figure(msg, val)
                        my_answer = open(f'{fig}', 'rb')
                        bot.send_photo(msg.chat.id, my_answer)

                    else:
                        raise TypeError

                else:
                    raise TypeError or IndexError

            else:
                raise TypeError

    except TypeError or IndexError:
            my_answer = '😓 Sorry, I don`t understand you. Please, type a correct command.'
            bot.send_message(msg.chat.id, my_answer)


bot.polling(none_stop=True, interval=0)
