# spotify_functions.py

import random
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client(cred):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=cred.client_id,
        client_secret=cred.client_secret,
        redirect_uri=cred.redirect_url,
        scope=cred.SPOTIFY_SCOPE
    ))

def get_playlist_tracks(sp, playlist_id):
    tracks = []
    offset = 0
    limit = 100  # Adjust the batch size as needed

    while True:
        results = sp.playlist_items(playlist_id, offset=offset, limit=limit)
        if not results['items']:
            break
        tracks.extend(results['items'])
        offset += limit

    return tracks
def get_filtered_tracks(sp, playlist_id, bpm):
    # Get all tracks from the playlist
    tracks = get_playlist_tracks(sp, playlist_id)

    # Filter tracks by BPM
    filtered_tracks = []

    for track in tracks:
        if 'track' in track:
            track_info = track['track']
            if track_info['id']:
                filtered_tracks.append(track_info)

    # Further filter by BPM in Python (rather than making additional API calls)
    filtered_tracks = [
        track for track in filtered_tracks
        if abs(int(sp.audio_features(track['id'])[0].get('tempo')) - int(bpm)) <= 5
    ]

    return filtered_tracks

