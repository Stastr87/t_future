"""Generate figi id list of instruments"""

from tinkoff.invest import InstrumentShort, InstrumentType

from clients.t_client.instrument_service.instruments_id_types import (
    InstrumentsIdTypes,
)
from clients.t_client.instrument_service.instruments_servise import (
    InstrumentsService,
)
from utils.logger.common_logger import common_logger


def get_base_instrument(base_instrument_name: str) -> list[InstrumentShort]:
    """Find base instrument figi id by name"""
    shares_list = InstrumentsService().find_instrument(base_instrument_name)
    return shares_list


def get_futures_list(
    base_instrument_name: str, base_instrument_ticker: str
) -> list[str]:
    """Returns list of figi id of futures according the base instrument name
    sorted by expiration date"""

    try:
        futures_list = InstrumentsService().find_instrument(
            base_instrument_name, type_=InstrumentType.INSTRUMENT_TYPE_FUTURES
        )

        if len(futures_list) == 0:
            raise ValueError(
                f'Фьючерсов для базового инструмента "{base_instrument_name}" не найдено'
            )

    except ValueError as err:
        common_logger.warning(err)
        futures_list = []

    temp_future_list = []
    for item in futures_list:
        full_future_obj = InstrumentsService().get_futures_by(
            future_id=item.figi,
            market_id_type=InstrumentsIdTypes.INSTRUMENT_ID_TYPE_FIGI,
        )

        if full_future_obj.basic_asset == base_instrument_ticker:
            temp_future_list.append(full_future_obj)

    result_futures_list = sorted(
        temp_future_list, key=lambda future: future.expiration_date
    )

    result_figi_list = []
    for item in result_futures_list:
        result_figi_list.append(item.figi)

    return result_figi_list


def generate_base_with_futures(instrument_name: str) -> list[list[str]]:
    """Returns list of figi id: base instruments with next futures"""

    result_figi_list: list[list[str]] = []
    base_instrument_list = get_base_instrument(instrument_name)

    for base_instrument in base_instrument_list:
        temp_list = []
        temp_list.append(base_instrument.figi)
        futures_list_by_base_instrument = get_futures_list(
            instrument_name, base_instrument.ticker
        )
        temp_list.extend(futures_list_by_base_instrument)
        result_figi_list.append(temp_list)

    return result_figi_list
