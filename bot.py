﻿import socket
import socks
import requests

socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, '176.221.104.2', port=35215)
socket.socket = socks.socksocket

token = '738099463:AAHjUgagLdzp5R-6eZapoC8GhNA-oh1DM3U' #Telegram @g18_search_bot
key = 'AIzaSyD44YDNQGAdGbqOjZ1CrnKYEUMQ5Wct6ns' #Google
custom_search='013695167246701378175:arrmuifq5-o'

class Google_Search:
    def __init__(self,key,custom_search):
        self.key=key
        self.custom_search=custom_search
        self.search_api_url='https://www.googleapis.com/customsearch/v1?'

    def get_search_results(self, search):
        params = {'key': self.key, 'cx': self.custom_search, 'fields':'items(title,link)', 'q': search}
        response = requests.get(self.search_api_url, params)
        return response.json()

    def generate_result_message(self, search):
        r = self.get_search_results(search)
        i = 0
        message = ''
        while i < 10:
            message += '\n' + str(r['items'][i]['title']) + '\n' + str(r['items'][i]['link']) + '\n'
            i += 1
        return message

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    def get_updates(self, offset=None, timeout=30):
        method = str('getUpdates')
        params = {'timeout': timeout, 'offset': offset}
        url = str(self.api_url) + str(method)
        resp = requests.get(url, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

search_bot=BotHandler(token)
google_search=Google_Search(key,custom_search)

def main():
    new_offset = None


    while True:
        search_bot.get_updates(new_offset)

        last_update = search_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        result_message=google_search.generate_result_message(last_chat_text)
        search_bot.send_message(last_chat_id, 'Результаты поиска по Google: ' + result_message)

        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()







