import random
import os

def build_data(path: str) -> list:
    result = []
    for (root, dirs, files) in os.walk(path, topdown=True):
        if len(root.split('/')) == 2:
            # This is an artists directory
            artists = collect_artists(dirs)
            result.extend(artists)
        elif len(root.split('/')) == 3:
            # This is an albums directory
            albums = collect_albums(root, dirs)
            result.extend(albums)
        elif len(root.split('/')) == 4:
            # This is a songs directory
            songs = collect_songs(root, files)
            result.extend(songs)
    random.shuffle(result)
    return result


def collect_artists(artists: list) -> list:
    return [{'type': 'artist', 'artist_name': artist.lower()} for artist in artists]


def collect_albums(path: str, albums: list) -> list:
    artist = path.split('/')[-1]
    return [
        {
            'type': 'album',
            'artist': artist.lower(),
            'album_name': album.lower(),
        } for album in albums
    ]


def collect_songs(path: str, songs: list) -> list:
    path_tokens = path.split('/')
    album = path_tokens[-1]
    artist = path_tokens[-2]
    result = []
    for song in songs:
        with open(os.path.join(path, song), 'r') as song_file:
            lyrics = song_file.read()
            lyrics = lyrics.split('_____')[0].strip()
        result.append({
            'type': 'song',
            'song_name': song.lower(),
            'album': album.lower(),
            'lyrics': lyrics,
        })
    return result

