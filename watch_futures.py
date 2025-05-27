"""monitoring prices"""
import time
from pprint import pprint

from t_client.instrument_service.instruments_servise import InstrumentsService
from t_client.quotes_service.market_data_stream_service import MarketDataStream
from utils.common import CustomThread


def watch_futures(instrument_guids):
    """Collect hardware usage data"""
    stream = MarketDataStream(figi_id_list=instrument_guids)
    while True:
        for item in instrument_guids:
            future = InstrumentsService().get_instrument_by(item).instrument
            # pprint(future.__dict__)
            print("==================================")
            print(future.name)
            print(future.figi)
            print("==================================")
        print("market data:")
        pprint(stream.data)
        time.sleep(10)

if __name__ == "__main__":


    figi_list = ["FUTASTR09250", "FUTASTR06250"]

    watch_futures_thread = CustomThread(
        "watch_futures", watch_futures(figi_list), daemon=False
    )
    watch_futures_thread.start()
