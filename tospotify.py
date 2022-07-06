import spotipy
from from_amazon import get_list_of_songs
from fuzzywuzzy import fuzz
from spotipy import util
from spotipy.oauth2 import SpotifyOAuth

client_secret = "ee1c44a4e3974c699f941826675aac2a"
scope = "playlist-modify-public"
id_user = "nd6otb32e4iqkjly6hoa17ge3"     # my spotify user id
id_client = "27463b3d497541799a2db077ab61a7f7"

token = util.prompt_for_user_token(username=id_user, scope=scope, client_id=id_client,
                                   client_secret=client_secret, redirect_uri='http://localhost:8080/')
sp = spotipy.Spotify(auth=token)


def IDS_tracks(song_titles):
    id_track_list = []

    for i in range(len(song_titles)):
        results = sp.search(q={song_titles[i]}, limit=5, type='track')

        if results['tracks']['total'] != 0:
            for j in range(len(results['tracks']['items'])):
                if fuzz.partial_ratio(results['tracks']['items'][j]['name'], song_titles[i]) > 90:
                    id_track_list.append(results['tracks']['items'][j]['id'])
                    break

    return id_track_list


def create_playlist(name_of_playlist, descrip):
    sp.user_playlist_create(user=id_user, name=name_of_playlist, description=descrip)


def ID_playlist(username, name_of_playlist):
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        # print(playlist['name'])
        if playlist['name'] == name_of_playlist:
            playlist_id = playlist['id']
    return playlist_id


def add_all_tracks_to_playlist(username, playlist_id, id_track_list):
    sp.user_playlist_add_tracks(username, playlist_id, id_track_list)


url_amazon_playlist = "https://music.amazon.in/playlists/B07WV4DNDR?"    # playlist link from amazon music
description = "my go to workout playlist from now!!"   # description of the new playlist you want on spotify
name_of_playlist = "my_workout_music"               # name of the new playlist you want on spotify

list_of_songs = get_list_of_songs(url_amazon_playlist)
# print(len(list_of_songs))
id_track_list = IDS_tracks(song_titles=list_of_songs)
# print(id_track_list)
create_playlist(name_of_playlist, description)
# create new playlist on your spotify
playlist_id = ID_playlist(id_user,name_of_playlist)
# print(playlist_id)
add_all_tracks_to_playlist(username=id_user,playlist_id=playlist_id,id_track_list=id_track_list)
# transferred all songs