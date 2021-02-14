import json
from collections import defaultdict

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConflictError

es = Elasticsearch(['poc-es01', 'poc-es02', 'poc-es03'])
orphan_map = defaultdict(list)
INDEX = 'music'


def process_message(message_obj: str):
    message = json.loads(message_obj.value())

    indexer_mapper = {
        'artist': index_artist,
        'album': index_album,
        'song': index_song,
    }

    try:
        indexer_mapper[message['type']](message)
    except ConflictError:
        print('There was a duplicate... check the database: ', message)


def index_artist(artist: dict):
    artist['joint_fields'] = 'artist'
    artist_id = 'art-{}'.format(slugify(artist['artist_name']))

    if es.exists(INDEX, id=artist_id):
        es.update(INDEX, id=artist_id, body=artist)
    else:
        es.create(INDEX, id=artist_id, body=artist)

    if artist_id in orphan_map.keys():
        for album in orphan_map[artist_id]:
            index_album(album)
        del orphan_map[artist_id]


def index_album(album: dict):
    artist_id = 'art-{}'.format(slugify(album['artist']))

    if es.exists(INDEX, id=artist_id):
        album_id = 'alb-{}'.format(slugify(album['album_name']))
        album['joint_fields'] = {
            'name': 'album',
            'parent': artist_id,
        }

        if es.exists(INDEX, id=album_id):
            es.update(INDEX, id=album_id, body=album, routing=artist_id)
        else:
            es.create(INDEX, id=album_id, body=album, routing=artist_id)

        if album_id in orphan_map.keys():
            for song in orphan_map[album_id]:
                index_song(song)
            del orphan_map[album_id]
    else:
        orphan_map[artist_id].append(album)


def index_song(song: dict):
    album_id = 'alb-{}'.format(slugify(song['album']))

    if es.exists(INDEX, id=album_id):
        song_id = 'sng-{}'.format(slugify(song['song_name']))
        song['joint_fields'] = {
            'name': 'song',
            'parent': album_id,
        }
        if es.exists(INDEX, id=song_id):
            es.update(INDEX, id=song_id, body=song, routing=album_id)
        else:
            es.create(INDEX, id=song_id, body=song, routing=album_id)
    else:
        orphan_map[album_id].append(song)


def slugify(string: str) -> str:
    return '-'.join(string.split(' '))
