"""
hellow this bot worked on "ChatGpt4free" - chatGpt4o-mini

some chat command writed on rus but u dont need to use it,u can replace it fore somthing other


"Лисыл" - for bot send all msg what he parsed to you as PrivateMessage - it can be True or False
"Ликарт <promt>" - generating img with brain fusionbrain api 
"Лиса/лиса/Лисабля/лисабля <promt>" - ask chatGpt it remember context for 100 symbols if it >100 it remember only last msg
"Лиранд <min value> <max value>" - random numder in diaposon
"Лихелп" - help info print to chat


im cocked bruh i write this for 3 hours 


"""
import telebot  
from g4f.client import Client
from telebot import types  
import time
import datetime
from datetime import date
from telebot.types import ReactionType
import random
from test_generation_img import Text2ImageAPI
import base64
import os
import sys
import speedtest
global lisyl
lisyl=False
all_requests=[]
token = "" # your telegamm bot token 
bot=telebot.TeleBot(token)
allcontext_by_id={}  
message_ids={}
role_to_q = "" #bot role
hellowmsg = "when bot get command /start"
def reboot():
    print("reboot")
    python = sys.executable 
    os.execl(python, python, * sys.argv) 

def test_internet_speed():
    st = speedtest.Speedtest()   
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000  
    ping = st.results.ping
    ans = str(download_speed) + " " +str(upload_speed) + " " + str(ping)
    return ans 

def UnixTime(add_h):
    now=datetime.datetime.now()
    hours_to_add=add_h  
    future_time=now+datetime.timedelta(hours=hours_to_add)
    unix_time=int(time.mktime(future_time.timetuple()))
    return unix_time
def handle_reply(message):
            original_message=message.reply_to_message
            if original_message.id in message_ids:
                original_chat_message = message_ids[original_message.id]
                bot.send_message(original_chat_message.chat.id, message.text)
def get_img(prom,message): #image generation
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'api_key', 'secret_api_key') #for get your own api key u need to login on  https://api-key.fusionbrain.ai/ its free
    model_id = api.get_model()
    uuid = api.generate(prom, model_id)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    with open("image.jpg", "wb") as file:
        file.write(image_data)
    with open("image.jpg", 'rb') as photo:
        bot.send_photo(message.chat.id, photo,reply_to_message_id=message.id)
def get_ansver(context,message1):
        if message1.from_user.id!=7684175263:
            client=Client()  
            try: 
                cur_user_cont=allcontext_by_id[str(message1.from_user.id )]
            except:
                allcontext_by_id[str(message1.from_user.id )]=" "
                cur_user_cont = allcontext_by_id[str(message1.from_user.id )] 
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content":role_to_q+ " " +cur_user_cont  + "curent question:"+ context}])
            all_requests.append(message1.text)
            if response.choices[0].message.content=="Misuse detected. Please get in touch, we can come up with a solution for your use case." :
                get_ansver(context,message1)
            else:
                bot.reply_to(message1,response.choices[0].message.content)   
                if len(allcontext_by_id[str(message1.from_user.id )])>100:
                    allcontext_by_id[str(message1.from_user.id )]=""
                allcontext_by_id[str(message1.from_user.id )]="my question: "+ message1.text + "your ansver: "+  response.choices[0].message.content
            message1.text=""
def Custom_ansver(message_rep_to,text):
    bot.reply_to(message_rep_to,text)
@bot.message_handler(commands=['start'])  
def send_welcome(message):  
    bot.send_message(message.chat.id,hellowmsg)  
@bot.message_handler()
def requestby(message):
    global lisyl
    if message.text == "rebootли" and message.from_user.id == 1157727122:
        reboot() 
        
    if message.chat.id != 1157727122 and lisyl==True:
        sent_message=bot.send_message(1157727122,message.from_user.first_name + " : " + message.text + "                " + message.chat.title )        
        message_ids[sent_message.id] = message   
    args=message.text.split()
   
    if args[0] == "Лисыл" and message.from_user.id == 1157727122:
        lisyl = not lisyl
        bot.reply_to(message,str(lisyl))
    if args[0]=="Ликарт":
        if len(args)>1:
            get_img(message.text.replace("Ликарт", ''),message)
            os.remove("image.jpg")
        else:
            bot.reply_to(message,"чтобы использовать команду Ликарт напиши то что нужно отобразить на картинке через пробел")
    if args[0]=="лисабля": 
        msg_text = message.text.replace("лисабля","привет")
        get_ansver(msg_text,message)      
    if  args[0]=="лиса":
        msg_text = message.text.replace("лиса","привет")
        get_ansver(msg_text,message)
    if  args[0]=="Лисабля":
        msg_text = message.text.replace("Лисабля","привет")
        get_ansver(msg_text,message)
    if  args[0]=="Лиса":
        msg_text = message.text.replace("Лиса","привет")
        get_ansver(msg_text,message)
    if args[0] == "Листат":
        bot.reply_to(message, test_internet_speed() ) 
   
    if args[0]=="Лиранд":
        if len(args)>2:
            bot.reply_to(message,"вероятность равнна: "+str(random.randint(int(args[1]),int(args[2]))))
        else:
            bot.reply_to(message,"ну ты ебанько диапозон задай")
    if args[0]=="Лихелп":
        bot.reply_to(message,"ну чо те не понятно то ? Лиса <вопрос> - обращение к чатхпт,ответ на мое сообющение любое - обращение к чатхпт, а большего тебе и не надо ")
    
bot.infinity_polling()