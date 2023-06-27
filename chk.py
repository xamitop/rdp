import requests
import datetime
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
TOKEN = '5879436787:AAGcfvT0RVuXRFk31H6jEE_g03oX1YVeGzk'
# Replace 'YOUR_PRIVATE_GROUP_LINK' with the actual private group invite link
GROUP_LINK = 'https://t.me/+ltX5ot6wa3I4ZWNl'

def start(update: Update, context):
    welcome_message = """
    Welcome to Proxy Checker Bot! 🤖🔎

    Send me a proxy to check if it's live. I will provide you with details about the proxy, including the IP address.

    Just send me a proxy in the format:
    ProxyServer:Port:Username:Password
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def check_proxy(update: Update, context):
    proxy_details = update.message.text.split(':')
    proxy_server = proxy_details[0]
    port = proxy_details[1]
    username = proxy_details[2]
    password = proxy_details[3]

    proxies = {'http': f'http://{username}:{password}@{proxy_server}:{port}',
               'https': f'http://{username}:{password}@{proxy_server}:{port}'}

    response = requests.get('https://api.ipify.org?format=json', proxies=proxies)

    if response.ok:
        ip_address = response.json().get('ip')
        message = f"Proxy is live! 🟢\nIP Address: {ip_address}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        context.bot.send_message(chat_id=GROUP_LINK, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Proxy is not live. 🔴")

def start_checker(update: Update, context):
    context.bot.send_message(chat_id=GROUP_LINK, text="Proxy Checker Bot has started!\nCurrent time: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("Bot started")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    check_proxy_handler = MessageHandler(Filters.text & (~Filters.command), check_proxy)
    dispatcher.add_handler(check_proxy_handler)

    start_checker_handler = CommandHandler('start_checker', start_checker)
    dispatcher.add_handler(start_checker_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Starting the bot...")
    main()
