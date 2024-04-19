from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

import requests
from .env import APIKEY, SINCEDATE

def index(request):
    beatmaps = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={APIKEY}&since={SINCEDATE}")
    beatmaps = beatmaps.json()
    beatmaps.reverse()
    beatmapsets = {}
    beatmaplist = []
    for beatmap in beatmaps:
        beatmapset_id = beatmap['beatmapset_id']
        if beatmapset_id not in beatmapsets and len(beatmaplist) < 15:
            beatmapsets[beatmapset_id] = True
            beatmaplist.append(beatmap)
    print(f"Made 1 request")
    return render(request, 'beatmap/index.html', {'beatmaps': beatmaplist})

def get_best_form(request):
    if request.method == 'POST':
        beatmapid = request.POST.get('beatmapid')
        return redirect('get_best', beatmapid=beatmapid)
    else:
        return render(request, 'beatmap/get_best.html')

def get_best(request, beatmapid):
    if beatmapid is not None:
        r1 = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={APIKEY}&b={beatmapid}")
        r2 = requests.get(f"https://osu.ppy.sh/api/get_scores?k={APIKEY}&b={beatmapid}")
        print(f"{beatmapid} -> {r1.status_code} {r2.status_code}")
        if r1.status_code != 200 or r2.status_code != 200:
            return HttpResponse("Erreur lors de la requête à l'API osu!")
        beatmap = r1.json()
        scores = r2.json()
        return render(request, 'beatmap/get_best.html', {'beatmap': beatmap[0], 'scores': scores})
    return render(request, 'beatmap/get_best.html', {'beatmapid': beatmapid})

def get_best_from_form(request):
    if request.method == "POST":
        player = request.POST.get('playerid')
        return redirect('beatmap/get_best_from', player=player)
    else:
        return render(request, 'beatmap/get_best_from.html')
    
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
        return render(request, 'beatmap/get_best_from.html', {'scores': scores, 'profile': profile[0]})
    return render(request, 'beatmap/get_best_from.html', {'player': player[0]})

def compare_score_form(request):
    if request.method == 'POST':
        beatmapid = request.POST.get('beatmapid')
        player1 = request.POST.get('player1')
        player2 = request.POST.get('player2')
        return redirect('beatmap/compare_score', beatmapid=beatmapid, player1=player1, player2=player2)
    else:
        return render(request, 'beatmap/compare_score.html')

def compare_score(request, beatmapid, player1, player2):
    print("DEBUG")
    print(beatmapid)
    print(player1)
    print(player2)
    print("END DEBUG")
    beatmap = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={APIKEY}&b={beatmapid}")
    score_p1 = requests.get(f"https://osu.ppy.sh/api/get_scores?k={APIKEY}&b={beatmapid}&u={player1}")
    score_p2 = requests.get(f"https://osu.ppy.sh/api/get_scores?k={APIKEY}&b={beatmapid}&u={player2}")
    if beatmap.status_code != 200 or score_p1.status_code != 200 or score_p2.status_code != 200:
        print(f"{beatmapid} -> {beatmap.status_code} {score_p1.status_code} {score_p2.status_code}")
        return HttpResponse("Erreur lors de la requête à l'API osu!")
    print("Made 3 requests")
    print(score_p1.json())
    return render(request, 'beatmap/compare_score.html', {'beatmap': beatmap.json()[0], 'score_p1': score_p1.json(), 'score_p2': score_p2.json()})
