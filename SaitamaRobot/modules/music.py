import asyncio
from asyncio import sleep
import os
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message
from SaitamaRobot.utils.ut import get_arg
from SaitamaRobot import pbot

@pbot.on_message(filters.command("song"))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("Processing...")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("Song not found.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song")
        LOGGER.error(ex)
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await pbot.send_chat_action(message.chat.id, "upload_audio")
    await pbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
