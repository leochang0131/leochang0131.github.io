import spotipy
import sys
import os
from spotipy.oauth2 import SpotifyClientCredentials


os.environ['SPOTIPY_CLIENT_ID'] = 'd6e2c6e36da54aaca82a73dc73c3b87b'
os.environ['SPOTIPY_CLIENT_SECRET'] = '6d8f9a06bbd74f00bfd31850db689256'



def get_info(name, artist, id):
    try:
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(), requests_timeout=10)
        #spotify = spotipy.Spotify(requests_timeout=10)

        all_info = {"code": 1, "id": id, "song": name, 
                    "url": 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(id)}
        # using 'search' of spotify api, default choose the first result
        # for getting the track's {"Spotify_id", "album_name", "album_pics", "artsit_name"}
        info = spotify.search(name + ' ' + artist, limit=1, type='track')

        item_info = info['tracks']['items'][0]    
        album = item_info['album']

        if len(item_info) > 0:
            s_id = item_info['id']
    except Exception:
        return 'cannot find the song in spotify'
    
    try:
        information = {'artist': item_info['artists'][0]['name'],
                        'album':{'al_name': album['name'], 'picUrl': album['images'][0]['url']}}

        all_info.update(information)
        # using 'audio_features' of spotify api, for getting the audio features
        features = spotify.audio_features(s_id)

        item_features = features[0]
        feat = {'featuress':{
                'tempo': item_features['tempo'], 
                'energy': item_features['energy'],
                'danceability': item_features['danceability'],
                'acousticness' : item_features['acousticness'],
                'liveness': item_features['liveness'],
                'valence' : item_features['valence'],
                'duration_s' : item_features['duration_ms'] / 1000}}
        all_info.update(feat)

        #using 'audio_analysis' of spotify api,for getting the sections info
        analysis = spotify.audio_analysis(s_id)
    
        #anal = {'sections': analysis['sections']}
    
        #find cliamx
        anal = find_climax(analysis['sections'])   
        anal = {'sections': anal}

        all_info.update(anal)
        return all_info

    except Exception:
        return 'runtime error'


def find_climax(list):
    list[0].update({'climax': 0})
    list[len(list)-1].update({'climax': 0})

    for i in range(1, len(list)-1):
        crt_l = list[i]['loudness']
        pre_l = list[i-1]['loudness']
        nxt_l = list[i+1]['loudness']

        if(crt_l > pre_l and crt_l > nxt_l):
            list[i].update({'climax': 1})
        else:
            list[i].update({'climax': 0})
    
    return list