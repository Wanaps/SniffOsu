from env import API_KEY
import requests


def get_user(username: str):
    response = requests.get(f'https://osu.ppy.sh/api/get_user?k={API_KEY}&u={username}')
    data = response.json()
    if not data:
        return None
    return data


def get_user_id(username: str):
    user = get_user(username)
    if not user:
        return None
    return user[0]['user_id']


def get_user_best(username: str, limit: int = 3):
    response = requests.get(f'https://osu.ppy.sh/api/get_user_best?k={API_KEY}&u={username}&limit={limit}')
    data = response.json()
    if not data:
        return None
    return data


def get_user_recent(username, limit: int = 3):
    response = requests.get(f'https://osu.ppy.sh/api/get_user_recent?k={API_KEY}&u={username}&limit={limit}')
    data = response.json()
    if not data:
        return None
    return data



print(get_user('lifeline'))
