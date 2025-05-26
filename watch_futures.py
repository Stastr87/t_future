"""monitoring prices"""

from t_client.instrument_service.instruments_servise import InstrumentsService
from t_client.quotes_service.market_data_stream_service import MarketDataStream
from utils.common import CustomThread


def watch_futures(instrument_guids):
    """Collect hardware usage data"""
    while True:
        for item in instrument_guids:
            future = InstrumentsService().get_instrument_by(item).instrument
            # pprint(future.__dict__)
            print("==================================")
            print(future.name)
            print(future.figi)
            print("==================================")
        market_data = MarketDataStream(figi_id_list=instrument_guids)
        print("market data:")
        market_data.wait_data()


if __name__ == "__main__":

    # ТУТ НАДО ПОРАБОТАТЬ НАД ВИЗУАЛИЗАЦИЕЙ
    figi_list = ["FUTASTR09250", "FUTASTR06250"]

    watch_futures_thread = CustomThread(
        "watch_futures", watch_futures(figi_list), daemon=False
    )
    watch_futures_thread.start()
