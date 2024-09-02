kafka-topics.sh --create --topic parse_streamers_topic \
               --partitions 3 --replication-factor 2 \
               --bootstrap-server localhost:9092

kafka-topics.sh --create --topic parse_streams_topic \
               --partitions 5 --replication-factor 3 \
               --bootstrap-server localhost:9092

kafka-topics.sh --create --topic parse_games_topic \
               --partitions 2 --replication-factor 1 \
               --bootstrap-server localhost:9092
