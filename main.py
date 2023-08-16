import telebot

TOKEN = '6313616793:AAG8vuTHMrSREOxSI7rIqhOmCKDwErab1IQ'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'hello world')


@bot.message_handler(func=lambda message: 'image' in message.text.lower())
def send_image(message):
    image_path = './6.jpg'

    with open(image_path, 'rb') as image_file:
        bot.send_photo(message.chat.id, image_file)


@bot.message_handler(commands=['members'])
def get_group_members_count(message):
    chat_id = message.chat.id

    members_count = bot.get_chat_members_count(chat_id)

    bot.reply_to(message, f"تعداد اعضای گروه: {members_count}")


@bot.message_handler(func=lambda message: 'سگ' in message.text.lower() and message.chat.type == 'group')
def delete_dog_message(message):
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['leave_group'])
def leave_group(message):
    chat_id = message.chat.id

    bot.leave_chat(chat_id)


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.count = 0

    def update(self):
        self.count += 1


users = []


@bot.message_handler(func=lambda message: True and message.chat.type == 'group')
def delete_user_messages(message):
    chat_id = message.chat.id

    user_id = message.from_user.id
    permission = True
    for user in users:
        if user.user_id == user_id:
            permission = False
            break

    if permission:
        newUser = User(user_id)
        users.append(newUser)

    limit = False
    for user in users:
        if user.user_id == user_id:
            if user.count >= 3:
                limit = True
                break

    if limit:
        bot.delete_message(chat_id, message.message_id)
    else:
        for user in users:
            if user.user_id == user_id:
                user.update()
                break


@bot.message_handler(content_types=['new_chat_members'])
def print_added_members(message):
    chat_id = message.chat.id

    if message.new_chat_members:
        for member in message.new_chat_members:
            print(f"New member added: {member.id}")

    print(f"Sender ID: {message.from_user.id}")


bot.infinity_polling()
