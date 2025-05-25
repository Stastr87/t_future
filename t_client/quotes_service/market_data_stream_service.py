"""Stream type to get market data"""

import asyncio

from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

from env.config import TOKEN


class MarketDataStream:
    """Market data stream object"""

    def __init__(self, figi_id, interval: SubscriptionInterval = None):
        self.instrument_id = figi_id
        self.interval = interval
        self.set_interval()
        asyncio.run(self.wait_data())

    def set_interval(
        self, new_interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE
    ):
        """Set new interval to get market data"""
        if not self.interval:
            self.interval = new_interval

    async def wait_data(self):
        """Wait data from broker"""
        async with AsyncClient(TOKEN) as client:
            async for marketdata in client.market_data_stream.market_data_stream(
                self.request_iterator()
            ):
                print(marketdata)

    async def request_iterator(self):
        """Returns data object from server"""
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        figi=self.instrument_id,
                        interval=self.interval,
                    )
                ],
            )
        )
        while True:
            await asyncio.sleep(1)
