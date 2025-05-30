"""quote scales utils"""

from datetime import datetime

import pytz
from prettytable import PrettyTable
from tinkoff.invest import InstrumentType

from quote_scales.schema.schema import (
    CalculatedDataSchema,
    QuotesScalesResponse,
)
from quote_scales.utils.quote_scales_utils import get_dif, get_future_price
from t_client.instrument_service.instruments_id_types import InstrumentsIdTypes
from t_client.instrument_service.instruments_servise import InstrumentsService
from t_client.quotes_service.quotes import MarketDataService
from t_client.quotes_service.schema.schema import FigiListSchema
from t_client.utils.data_converter import t_quotation_to_float
from utils.common import display_result


class QuotesScales:
    """It contains a set of functions for comparing instrument quotes"""

    def __init__(self, instruments_list: list[str]):
        self.instruments = instruments_list

    def get_last_prises_for_figi_list(self):
        """Returns last prices for list of instruments"""

        body = FigiListSchema(figi_list=self.instruments)
        resp = MarketDataService().get_quotes_by_figi(body)
        return resp.last_prices

    def get_quotes(self) -> list[QuotesScalesResponse]:
        """Returns qutes of list of instruments"""

        server_resp = self.get_last_prises_for_figi_list()
        result = []
        for item in server_resp:
            instrument_info = InstrumentsService().get_instrument_by(
                item.figi, InstrumentsIdTypes.INSTRUMENT_ID_TYPE_FIGI
            )
            match instrument_info.instrument_kind:
                case InstrumentType.INSTRUMENT_TYPE_FUTURES:
                    future_object = InstrumentsService().get_futures_by(
                        instrument_info.figi, InstrumentsIdTypes.INSTRUMENT_ID_TYPE_FIGI
                    )

                    converted_price = get_future_price(future_object, item.price)
                case _:
                    converted_price = t_quotation_to_float(item.price)

            new_item = QuotesScalesResponse(
                figi_id=item.figi,
                instrument_name=instrument_info.name,
                ticker=instrument_info.ticker,
                price=converted_price,
                currency=instrument_info.currency,
            )
            result.append(new_item)
        return result

    def get_calculation(self) -> list[CalculatedDataSchema]:
        """Returns calculated data for group of instruments"""
        raw_data = self.get_quotes()
        calculation_result: list[CalculatedDataSchema] = []

        for i, instrument in enumerate(raw_data):
            new_item = CalculatedDataSchema()
            if i == 0:
                new_item = CalculatedDataSchema(
                    figi_id=instrument.figi_id,
                    instrument_name=instrument.instrument_name,
                    currency=instrument.currency,
                    ticker=instrument.ticker,
                    price=instrument.price,
                )
            elif i > 0:
                dif = get_dif(raw_data[i - 1].price, instrument.price)
                new_item = CalculatedDataSchema(
                    figi_id=instrument.figi_id,
                    instrument_name=instrument.instrument_name,
                    currency=instrument.currency,
                    ticker=instrument.ticker,
                    price=instrument.price,
                    dif=round(dif, 2),
                )
            instrument_info = InstrumentsService().get_instrument_by(
                instrument.figi_id, InstrumentsIdTypes.INSTRUMENT_ID_TYPE_FIGI
            )
            match instrument_info.instrument_kind:

                case InstrumentType.INSTRUMENT_TYPE_FUTURES:
                    futures = InstrumentsService().get_futures_by(
                        instrument.figi_id, InstrumentsIdTypes.INSTRUMENT_ID_TYPE_FIGI
                    )
                    new_item.days_for_expiration = (
                        futures.expiration_date - datetime.now(tz=pytz.UTC)
                    ).days

            calculation_result.append(new_item)
        return calculation_result

    @display_result
    def show_table(self):
        """Show table with result"""
        calculated_data = self.get_calculation()
        table = PrettyTable()
        table.field_names = [
            "instrument",
            "ticker",
            "currency",
            "price",
            "dif, %",
            "days_to_exp",
        ]

        if calculated_data:
            table.add_rows(
                [
                    [
                        item.instrument_name,
                        item.ticker,
                        item.currency,
                        item.price,
                        item.dif,
                        item.days_for_expiration,
                    ]
                    for item in calculated_data
                ]
            )
        return table
