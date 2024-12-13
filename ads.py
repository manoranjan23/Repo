from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

Telegram Ads API settings
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

Pyrogram client
app = Client("my_bot")


AD_TEXT = "Exclusive music updates!"
GROUP_ID = "YOUR_GROUP_ID"

def send_ad(client, message):
    client.send_message(GROUP_ID, AD_TEXT)

@app.on_message(filters.command('start'))
def start_command(client, message):
    message.reply_text("Welcome!")

@app.on_message(filters.command('help'))
def help_command(client, message):
    message.reply_text("Help!")

@app.on_message(filters.command('ad'))
def send_ad_command(client, message):
    send_ad(client, message)

app.run()
