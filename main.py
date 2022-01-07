#Features

# 1) /add Add Tasking To The Bot
# 2) /clear_list Clear Entire To Do List - (maybe add a confirmation key)
# 3) /reminder remind user at a certain time
# 4) /clear_task clear single task
# (followed by prompt to choose task to clear)
# 5) /view see items in list

import os

from database import user
import telebot
from telebot.types import (
  BotCommand,
  InlineKeyboardButton,
  InlineKeyboardMarkup
)

API_KEY = os.getenv('API_KEY') 
bot = telebot.TeleBot(API_KEY)


# from threading import Thread
# from time import sleep
# import time, datetime 
# print(datetime.date.today().weekday())



bot.set_my_commands([
  BotCommand('start', 'Start The Bot'),
  BotCommand('add', 'Add Tasking To the Bot'),
  BotCommand('clear_list', 'Clear Entire To Do List'),  
  BotCommand('remind', 'Remind User Of A Specific Task At A Certain Time'),
  BotCommand('view', 'View Entire List and Remove Specific Task')
  ])


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Spam
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# @bot.message_handler(commands=['gabby'])
# def gabby(message):
#     bot.send_message(chat_id=message.chat.id, text='OI GABBY HO, FUCK U YIWONG🥵🥵🥵🥵')
#     return


# @bot.message_handler(commands=['rty'])
# def rty(message):
#     bot.send_photo(
#       chat_id = message.chat.id,
#       photo=open('./Images/rty.jpg', 'rb'),
#       caption= 'So cute !'
#     )

# @bot.message_handler(commands=['mia'])
# def mia(message):
#     bot.send_photo(
#       chat_id = message.chat.id,
#       photo=open('./Images/mia.jpg', 'rb'),
#       caption= 'So cute !'
#     )

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Spam
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def request_start(chat_id):
  """
  Helper function to request user to execute command /start
  """
  if chat_id not in user:
    bot.send_message(chat_id=chat_id, text='Please start the bot by sending /start')
  
  return




@bot.message_handler(commands=['start'])
def start(message):
  """
  Command that welcomes the user and configures the required initial setup
  """
  chat_id = message.chat.id
  if message.chat.type == 'private':
    chat_user = message.chat.first_name
  else:
    chat_user = message.chat.title
  user[chat_id] = []
  message_text = f'Hello {chat_user} !'
  bot.reply_to(message, message_text)





@bot.message_handler(commands=['view'])
def view(message):
  """
  Command that lists all outstanding tasks
  """

  chat_id = message.chat.id
  if chat_id not in user: 
    request_start(chat_id)
    return

  if (not user[chat_id]):
    chat_text = 'No outstanding tasks!'
    bot.send_message(
      chat_id=chat_id,
      text = chat_text
    )
  # bot.send_photo(chat_id=chat_id, photo=open('./gabby.jpg', 'rb'))
#     bot.send_photo(
#       chat_id = chat_id,
#       photo=open('./Images/gabby.jpg', 'rb'),
#       caption= 'So good like Gabby !'
#     )

  else:
    chat_text='Outstanding tasks:'

    buttons = []
    for task in user[chat_id]:
      row = []
      button = InlineKeyboardButton(
        task, 
        callback_data='confirm ' + task
      )
      row.append(button)
      buttons.append(row)
    
    bot.send_message(
      chat_id=chat_id, 
      text=chat_text,
      reply_markup=InlineKeyboardMarkup(buttons)
    )





@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  """
  Handles the execution of the respective functions upon receipt of the callback query
  """

  chat_id = call.message.chat.id
  data = call.data
  # intent, data = data.split()[0], data.split()[1:]
  intent, data = data.split()[0], data[data.index(' ') + 1:]
  if intent == 'confirm':
    confirm_task(chat_id, data)
    return

  if intent == 'yes':
    remove_task(chat_id, data)
    view(call.message)
    return

  if intent == 'no':
    view(call.message)
    return

  print(f'{chat_id}: Callback not implemented')






def confirm_task(chat_id, task):
    options = ['yes', 'no']
    buttons = []
    row = []
    for option in options:
      button = InlineKeyboardButton(
        option, 
        callback_data = option + ' ' + task
        )
      row.append(button)
    buttons.append(row)

    chat_text= f'Confirm remove {task} ?'
    
    bot.send_message(
      chat_id=chat_id, 
      text=chat_text,
      reply_markup=InlineKeyboardMarkup(buttons)
    )






def remove_task(chat_id, task):
  user[chat_id].remove(task)
  bot.send_message(chat_id, f'Completed {task}')






@bot.message_handler(commands=['add'])
def add_to_user(message):
  """
  Add a task to the list
  """
  chat_id = message.chat.id
  task = message.text

  if message.text == '/add' or message.text == '/add@Taskshelper_bot':
    bot.send_message(chat_id, 'Please enter task after /add')
    return
  else:
    # task = ' '.join(message.text.split()[1:])    
    task = task[task.index(' ') + 1:]
    if chat_id not in user: 
      request_start(chat_id)
      return

    user[chat_id].append(task)
    bot.send_message(chat_id, f'Added {task}')





@bot.message_handler(commands=['clear_list'])
def clear_list(message):
  """
  Command that removes all items in the tasks
  """

  chat_id = message.chat.id
  if chat_id not in user: 
    request_start(chat_id)
    return

  cart_cleared_text = 'Tasks have been cleared!'
  user[chat_id].clear()

  bot.send_message(chat_id=chat_id, text=cart_cleared_text)


bot.infinity_polling()
