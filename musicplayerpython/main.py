import os
import json
import time
import spotipy
import lyricsgenius as lg

SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
SPOTIPY_REDIRECT_URI = 'https://google.com'
GENIUS_ACCESS_TOKEN = 'your_genius_access_token'

scope = 'user-read-currently-playing'

oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                    scope=scope)

token_dict = oauth_object.get_access_token()
token = token_dict['access_token']

# Our spotify object
spotify_object = spotipy.Spotify(auth=token)

# Genius object
genius = lg.Genius(GENIUS_ACCESS_TOKEN)

previous_track_name = None
previous_track_artist = None

while True:
    try:
        # Retrieve current playing track
        current = spotify_object.currently_playing()

        if current is not None and current['currently_playing_type'] == 'track':
            current_track_name = current['item']['name']
            current_track_artist = current['item']['album']['artists'][0]['name']

            # Check if the current track is different from the previous one
            if (current_track_name != previous_track_name) or (current_track_artist != previous_track_artist):
                # Search for lyrics only if the track is different
                song = genius.search_song(title=current_track_name, artist=current_track_artist)
                if song is not None:
                    lyrics = song.lyrics

                    # Filter out unwanted lines
                    filtered_lyrics = ""
                    for line in lyrics.split('\n'):
                        if not any(word in line for word in
                                   ["Embed", "Contributor", "Contributors", "Translations", "Español", "Português", "Kiswahili", "Deutsch",
                                    "Italiano", "Српски", "Nederlands", "Svenska", "Polski", "Türkçe", "Ελληνικά",
                                    "Français", "Dansk", "日本語", "Русский", "العربية", "Українська", "Bahasa Indonesia",
                                    "فارسی"]):
                            filtered_lyrics += line + '\n'

                    print("Currently playing:", current_track_name, "by", current_track_artist)
                    print("", filtered_lyrics, '\n')
                else:
                    print("No lyrics found for:", current_track_name, "by", current_track_artist)

                # Update previous track information
                previous_track_name = current_track_name
                previous_track_artist = current_track_artist
        else:
            print("No track is currently playing.")

        # Wait for a short duration before checking again
        time.sleep(5)
    except KeyboardInterrupt:
        break