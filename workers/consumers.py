from workers.services.lamoda_consumer import LamodaConsumer
from workers.services.twitch_consumer import TwitchConsumer


def start_all_consumers(funcs: list):
    import threading

    threads = []
    for func in funcs:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    twitch_consumer = TwitchConsumer()
    lamoda_consumer = LamodaConsumer()
    funcs = [twitch_consumer.consume_parse_games, twitch_consumer.consume_parse_streams,
             twitch_consumer.consume_parse_streamers, lamoda_consumer.consume_parse_brands,
             lamoda_consumer.consume_parse_category]
    start_all_consumers(funcs)
    # lamoda_consumer.consume_parse_category()
    # lamoda_consumer.consume_parse_brands()
    # consumer = TwitchConsumer()
    # consumer.start_all_consumers()
    # consumer.consume_parse_streamers()
    # consumer.consume_parse_streams()
    # consumer.consume_parse_games()
