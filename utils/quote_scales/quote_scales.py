"""quote scales utils"""

from datetime import datetime, timedelta

import pytz
from prettytable import PrettyTable
from tinkoff.invest import InstrumentType

from clients.t_client.instrument_service.instruments_id_types import (
    InstrumentsIdTypes,
)
from clients.t_client.instrument_service.instruments_servise import (
    InstrumentsService,
)
from clients.t_client.quotes_service.quotes import MarketDataService
from clients.t_client.quotes_service.schema.schema import FigiListSchema
from clients.t_client.utils.data_converter import t_quotation_to_float
from utils.common import display_result, sum_elements
from utils.quote_scales.schema.schema import (
    CalculatedDataSchema,
    QuotesScalesResponse,
)
from utils.quote_scales.utils.quote_scales_utils import (
    add_futures_deviation,
    get_dif,
    get_fair_future_price_as_str,
    get_future_price,
    get_percent_from_value_as_str,
)


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
        calculation_object: list[CalculatedDataSchema] = []

        base_instrument_dividend: float = 0
        base_instrument_price: float = 0

        for i, instrument in enumerate(raw_data):
            new_item = CalculatedDataSchema()
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

                    new_item.figi_id = instrument.figi_id
                    new_item.instrument_name = instrument.instrument_name
                    new_item.currency = instrument.currency
                    new_item.ticker = instrument.ticker
                    new_item.price = instrument.price
                    new_item.dif = round(
                        get_dif(raw_data[i - 1].price, instrument.price), 2
                    )
                    new_item.fair_price = get_fair_future_price_as_str(
                        base_instrument_price,
                        new_item.days_for_expiration,
                        base_instrument_dividend,
                    )

                case _:
                    new_item.figi_id = instrument.figi_id
                    new_item.instrument_name = instrument.instrument_name
                    new_item.currency = instrument.currency
                    new_item.ticker = instrument.ticker
                    new_item.price = instrument.price

                    now = datetime.now(tz=pytz.UTC)
                    next_year = now + timedelta(days=365)
                    expected_dividends = InstrumentsService(
                        instrument.figi_id, from_date=now, to_date=next_year
                    ).get_expected_dividends()

                    div_list = list(map(lambda x: x.value, expected_dividends))
                    base_instrument_dividend = sum_elements(div_list)
                    base_instrument_price = instrument.price
                    new_item.next_dividends_value = base_instrument_dividend

            calculation_object.append(new_item)

        return add_futures_deviation(calculation_object)

    @display_result
    def show_table(self):
        """Show table with result"""
        calculated_data = self.get_calculation()
        table = PrettyTable()

        table.field_names = [
            "instrument",
            "currency",
            "price",
            "dif, %",
            "days_to_exp",
            "next dividends",
            "fair_price",
            "deviation, %",
        ]

        if calculated_data:
            table.add_rows(
                [
                    [
                        f"{item.instrument_name} ({item.ticker})",
                        item.currency,
                        item.price,
                        item.dif,
                        item.days_for_expiration,
                        get_percent_from_value_as_str(
                            item.next_dividends_value, item.price
                        ),
                        item.fair_price,
                        item.deviation,
                    ]
                    for item in calculated_data
                ]
            )
        return table
