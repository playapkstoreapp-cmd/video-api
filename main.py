from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"status":"API Running - Use /api/info?url=LINK"}

@app.get("/api/info")
def get_info(url: str):
    ydl_opts = {'quiet': True, 'skip_download': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        seen=set()
        for f in sorted(info.get('formats', []), key=lambda x: x.get('height',0) or 0, reverse=True):
            if f.get('ext')=='mp4' and f.get('vcodec')!='none' and f.get('height') and f.get('height') not in seen:
                seen.add(f['height'])
                formats.append({"quality":f"{f['height']}p","url":f['url']})
            if len(formats)>=4:
                break
        if not formats and info.get('url'):
            formats=[{"quality":"HD","url":info['url']}]
        return {"title":info.get('title'),"thumbnail":info.get('thumbnail'),"formats":formats}
