from django.shortcuts import render
from django.http import HttpResponse
from player.env import API_KEY
import requests
import asyncio

import logging
logger = logging.getLogger("mylogger")
logger.info("Whatever to log")

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
    return render(request, 'index.html')

def compare_form(request):
    return HttpResponse("Hello, world. You're at the COMPARE index.")

def compare(request, username, username2):
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
    return render(request, 'compare.html', {"compare_dic":compare_dic, "user1":data_user, "user2":data_user2})


def get_user(request, username: str):
    user_profile = user(username)
    get_user_best_response = requests.get(f'https://osu.ppy.sh/api/get_user_best?k={API_KEY}&u={username}&limit=5')
    gubr_response = get_user_best_response.json()
    if not gubr_response:
        return HttpResponse("User not found")
    get_user_recent_response = requests.get(f'https://osu.ppy.sh/api/get_user_recent?k={API_KEY}&u={username}&limit=5')
    gur_response = get_user_recent_response.json()
    if not gur_response:
        gur_response = []
    return render (request, 'profile.html', {"profile":user_profile[0], "best":gubr_response, "recent":gur_response, "user_id":user_profile[0]["user_id"]})


def user(username: str):
    get_user_response = requests.get(f'https://osu.ppy.sh/api/get_user?k={API_KEY}&u={username}')
    gur_response = get_user_response.json()
    if not gur_response:
        return HttpResponse("User not found")
    return gur_response
