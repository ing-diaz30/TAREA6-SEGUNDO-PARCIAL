import time
import telebot
from telebot import types

TOKEN = '1938052810:AAGU1ulVWO8yooxeGvWqz20UB-bg59YVCqo'

knownUsers = [] 
userStep = {}  

commands = { 
    'start'         : 'Iniciar el bot\n\n',
    'help'          : 'Muestra los comandos disponibles\n\n',
    'reclutar'    : 'Inicar proceso de reclutamiento\n\n',
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  
imageSelect.add('Aplicacion Empleo', 'Ubicacion Reclutamiento')

hideBoard = types.ReplyKeyboardRemove()  

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("Nuevo usuarios detectado, pero no ha usado \"/start\" ")
        return 0

def listener(messages):
    for m in messages:
        if m.content_type == 'text':0
    print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)     

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers: 
        knownUsers.append(cid)  
        userStep[cid] = 0 
        
        bot.send_message(cid, 'Bienvenido a tu bot de reclutamiento')
        bot.send_chat_action(cid, 'typing')  
        time.sleep(1)
        bot.send_chat_action(cid, 'typing')  
        time.sleep(1)
        command_help(m) 
    else:
        bot.send_message(cid, "Ya usaste el comando /start, usa el comando /help para visualizar más comandos")

@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Selecciona la opcion de tu interes:\n\n\n"
    for key in commands: 
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  

@bot.message_handler(commands=['reclutar'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Selecciona la tecla de tu preferencia ", reply_markup=imageSelect)  
    userStep[cid] = 1 

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)

    if text == 'Aplicacion Empleo':
        bot.send_message(cid, "Has seleccionado Aplicacion Empleo")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "A continuacíon se te enviara un documento de aplicacion de empleo")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_chat_action(cid, 'upload_document')
        time.sleep(3)   
        bot.send_document(cid, open('aplicacion de empleo.pdf', 'rb'),
                       reply_markup=hideBoard)  
        time.sleep(3)
        bot.send_message(cid, "Selecciona el comando /reclutar para realizar otra consulta o /help para otros comandos")
        userStep[cid] = 0 

    elif text == 'Ubicacion Reclutamiento':
        bot.send_message(cid, "Has seleccionado Ubicacion Viral")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "A continuacíon se te enviara un video del Video Viral")
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_chat_action(cid, 'find_location')
        time.sleep(3)   
        bot.send_location(cid, latitude=15.505423962942492,longitude=-88.02634056301166,
                       reply_markup=hideBoard)  
        time.sleep(3)
        bot.send_message(cid, "Selecciona el comando /reclutar para realizar otra consulta o /help para otros comandos")
        userStep[cid] = 0    
    else:
        bot.send_message(m.chat.id, "No entiendo el texto:\"" + m.text + "\"\nIntenta usar /help para visualizar la lista de comandos disponibles")
        bot.send_message(cid, "Vamos, intentalo de nuevo. ")

bot.polling()