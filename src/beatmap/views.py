from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

import requests
APIKEY = "fed188581e43c97fb53a83986b0befbfb84236dd"

def index(request):
    return HttpResponse("Beatmap index.")

def get_best_form(request):
    if request.method == 'POST':
        beatmapid = request.POST.get('beatmapid')
        return redirect('get_best', beatmapid=beatmapid)
    else:
        return render(request, 'get_best.html')

def get_best(request, beatmapid):
    if beatmapid is not None:
        r1 = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={APIKEY}&b={beatmapid}")
        r2 = requests.get(f"https://osu.ppy.sh/api/get_scores?k={APIKEY}&b={beatmapid}")
        beatmap = r1.json()
        scores = r2.json()
        return render(request, 'get_best.html', {'beatmap': beatmap[0], 'scores': scores})
    return render(request, 'get_best.html', {'beatmapid': beatmapid})

def get_best_from(request, player):
    return HttpResponse("Get best scores from %s" % player)

def compare_score(request, beatmapid, player1, player2):
    if beatmapid is None:
        beatmapid = 000000
    if player1 is None:
        player1 = "player1"
    if player2 is None:
        player2 = "player2"
    return HttpResponse(f"Compare the score between {player1} and {player2} on the beatmap {beatmapid}.")