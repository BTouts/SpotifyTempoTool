import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import time


def create_spotify_client(cred):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=cred.client_id,
        client_secret=cred.client_secret,
        redirect_uri=cred.redirect_url,
        scope=cred.SPOTIFY_SCOPE
    ))


def get_filtered_tracks(sp, playlist_id, bpm, num_songs, delay=2):
    # Get all tracks from the playlist
    tracks = get_playlist_tracks(sp, playlist_id)

    # Filter tracks by BPM
    filtered_tracks = []
    count = 0
    for t in range((len(tracks))):
        if(count == num_songs):
            break
        track = random.choice(tracks)
        if 'track' in track:
            track_info = track['track']
            if track_info['id']:
                track_bpm = int(sp.audio_features(track_info['id'])[0].get('tempo'))
                if abs(track_bpm - int(bpm)) <= 5:
                    filtered_tracks.append(track_info)
                    count = count + 1

    # Introduce a delay between API calls to stay within rate limits
    for _ in filtered_tracks:
        time.sleep(delay)

    return filtered_tracks


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

