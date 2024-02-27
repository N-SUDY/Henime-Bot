# plugin/video_hentai.py

from pyrogram import *
from pyrogram.types import *
import requests
from pymongo import MongoClient
import os
import subprocess
import json

MONGO_URL = os.environ.get("MONGO_URL", None) 
CACHE_CHANNEL = os.environ.get("CACHE_CHANNEL")

def hentailink(client, callback_query):
    click = callback_query.data
    clickSplit = click.split("_")
    link = clickSplit[1]
    chatid = callback_query.from_user.id
    messageid = callback_query.message.id
    url = f"https://hanime-tv-api-phi.vercel.app/link?id={link}" 
    result = requests.get(url).json()  
    url = result["data"][0]["url"]
    if not url == "":
        url1 = result["data"][0]["url"]
        url2 = result["data"][1]["url"]
        url3 = result["data"][2]["url"]        
        keyb = [
            [InlineKeyboardButton("360p", url=f"{url3}")],
            [InlineKeyboardButton("480p", url=f"{url2}")],
            [InlineKeyboardButton("720p", url=f"{url1}")],
            [InlineKeyboardButton("Back", callback_data=f"info_{link}")]
        ]
        repl = InlineKeyboardMarkup(keyb)
        callback_query.message.reply_text(text=f"""You are now watching **Episode https://hanime.tv/videos/hentai/{link}** :-\nPlease share the bot if you like it ☺️.""", reply_markup=repl)
        
    if url == "":
        url1 = result["data"][1]["url"]
        url2 = result["data"][2]["url"]
        url3 = result["data"][3]["url"]
        keyb = [
            [InlineKeyboardButton("360p", url=f"{url3}")],
            [InlineKeyboardButton("480p", url=f"{url2}")],
            [InlineKeyboardButton("720p", url=f"{url1}")],
            [InlineKeyboardButton("Back", callback_data=f"info_{link}")]
        ]
        repl = InlineKeyboardMarkup(keyb)
        callback_query.message.reply_text(text=f"""You are now watching **Episode https://hanime.tv/videos/hentai/{link}** :-\nPlease share the bot if you like it ☺️.""", reply_markup=repl)
        
def hentaidl(client, callback_query):
    click = callback_query.data
    clickSplit = click.split("_")
    link = clickSplit[1]
    hentaidb = MongoClient(MONGO_URL)
    hentai = hentaidb["MangaDb"]["Name"]
    chatid = callback_query.from_user.id
    messageid = callback_query.message.id
    url = f"https://hanime-tv-api-phi.vercel.app/link?id={link}" 
    result = requests.get(url).json()  
    url = result["data"][0]["url"]
    callback_query.edit_message_text(text="Wait till we fetch hentai for you...\nStatus: **DOWNLOADING**")
    is_hentai = hentai.find_one({"name": link})
    if not is_hentai:
        if url:
            file_url = result["data"][2]["url"]
            file_path = f"{link}.mp4"
            subprocess.run(["ffmpeg", "-i", file_url, "-acodec", "copy", "-vcodec", "copy", file_path])
            callback_query.edit_message_text(text="Uploading Now")
            document = client.send_document(chat_id=chatid, document=file_path, caption="Download By @hanime_dl_bot")
            file_id = document.document.file_id
            client.send_document(chat_id=CACHE_CHANNEL, document=file_id, caption="Download By @hanime_dl_bot")
            hentai.insert_one({"name": link, "file_id": file_id})
            os.remove(file_path)
    else:
        file_id = is_hentai["file_id"]
        callback_query.edit_message_text(text="Uploading Now")
        client.send_document(chat_id=chatid, document=file_id, caption="Download By @hanime_dl_bot")
