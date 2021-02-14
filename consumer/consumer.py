from confluent_kafka import Consumer

from message_processor import process_message

config = {
    'bootstrap.servers': 'broker:9092',
    'group.id': 'israel-group',
    'auto.offset.reset': 'smallest',
}

consumer = Consumer(config)

running = True

def basic_consume(consumer: Consumer, topics: list):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                process_message(msg)
    finally:
        consumer.close()

def shutdown():
    running = False


basic_consume(consumer, ['israel-test-topic',])
