import os
from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import requests

load_dotenv()

APIKEY = os.getenv("APIKEY")


compare_dic = {
    "count300": 0,
    "better_count300": "",
    "count100": 0,
    "better_count100": "",
    "count50": 0,
    "better_count50": "",
    "playcount": 0,
    "better_playcount": "",
    "ranked_score": 0,
    "better_ranked_score": "",
    "total_score": 0,
    "better_total_score": "",
    "pp_rank": 0,
    "better_pp_rank": "",
    "level": 0.0,
    "better_level": "",
    "pp_raw": 0.0,
    "better_pp_raw": "",
    "accuracy": 0.0,
    "better_accuracy": "",
    "count_rank_ss": 0,
    "better_count_rank_ss": "",
    "count_rank_s": 0,
    "better_count_rank_s": "",
    "count_rank_a": 0,
    "better_count_rank_a": "",
    "pp_country_rank": 0,
    "better_pp_country_rank": ""
    }   

def index(request):
    return render(request, 'player/index.html')

def compare_form(request):
    if (request.method == 'POST'):
        username = request.POST['player1']
        username2 = request.POST['player2']
        compare_dic, user1, user2 = compare(username, username2)
        return render(request, 'player/compare.html', {"username":username, "username2":username2, "compare_dic":compare_dic, "user1":user1, "user2":user2})
    return render(request, 'player/compare.html')

def compare(username, username2):
    data_user = user(username)[0]
    data_user2 = user(username2)[0]
    keys_int = ['count300', 'count100', 'count50', 'playcount', 'ranked_score', 'total_score', 'pp_rank',
            'count_rank_ss', 'count_rank_s', 'count_rank_a', 'pp_country_rank']
    rank_keys = ['pp_rank', 'pp_country_rank']
    keys_float = ['level', 'pp_raw', 'accuracy']
    for key in keys_int:
        data_user[key] = int(data_user[key])
        data_user2[key] = int(data_user2[key])
        if data_user[key] > data_user2[key]:
            compare_dic[key] = data_user[key] - data_user2[key]
            compare_dic['better_' + key] = data_user['username']
        else:
            compare_dic[key] = data_user2[key] - data_user[key]
            compare_dic['better_' + key] = data_user2['username']
    for key in rank_keys:
        data_user[key] = int(data_user[key])
        data_user2[key] = int(data_user2[key])
        if data_user[key] < data_user2[key]:
            compare_dic[key] = data_user[key]
            compare_dic['better_' + key] = data_user['username']
        else:
            compare_dic[key] = data_user2[key]
            compare_dic['better_' + key] = data_user2['username']
    for key in keys_float:
        data_user[key] = float(data_user[key])
        data_user2[key] = float(data_user2[key])
        if data_user[key] > data_user2[key]:
            compare_dic[key] = round(data_user[key] - data_user2[key], 2)
            compare_dic['better_' + key] = data_user['username']
        else:
            compare_dic[key] = round(data_user2[key] - data_user[key], 2)
            compare_dic['better_' + key] = data_user2['username']
    return compare_dic, data_user, data_user2


def profile_form(request):
    if (request.method == 'POST'):
        player = request.POST['player1']
        user_profile, user_best, user_recent, user_id = get_user(player)
        return render(request, 'player/profile.html', {"user_profile":user_profile, "user_best":user_best, "user_recent":user_recent, "user_id":user_id, "player":player})
    return render(request, 'player/profile.html')


def get_user(username: str):
    user_profile = user(username)
    get_user_best_response = requests.get(f'https://osu.ppy.sh/api/get_user_best?k={APIKEY}&u={username}&limit=5')
    gubr_response = get_user_best_response.json()
    if not gubr_response:
        return HttpResponse("User not found")
    get_user_recent_response = requests.get(f'https://osu.ppy.sh/api/get_user_recent?k={APIKEY}&u={username}&limit=5')
    gur_response = get_user_recent_response.json()
    if not gur_response:
        gur_response = []
    return user_profile[0], gubr_response, gur_response, user_profile[0]["user_id"]


def user(username: str):
    get_user_response = requests.get(f'https://osu.ppy.sh/api/get_user?k={APIKEY}&u={username}')
    gur_response = get_user_response.json()
    if not gur_response:
        return HttpResponse("User not found")
    return gur_response
