
import cred
import spotify_functions
import random
import time
def driver():
    # Initialize Spotify client
    sp = spotify_functions.create_spotify_client(cred)
    print("Welcome to the Spotify Tempo Tool! This is a tool to take a spotify playlist and queue up a few songs within a tempo range")
    print()
    time.sleep(3)
    print("Please ensure the playlist you are using is not too long, as too many songs can overwhelm the system :(")
    print()
    time.sleep(3)
    input("To begin, open Spotify and shuffle the playlist you would like to play songs from, then hit ENTER")
    print()
    bpm = input("Enter the BPM you want to play: ")
    songs = input("Enter the number of songs you would like to practice with: ")

    # Get the URI of the currently playing playlist
    id = sp.currently_playing()['context']['uri']
    print("Received playlist, currently searching for songs around " + bpm + " bpm!")
    print()
    # Get filtered tracks from the playlist based on BPM
    filtered_tracks = spotify_functions.get_filtered_tracks(sp, id, bpm,songs)
    print("Playlist has been filtered, shuffling " + songs + " songs out of " + str(len(filtered_tracks)) + " found!")
    print()
    playback(sp, filtered_tracks,bpm, songs)

    print()
    print("All songs have been queued, thank you!")
def playback(sp, tracklist, bpm, songs):
    counter1 = 0

    while counter1 < int(songs):
        if not tracklist:
            print("No more tracks in the filtered list.")
            break

        # Randomly select a track from the filtered list
        selected_track = random.choice(tracklist)


        print(selected_track['artists'][0]['name'], " – ", selected_track['name'])

        sp.add_to_queue(selected_track['id'], device_id=None)

        if (counter1 == 0):
            sp.next_track()
        else:
            time.sleep(10)
        # Remove the selected track from the list to prevent duplicates
        tracklist.remove(selected_track)

        counter1 += 1

if __name__ == "__main__":
    driver()