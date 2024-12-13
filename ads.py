from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

Telegram Ads API settings
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

Pyrogram client
app = Client("my_bot")

Ads function
def send_ad(client, message):
    # Ad settings
    ad_text = "Get exclusive music updates!"
    ad_title = "Music Updates"
    ad_button_text = "Join Channel"
    ad_url = "@music_updates"

    # Ad keyboard
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(ad_button_text, url=ad_url)]])

    # Send ad
    message.reply_text(ad_text, reply_markup=keyboard)

Command handler
@app.on_message(filters.command('ad'))
def send_ad_command(client, message):
    send_ad(client, message)

Bot start
app.run()
