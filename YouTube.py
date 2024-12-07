import asyncio
import os
import re
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from AOMusic.utils.database import is_on_off
from AOMusic.utils.formatters import time_to_seconds

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")


cookies_file = "AOMusic/cookies/cookies.txt"

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            duration = result["duration"]
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookies_file,
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp --cookies {cookies_file} -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        try:
            result = playlist.split("\n")
            for key in result:
                if key == "":
                    result.remove(key)
        except:
            result = []
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True, "cookiefile": cookies_file}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except:
                    continue
                if not "dash" in str(format["format"]).lower():
                    try:
                        format["format"]
                        format["filesize"]
                        format["format_id"]
                        format["ext"]
                        format["format_note"]
                    except:
                        continue
                    formats_available.append(
                        {
                            "format": format["format"],
                            "filesize": format["filesize"],
                            "format_id": format["format_id"],
                            "ext": format["ext"],
                            "format_note": format["format_note"],
                            "yturl": link,
                        }
                    )
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile": cookies_file,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile": cookies_file,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_video_dl():
            formats = f"{format_id}+140"
            fpath = f"downloads/{title}"
            ydl_optssx = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
                "cookiefile": cookies_file,  # Add cookie file option here
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_optssx = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "cookiefile": cookies_file, # Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1749011212	VISITOR_INFO1_LIVE	ZVp6yvCfJvM
.youtube.com	TRUE	/	TRUE	1749011212	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgEA%3D%3D
.youtube.com	TRUE	/	TRUE	1768019323	PREF	f6=40000000&tz=Asia.Kolkata&f5=30000&f7=100
.youtube.com	TRUE	/	TRUE	1764995285	__Secure-1PSIDTS	sidts-CjEBQT4rXxVU5lTQxwBOeT2ihdQXCZpXcLBDoFRww7trryM0WJGRn3yQmAvr38XTPSPcEAA
.youtube.com	TRUE	/	TRUE	1764995285	__Secure-3PSIDTS	sidts-CjEBQT4rXxVU5lTQxwBOeT2ihdQXCZpXcLBDoFRww7trryM0WJGRn3yQmAvr38XTPSPcEAA
.youtube.com	TRUE	/	TRUE	1768019291	__Secure-3PAPISID	QBIWDQ3iNbpmn6TK/AyUPlnlinoWJlCWTB
.youtube.com	TRUE	/	TRUE	1768019291	__Secure-3PSID	g.a000rAht_p3175JekVDY2aWDEyUNHvFcZ8wFVTEoFzls6RTEevLBsC8ex8A_GWWCJMbRhNnVQAACgYKAQISARYSFQHGX2Mi1Vp3bKY64nDMRisi_1DdrRoVAUF8yKqHZflqffKrQwCI0vgwnt8H0076
.youtube.com	TRUE	/	TRUE	1764995566	__Secure-3PSIDCC	AKEyXzVoW0e7Az0s686tsi6qkd6HI_g90aFlAKSUZsGh73JIojAMVAY8TfIz-SxdslwFImEb
.youtube.com	TRUE	/	FALSE	1733456913	ST-1mqyjaj	csn=iv6ZvRaYRo7svCfD&itct=CJEBEIf2BBgBIhMIyNaelp6SigMV33CdCR0vWjhTUhRjb3B5cmlnaHQgZnJlZSBtdXNpY5oBBQgyEPQk
.youtube.com	TRUE	/	FALSE	1733458580	ST-17dl11s	csn=hXUzOssqUQnkXSAr&itct=CPUBEPxaGAEiEwjolLuDpJKKAxWpm9gFHQODEIQyB3JlbGF0ZWRIzOHIt7nMj8zIAZoBBQgBEPgd
.youtube.com	TRUE	/	TRUE	1733460432	GPS	1
.youtube.com	TRUE	/	FALSE	1733458645	ST-1afjx4n	csn=bHSRfi0GsFw8n1eo&itct=CAIQ39wCGAciEwjFuZbPpJKKAxV_6KACHZBbDbM%3D
.youtube.com	TRUE	/	FALSE	1768019291	HSID	AgZ_uKqKjXAA2-m50
.youtube.com	TRUE	/	TRUE	1768019291	SSID	AliJbluGRRUAQ_RkH
.youtube.com	TRUE	/	FALSE	1768019291	APISID	MuY2WTRHxO401Vgv/ARVDUGrUnbuRsFlGa
.youtube.com	TRUE	/	TRUE	1768019291	SAPISID	QBIWDQ3iNbpmn6TK/AyUPlnlinoWJlCWTB
.youtube.com	TRUE	/	TRUE	1768019291	__Secure-1PAPISID	QBIWDQ3iNbpmn6TK/AyUPlnlinoWJlCWTB
.youtube.com	TRUE	/	FALSE	1768019291	SID	g.a000rAht_p3175JekVDY2aWDEyUNHvFcZ8wFVTEoFzls6RTEevLBl4HIjkJr5Kk5saD-xdo7KQACgYKATkSARYSFQHGX2MiZX9v5PmQV_yKDpf-gru1ZxoVAUF8yKqRrakg__b9lH_R_GiTNBfk0076
.youtube.com	TRUE	/	TRUE	1768019291	__Secure-1PSID	g.a000rAht_p3175JekVDY2aWDEyUNHvFcZ8wFVTEoFzls6RTEevLBqJWM3CpcbH0Hx5TKOYgPAgACgYKAScSARYSFQHGX2MiiA77p_ryy0pwRfkjKRHmbBoVAUF8yKoUy4-bk-Qj5i6v55M7YTyf0076
.youtube.com	TRUE	/	FALSE	1764995566	SIDCC	AKEyXzX2CS1KnNoGsZrS1DkAsZ0tb985wn5Ko84mTrmETvdxPsc5-8r4YqEZaLa0jBQSjTfJ
.youtube.com	TRUE	/	TRUE	1764995566	__Secure-1PSIDCC	AKEyXzXbwuh4kTzzquzKXfqK4mynrukMBbMgEJ7WbLIPyco3S2pDjZHMq08MtaGqfb0ucGCbOA
.youtube.com	TRUE	/	TRUE	1733459407	YTSESSION-rvkia	ANPz9Kh99WDgKIB+7AMNuacV+aMhX3IEs38TUJkoiEn5BvAuIXoENo1YG/NRuJu36sxAaJoFJ7iOhdnQBMwMRu30L1hZHDxI/l5bd0NtEf1V4THg4OMYVC3c5qWeZKOZ7tkyXLD1hnqpcVj+0ycLdGYqpih76OS3Da+ULpEZU9u0GA==
.youtube.com	TRUE	/	TRUE	0	YSC	kmSr1SNDyqo
.youtube.com	TRUE	/	TRUE	1768019290	LOGIN_INFO	AFmmF2swRAIgCUGJYkAeTsbhk0nD19Vby1r0NVbzfwwBq9P26kWUEfACIEwqdVx2lt1nvKqZhpUJIfSbntgydSv5Lbl3NAMH6bxn:QUQ3MjNmekZqaXM2YVN0WTZvY0h6SHVYWlRjb0xadkRGNkVpbGNLekdITHMtR0xIcExPZmRqV2oyLUhaU2UxZFkzQ3Z1eU5uSnNNalVYaC10SmdTb2NEQnlIOGRWNUV0MWtQa25wNVFWRjZjaE9id09wblJ1elRadTVGT3FqY1dDeURaYjJPeDZCRnpxVkRWU2cyc0pJUGNaQWN1a1pNdlFn
.youtube.com	TRUE	/	TRUE	1733459410	YTSESSION-fnj3yf	ANPz9KjFJAV/Ucli5EEsrNMLbOi+hJttrU36b9MnwON1Vp+s/Adj2hboR8pSWDx/YL8meg0kCKhpwFc700+GGIOqbJ5dCX97gyHiSB0=
.youtube.com	TRUE	/	FALSE	1733459328	ST-11rlstz	csn=T6kGrcDIAmDqu8vO&itct=CJABEPxaGAAiEwjt7uyWp5KKAxWwKbcAHVOQLuwyBnNlYXJjaFILdHUgY2hhaGl5ZSCaAQMQ9CQ%3D # Add cookie file option here
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        if songvideo:
            await loop.run_in_executor(None, song_video_dl)
            fpath = f"downloads/{title}.mp4"
            return fpath
        elif songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            fpath = f"downloads/{title}.mp3"
            return fpath
        elif video:
            if await is_on_off(1):
                direct = True
                downloaded_file = await loop.run_in_executor(None, video_dl)
            else:
                proc = await asyncio.create_subprocess_exec(
                    "yt-dlp",
                    "--cookies", cookies_file,
                    "-g",
                    "-f",
                    "best[height<=?720][width<=?1280]",
                    f"{link}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = None
                else:
                    return
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, direct
