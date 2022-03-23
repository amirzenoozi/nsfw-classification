from datetime import datetime
from keras.models import load_model
from dotenv import load_dotenv

import numpy as np
import script.utils
import telebot
import os
import cv2

config = load_dotenv(".localenv")
app = telebot.TeleBot(os.getenv('BOT_TOKEN'))

@app.message_handler(commands=['start'])
def say_hello(messages):
    app.send_message(messages.chat.id, f'Wellcome Dear {messages.from_user.first_name}🌹')
    app.send_message(messages.chat.id, f'Here you can Classify Your Image')
    app.send_message(messages.chat.id, f'Now send me the photo so I can tell you 😉')

@app.message_handler(content_types=['photo'])
def photo(message):
    file_info = app.get_file(message.photo[-1].file_id)
    downloaded_file = app.download_file(file_info.file_path)

    if not os.path.exists("upload"):
            os.mkdir("upload")

    if not os.path.exists("upload/telegram"):
            os.makedirs("upload/telegram")

    base_filename = file_info.file_path.split("/")
    file_parts = base_filename[1].split(".")
    date = str(datetime.timestamp(datetime.now())).replace(".", "-")
    file_name = f'{os.getcwd()}\\upload\\telegram\\{file_parts[0].replace(" ", "-")}_telebot_{date}.{file_parts[1]}'
    script.utils.save_file(file_name, downloaded_file)

    
    print("Now We Are Proccessing...")
    app.send_message(message.chat.id, f'🧑🏻‍💻 Now We Are Proccessing...')
    model = load_model('model/model.h5')

    image = script.utils.load_image(file_name)
    ans = model.predict(image)
    maping = {0 : "Neutral", 1 : "Porn", 2 : "Sexy"}
    new_ans = np.argmax(ans[0])

    app.reply_to(message, f'``` \nImage Class: {maping[new_ans]} \nProbability {round((ans[0][new_ans] * 100), 2)}% \n```', parse_mode='Markdown')
                

if __name__ == '__main__':
    print("We Are Starting The Bot...")
    app.infinity_polling()
