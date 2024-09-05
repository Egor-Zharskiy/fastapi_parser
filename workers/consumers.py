import asyncio

from workers.services.lamoda_consumer import LamodaConsumer
from workers.services.twitch_consumer import TwitchConsumer


async def start_all_consumers():
    lamoda_consumer = LamodaConsumer()
    twitch_consumer = TwitchConsumer()

    await asyncio.gather(
        twitch_consumer.consume_parse_games(),
        twitch_consumer.consume_parse_streamers(),
        twitch_consumer.consume_parse_streams(),
        lamoda_consumer.consume_parse_brands(),
        lamoda_consumer.consume_parse_category(),
    )


if __name__ == "__main__":
    asyncio.run(start_all_consumers())
