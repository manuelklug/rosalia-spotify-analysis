import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import csv
import _csv

def get_data(client_ID: str, client_secret: str, artist_ID: str) -> '_csv._writer':
    """Gets tracks' data from a specific artist using the Spotify API and writes it to a CSV file. 

    Args:
        client_ID (str): The Spotify API client ID  
        client_secret (str): The Spotify API client secret key
        artist_ID (str): The Spotify ID of the artist 

    Returns:
        artist_tracks: A CSV file with the audio features for all the songs of an artist"""
    
    # Creates a Client Credentials Flow Manager.
    client_credentials_manager = SpotifyClientCredentials(client_id = client_ID,
                                                  client_secret = client_secret)
    
    # Creates a Spotify API client.
    sp = spotipy.Spotify(auth_manager = client_credentials_manager)
    
    # The Spotify ID of the artist.
    artist_URI = f'spotify:artist:{artist_ID}'
    
    # Get Spotify catalog information about an artist’s albums
    results = sp.artist_albums(artist_URI, album_type="album")
    albums = results["items"]
    
    # Iterate over the artist's albums and artist's tracks to get the audio features for every song.
    track_data = []

    for album in albums:
        album_name = album["name"]
        album_uri = album["uri"]

        album_tracks = sp.album_tracks(album_uri)

        for track in album_tracks["items"]:
            track_name = track["name"]
            track_id = track["id"]
            track_number = track["track_number"]
            track_duration = track["duration_ms"]
            track_uri = track["uri"]

            track_audio_features = sp.audio_features(track_uri)

            track_acousticness = track_audio_features[0]["acousticness"]
            track_danceability = track_audio_features[0]["danceability"]
            track_energy = track_audio_features[0]["energy"]
            track_instrumentalness = track_audio_features[0]["instrumentalness"]
            track_key = track_audio_features[0]["key"]
            track_liveness = track_audio_features[0]["liveness"]
            track_loudness = track_audio_features[0]["loudness"]
            track_mode = track_audio_features[0]["mode"]
            track_speechiness = track_audio_features[0]["speechiness"]
            track_tempo = track_audio_features[0]["tempo"]
            track_time_signature = track_audio_features[0]["time_signature"]
            track_valence = track_audio_features[0]["valence"]

            track_list = [album_name, track_number, track_name, track_id, track_duration, track_acousticness,
                         track_danceability, track_energy, track_instrumentalness, track_key, track_liveness,
                         track_loudness, track_mode, track_speechiness, track_tempo, track_time_signature, 
                         track_valence]

            track_data.append(track_list)
    
    # Creates and writes the data to a CSV file
    with open('data/artist_tracks.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        header = ["album_name", "track_number", "song_title", "id", "duration", 
                  "acousticness","danceability", "energy", "instrumentalness", "key", 
                  "liveness","loudness", "mode", "speechiness",
                  "tempo", "time_signature", "valence"]

        writer.writerow(header)

        for track in track_data:
            writer.writerow(track)


# Artist ID
rosalia_ID = "7ltDVBr6mKbRvohxheJ9h1"

# Credentials
client_ID = "your-client-ID"
client_secret = "your-client-secret-key"

if __name__ == "__main__":
    get_data(client_ID = client_ID, 
             client_secret = client_secret, 
             artist_ID = rosalia_ID)