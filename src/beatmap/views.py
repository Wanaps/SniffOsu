from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

import requests

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
        print(f"{beatmapid} -> {r1.status_code} {r2.status_code}")
        if r1.status_code != 200 or r2.status_code != 200:
            return HttpResponse("Erreur lors de la requête à l'API osu!")
        beatmap = r1.json()
        scores = r2.json()
        return render(request, 'get_best.html', {'beatmap': beatmap[0], 'scores': scores})
    return render(request, 'get_best.html', {'beatmapid': beatmapid})

def get_best_from_form(request):
    if request.method == "POST":
        player = request.POST.get('playerid')
        return redirect('get_best_from', player=player)
    else:
        return render(request, 'get_best_from.html')
    
def get_best_from(request, player):
    requestsnb = 0
    if player is not None:
        if player.isdigit():
            scores = requests.get(f"https://osu.ppy.sh/api/get_user_best?k={APIKEY}&u={player}")
            profile = requests.get(f"https://osu.ppy.sh/api/get_user?k={APIKEY}&u={player}")
            requestsnb += 2
        else:
            scores = requests.get(f"https://osu.ppy.sh/api/get_user_best?k={APIKEY}&u={player}")
            profile = requests.get(f"https://osu.ppy.sh/api/get_user?k={APIKEY}&type=string&u={player}")
            requestsnb += 2
        if scores.status_code != 200 or profile.status_code != 200:
            return HttpResponse("Erreur lors de la requête à l'API osu!")
        scores = scores.json()
        profile = profile.json()
        for score in scores:
            r = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={APIKEY}&b={score['beatmap_id']}")
            requestsnb += 1
            if r.status_code != 200:
                return HttpResponse("Erreur lors de la requête à l'API osu!")
            score['beatmap'] = r.json()[0]
        print(f"{player} -> {requestsnb} requests")
        return render(request, 'get_best_from.html', {'scores': scores, 'profile': profile[0]})
    return render(request, 'get_best_from.html', {'player': player[0]})

def compare_score(request, beatmapid, player1, player2):
    if beatmapid is None:
        beatmapid = 000000
    if player1 is None:
        player1 = "player1"
    if player2 is None:
        player2 = "player2"
    return HttpResponse(f"Compare the score between {player1} and {player2} on the beatmap {beatmapid}.")