# testbot
Bot takes data from external API - https://api.exchangeratesapi.io.
Bot has 3 functionalities (commands):
1) /list - take the all aviable currencies which Bot can use with base currency (base currency - USD);
2) /convert [some_currency] to [another_currency] - converting custom currencies. While user don't use another command, Bot will convert by custom currencies. For it just need send number in message;
3) /history [some_currency]/[another_currency] for [some_number] days - return image graph of historical rates from custom number (some_number) to current day. [some_number] must be an integer number and less than 30.
