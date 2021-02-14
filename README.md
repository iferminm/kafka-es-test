# kafka-es-test
Playing around with Kafka and Elasticsearch indexing a small taxonomy with unordered messages

It indexes a 3 level parent-child set of documents.

Artist -> Album -> Song

4054 documents in total

# How to run it

The docker-compose file has all the confluent kafka stack + elasticsearch and kibana, producer and consumer are inside their respective directories and are meant to be run separate.

Start kafka and elasticsearch containers
```bash
docker-compose up -d
```

Now, go to kafka control centeer and create the topic, name it `israel-test-topic`

http://127.0.0.1:9021/

Then, go to kibana and execute the following request in the developer tools tab

* Create the index and the mapping
```json
PUT /music
{
  "mappings": {
      "properties": {
        "artist": { "type": "text" },
        "album": { "type": "text" },
        "song": { "type": "text" },
        "joint_fields": {
          "type": "join",
          "relations": {
            "artist": "album",
            "album": "song"
          }
        }
      }
    }
  }  
```

## Run producer and consumer
In a terminal go to the consumer directory and run the following:

```bash
docker image build -t consumer:test .
docker container start -it --network=kafka-unordered_kafka-poc consumer:test bash
```

Then in a separate terminal tab go to the producer directory and run the following

```bash
docker image build -t producer:test .
docker container start -it --network=kafka-unordered_kafka-poc producer:test bash
```

Inside the consumer container run:

```bash
python consumer.py
```

Inside the producer container run

```bash
python producer.py
```

Check the progress in both Kafka Control Center and Kibana
