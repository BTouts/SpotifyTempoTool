import random
import time

import spotipy
import spotifysearch
from spotipy.oauth2 import SpotifyOAuth
import cred
from spotifysearch.client import Client


scope = " user-read-playback-state user-read-recently-played user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                               redirect_uri=cred.redirect_url, scope=scope))
auth2 = spotipy.SpotifyOAuth(cred.client_id, cred.client_secret, cred.redirect_url)

token_dict = auth2.get_cached_token()
token = token_dict['access_token']
token= 0
token_dict2 = auth2.get_cached_token()
token2 = token_dict['access_token']

spotifyObject = spotipy.Spotify(auth=token2)
user_name = spotifyObject.current_user()

myclient = Client(cred.client_id, cred.client_secret)


def driver():
    input("To begin, open spotify and shuffle the playlist you would like to play songs from, then hit ENTER")

    bpm = input("Enter the BPM you want to play: ")

    songs = input("Enter the number of songs you would like to practice with")
    id = (sp.currently_playing()['context']['uri'])
    print(id)
    tracklist = get_playlist_tracks(id, bpm)
    #tracklist = get_playlist_tracks("spotify:playlist:0H0bCcEmeCAuACr9TW5gNs?si=8be86da0f0454144")
    playback(tracklist, bpm, songs)
def queue(uri):
    sp.add_to_queue(uri, device_id=None)

def get_playlist_tracks(playlist_id, bpm):
    results = sp.playlist_items(playlist_id)

    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def playback(tracklist, bpm, songs):
    devices = sp.devices()
    context_uri = "spotify:playlist:0H0bCcEmeCAuACr9TW5gNs?si=8be86da0f0454144"
    counter = 0
    counter1 = 0
    for i in range(len(tracklist)):
        print(counter1)

        if(int(counter1) == int(songs)):
            exit(0)

        ind = random.randrange(0, len(tracklist))
        if i < len(tracklist) and 'track' in tracklist[ind]:
            trackOn = tracklist[ind]['track']
            if(trackOn['id']):
                trackInfo = sp.audio_features(trackOn['id'])
            else:
                continue
            trackBpm = int(trackInfo[0].get('tempo'))
            if  trackBpm > int(bpm) - 5 and trackBpm < int(int(bpm) + 5 ):
                stat = sp.currently_playing()
                if (stat == None):
                    print("Shuffle the playlist you want to filter")
                    time.sleep(5)
                else:
                    if (counter == 0):
                        sp.next_track()
                        counter = 1
                        counter1 = counter1 + 1
                    else:
                       print(trackOn['artists'][0]['name'], " – ", trackOn['name'], " - ",
                       int(trackInfo[0].get('tempo')))
                       queue(trackOn['id'])
                       counter1 = counter1 + 1
        time.sleep(5)

driver()
