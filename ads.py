from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

Telegram Ads API settings
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

Pyrogram client
app = Client("my_bot")


Ad settings
AD_TEXT = "Exclusive music updates!"
GROUP_ID = "YOUR_GROUP_ID"

Send ad function
def send_ad(client, message):
    client.send_message(GROUP_ID, AD_TEXT)

Command handler
@app.on_message(filters.command('ad'))
def send_ad_command(client, message):
    send_ad(client, message)

app.run()
