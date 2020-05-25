import requests
import json



def get_song_name(id):
    url = 'http://music.163.com/api/song/detail/?id={}&ids=%5B{}%5D'.format(id, id)
    r = requests.get(url)
    info = r.json()
    return info['songs'][0]['name']

def get_artisit_name(id):
    url = 'http://music.163.com/api/song/detail/?id={}&ids=%5B{}%5D'.format(id, id)
    r = requests.get(url)
    info = r.json()
    return info['songs'][0]['artists'][0]['name']



