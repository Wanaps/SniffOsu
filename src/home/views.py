from os import getenv
from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()
APIKEY = getenv("APIKEY")
SINCEDATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def home(request):
    beatmaps = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={APIKEY}&since={SINCEDATE}")
    beatmaps = beatmaps.json()
    beatmaps.reverse()
    beatmapsets = {}
    beatmaplist = []
    for beatmap in beatmaps:
        beatmapset_id = beatmap['beatmapset_id']
        if beatmapset_id not in beatmapsets and len(beatmaplist) < 12:
            beatmapsets[beatmapset_id] = True
            beatmaplist.append(beatmap)
    return render(request, 'index.html', {'beatmaps': beatmaplist})

