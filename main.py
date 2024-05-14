import telebot
import json
import requests

bot = telebot.TeleBot('7160495612:AAG5s3J7x1OAK6ucrTpe7F2SYFbZiXrjqp8')

class Model:
    def __init__(self, text):
        self.url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
        self.apiKey = 'AQVN2yF2UAYkYY3wd7r0te16FU6rs65rOBw7-m8y'

        self.headers = {
            'Authorization': f'Api-Key {self.apiKey}',
        }
        self.data = json.dumps({
            "modelUri": "gpt://b1gokpjhe19ihtpivard/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": [
        {
                "role": "user", 
                "text": text
        }]})

    def send(self):
        resp = requests.post(self.url, headers=self.headers, data=self.data)
        return resp.json()["result"]["alternatives"][0]["message"]["text"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Телеграм-бот написан для проектной работы, напишите мне любой запрос.", parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        gpt = Model(message.text)
        answer = gpt.send()
        print(f"username: {message.from_user.username}, message: {message.text} \nanswer:\n{answer}\n ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE ENDLINE\n")
        bot.send_message(message.from_user.id, answer)
    except Exception as e:
        bot.send_message(message.from_user.id, f"Произошла ошибка, попробуйте еще раз.")
        print(f"Error: {e}")



bot.polling(none_stop=True, interval=0)
