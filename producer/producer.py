import json
import socket

from confluent_kafka import Producer

from data_builder import build_data


"""
artist -> album -> song

artist:
{
    name: string
}

album:
{
    artist: parent_id->band
    name: string
    year: int
}

song:
{
    album: parent_id->album
    name: string
    order: int
    lyrics: text
}
"""


config = {
    'bootstrap.servers': 'broker:9092',
    'client.id': socket.gethostname(),
}

producer = Producer(config)

messages = build_data('database')

for message in messages:
    producer.produce('israel-test-topic', value=json.dumps(message), headers={'content-type': 'application/json'})
    producer.flush()

