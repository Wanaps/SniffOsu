from django.shortcuts import render
from django.http import HttpResponse

import requests
from .env import APIKEY, SINCEDATE


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
    print(f"Made 1 request")
    return render(request, 'index.html', {'beatmaps': beatmaplist})

