
import cred
import spotify_functions
import random
def driver():
    # Initialize Spotify client
    sp = spotify_functions.create_spotify_client(cred)

    input("To begin, open Spotify and shuffle the playlist you would like to play songs from, then hit ENTER")

    bpm = input("Enter the BPM you want to play: ")
    songs = input("Enter the number of songs you would like to practice with")

    # Get the URI of the currently playing playlist
    id = sp.currently_playing()['context']['uri']
    print(id)

    # Get filtered tracks from the playlist based on BPM
    filtered_tracks = spotify_functions.get_filtered_tracks(sp, id, bpm)
    print("filtered list")
    playback(sp, filtered_tracks,bpm, songs)

    print("started playback")
def playback(sp, tracklist, bpm, songs):
    counter1 = 0

    while counter1 < int(songs):
        if not tracklist:
            print("No more tracks in the filtered list.")
            break

        # Randomly select a track from the filtered list
        selected_track = random.choice(tracklist)


        print(selected_track['artists'][0]['name'], " – ", selected_track['name'], " - ", int(bpm))
        sp.add_to_queue(selected_track['id'], device_id=None)

        if (counter1 == 0):
            sp.next_track()

        # Remove the selected track from the list to prevent duplicates
        tracklist.remove(selected_track)

        counter1 += 1

if __name__ == "__main__":
    driver()