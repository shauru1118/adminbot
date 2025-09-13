from math import e
import time
from telebot import TeleBot
from telebot.types import Message
from dotenv import load_dotenv
import os
from loguru import logger

from pprint import pprint

load_dotenv()

TOKEN = str(os.getenv("BOT_TOKEN"))

bot = TeleBot(token=TOKEN)
logger.success(f"New bot: {bot.get_me().to_dict()}")

def log_all(messages: list[Message]):
    for message in messages:
        try:
            if message.chat.id < 0 and message.content_type != "bot_command":
                continue 
            logger.info(f"{message.from_user.first_name}_{message.from_user.last_name} ({message.from_user.username}): {message.text}")
        except Exception as e:
            logger.error(f"Error with message: {message} \n{e}")
bot.set_update_listener(log_all)


@bot.message_handler(commands=['start'])
def start(message: Message):
    logger.info(f"New user: {message.from_user.username}")
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}! \nAdd me to your group and start using the bot!')

@bot.message_handler(commands=['mute'])
def mute(message: Message):
    msg = message.reply_to_message
    pprint(message.__dict__["reply_to_message"], indent=2)
    logger.info(f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) muted!")
    bot.restrict_chat_member(message.chat.id, msg.from_user.id, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, until_date=int(time.time() + 600))
    bot.send_message(message.chat.id, f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) muted!")

@bot.message_handler(commands=['unmute'])
def unmute(message: Message):
    msg = message.reply_to_message
    logger.info(f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) UNmuted!")
    bot.restrict_chat_member(message.chat.id, msg.from_user.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
    bot.send_message(message.chat.id, f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) UNmuted!")

@bot.message_handler(commands=['kick'])
def kick(message: Message):
    msg = message.reply_to_message
    logger.info(f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) kicked!")
    bot.kick_chat_member(message.chat.id, msg.from_user.id)
    bot.send_message(message.chat.id, f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) kicked!")

@bot.message_handler(commands=['ban'])
def ban(message: Message):
    msg = message.reply_to_message
    logger.info(f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) banned!")
    bot.ban_chat_member(message.chat.id, msg.from_user.id)
    bot.send_message(message.chat.id, f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) banned!")

@bot.message_handler(commands=['unban'])
def unban(message: Message):
    msg = message.reply_to_message
    logger.info(f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) UNbanned!")
    bot.unban_chat_member(message.chat.id, msg.from_user.id)
    bot.send_message(message.chat.id, f"User {msg.from_user.first_name}_{msg.from_user.last_name} (@{msg.from_user.username}) UNbanned!")


if __name__ == '__main__':
    bot.remove_webhook()
    logger.success("Bot started")
    bot.polling(none_stop=True)
    logger.warning("Bot stopped")


