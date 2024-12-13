from pyrogram import Client, filters
from pyrogram.types import Message

Ad settings
AD_TEXT = "Get exclusive music updates!"
AD_TITLE = "Music Updates"
AD_BUTTON_TEXT = "Join Channel"
AD_URL = "@music_updates"

Ad keyboard
AD_KEYBOARD = {"text": AD_TEXT, "buttons": [[{"text": AD_BUTTON_TEXT, "url": AD_URL}]]}

def send_ad(client, message):
    message.reply_text(AD_TEXT)
