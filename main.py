import telebot
from telebot import types
bot = telebot.TeleBot("8018610523:AAGYsvSWQ84oMmLW7_tTRg9RYEjhogDqNhM")
BUTTONS = ['new task', 'task list']
weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
to_do_list = []
class Task():
    def __init__(self, task_day: str, task_name: str, task_time: str) -> None:
        self.task_day = task_day
        self.task_name = task_name
        self.task_time = task_time
@bot.message_handler("start")
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton(BUTTONS[0])
    itembtn2 = types.KeyboardButton(BUTTONS[1])
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "What do you want to do:", reply_markup=markup)
@bot.message_handler("help")
def help(message):
    bot.send_message(message.chat.id, "/help - info about this bot \n /start - start of the bot \n (button)new_task - make a new task \n (button)task_list - shows your task list")
@bot.message_handler(content_types="text")
def answer(message):
    if message.text == "new task":
        bot.send_message(message.chat.id, "type in a name for your task:")
    elif message.text == "task list":
        print_to_do_list(message)
    else:
        add_task(message)
def print_to_do_list(message):
    text_list = ""
    if len(to_do_list) > 0:
        for i, task in enumerate(to_do_list):
            text_list += f"task {i + 1} - {task.task_name} \n"
    else:
        text_list += "You dont have any tasks yet."
    bot.send_message(message.chat.id, text_list)

def add_task(message):
    task_name = message.text
    task_day = None 
    task_time = None
    new_task = Task(task_day, task_name, task_time)
    to_do_list.append(new_task)
    save_tasks_to_file()
    bot.send_message(message.chat.id, f"Task '{task_name}' added!")
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard_buttons = []
    for i in weekdays:
        day_button = types.InlineKeyboardButton(f"{i}", callback_data=i)
        keyboard_buttons.append(day_button)
    keyboard.add(*keyboard_buttons)
    bot.send_message(message.chat.id, text="pic a day", reply_markup=keyboard)  
def save_tasks_to_file():
    with open("tasks.txt", "w") as tasks:
        for i in to_do_list:
            tasks.write(i.task_name)
            tasks.write("\n")
def load_tasks_from_file():
    with open("tasks.txt") as tasks:
        for i in tasks:
            print(i)
bot.polling(True, interval=0)

# Переписать работу с тасками на файловую систему