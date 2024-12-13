import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from AnonXMusic.utils import seconds_to_min, time_to_seconds
from config import AD_CONTENT, BANNED_USERS

@app.on_message(
    filters.command(
        ["play", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"]
    )
    & filters.group
    & ~BANNED_USERS
)
async def play_commnd_with_ads(client, message: Message, _, chat_id, video, channel, playmode, url, fplay):
    mystic = await message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )

    # Simulate Ad Show - Before Playing Music
    await show_advertisement(client, message, mystic)

    # Continue with the usual play command logic as before...
    # (Include the rest of your code for music playback here)
    
    return await mystic.delete()

async def show_advertisement(client, message: Message, mystic: Message):
    """Function to display ads to users."""
    
    # Randomly select an ad from the list
    ad = random.choice(AD_CONTENT)
    
    # Check if the ad is text or image/video
    if ad["type"] == "text":
        ad_message = ad["content"]
        await mystic.edit_text(f"**Ad:** {ad_message}")
    elif ad["type"] == "image":
        ad_image = ad["content"]
        ad_caption = ad.get("caption", "Enjoy this ad!")
        await mystic.edit_text(
            f"**Ad:** {ad_caption}",
            reply_markup=InlineKeyboardMarkup([[
                ("Click here for more", ad_image)  # Example button that leads somewhere
            ]]),
        )
        await mystic.reply_photo(ad_image, caption=ad_caption)

# Example ad content in `config.py`:

AD_CONTENT = [
    {"type": "text", "content": "Check out the latest music gear at www.musicshop.com!"},
    {"type": "image", "content": "https://example.com/ad_image.jpg", "caption": "Amazing headphones at 20% off!"}
]

# Optionally, you can add a command to show ads directly:
@app.on_message(filters.command("ads"))
async def show_direct_ad(client, message: Message):
    """Display an ad when requested directly by the user."""
    mystic = await message.reply_text("Here comes an ad!")
    await show_advertisement(client, message, mystic)
