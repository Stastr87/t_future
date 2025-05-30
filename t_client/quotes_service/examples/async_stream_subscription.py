"""Подписка на стрим котировок по минутным свечам и вывод получаемых свечей в консоль"""

import asyncio
from pprint import pprint

from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

from env.config import TOKEN


async def main():
    """main"""

    async def request_iterator():
        """iterator"""
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        figi="BBG004730N88",
                        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                    )
                ],
            )
        )
        while True:
            await asyncio.sleep(1)

    async with AsyncClient(TOKEN) as client:
        async for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):
            pprint(marketdata.__dict__)


if __name__ == "__main__":
    asyncio.run(main())
