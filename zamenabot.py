from telebot import types
import telebot
from pdf2image import convert_from_path
import requests
import os
import os.path

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Замена")
    btn2 = types.KeyboardButton("Основное расписание")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Что будем смотреть?🧐".format(message.from_user), reply_markup=markup)    

@bot.message_handler(commands=['download'])
def send_file(message):
    file_url = 'http://kit68.ru/raspisanie/zamena.pdf'
    file_name = 'zamena.pdf'
    r = requests.get(file_url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    doc = open(file_name, 'rb')
    #bot.send_document(message.chat.id, doc)  #док = пдф файл
    images = convert_from_path('zamena.pdf')
    for i, image in enumerate(images):
        image.save(f'zamena_{i}.png')
    file_path = "/root/kit68/zamena_1"
    os.path.isfile(file_path)
    try:
        img = open('zamena_0.png', 'rb')
        img1 = open('zamena_1.png', 'rb')
        bot.send_document(message.chat.id, img)
        bot.send_document(message.chat.id, img1)
        os.remove('/root/kit68/zamena_1.png')
        os.remove('/root/kit68/zamena_0.png')
    except FileNotFoundError:
        img = open('zamena_0.png', 'rb')
        bot.send_document(message.chat.id, img)
        os.remove('/root/kit68/zamena_0.png')
    os.remove('/root/kit68/zamena.pdf')

def p22(message):         #p22 = П-2-2
    imgp22 = open('p22.png', 'rb')
    bot.send_document(message.chat.id, imgp22)
            
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Замена"):
        send_file(message)
    elif(message.text == "Основное расписание"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  
        grp = types.KeyboardButton("П-2-2")
        back = types.KeyboardButton("Назад")
        markup.add(grp, back)
        bot.send_message(message.chat.id, text="Выбери группу".format(message.from_user), reply_markup=markup)
    elif(message.text == "П-2-2"):
        p22(message)
        start(message)
    elif(message.text == "Назад"):
        start(message)
    else:
        bot.send_message(message.chat.id, text="ты это, пользуйся кнопками, а то я тупой".format(message.from_user))

bot.polling()