"""Подписка на стрим минутных свечей и их вывод"""

import time
from pprint import pprint

from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

from env.config import TOKEN

instr_list = [
    CandleInstrument(
        figi="BBG004730N88",
        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
    )
]


def request_iterator(instruments_list: list[CandleInstrument]):
    """iterator"""
    yield MarketDataRequest(
        subscribe_candles_request=SubscribeCandlesRequest(
            waiting_close=True,
            subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
            instruments=instruments_list,
        )
    )
    while True:
        time.sleep(1)


with Client(TOKEN) as client:
    for marketdata in client.market_data_stream.market_data_stream(
        request_iterator(instr_list)
    ):
        pprint(marketdata.__dict__)
