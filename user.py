from env import API_KEY
import requests


class User:
    def __init__(self, username: str):
        self.username = username

    def get_user(self):
        response = requests.get(f'https://osu.ppy.sh/api/get_user?k={API_KEY}&u={self.username}')
        data = response.json()
        if not data:
            return None
        return data

    def get_user_id(self):
        user = self.get_user()
        if not user:
            return None
        return user[0]['user_id']

    def get_user_best(self, limit: int = 3):
        response = requests.get(f'https://osu.ppy.sh/api/get_user_best?k={API_KEY}&u={self.username}&limit={limit}')
        data = response.json()
        if not data:
            return None
        return data

    def get_user_recent(self, limit: int = 3):
        response = requests.get(f'https://osu.ppy.sh/api/get_user_recent?k={API_KEY}&u={self.username}&limit={limit}')
        data = response.json()
        if not data:
            return None
        return data


if __name__ == '__main__':
    guervus = User('guervus')
    print(guervus.get_user())
    print(guervus.get_user_id())
    print(guervus.get_user_best())
    print(guervus.get_user_recent())

