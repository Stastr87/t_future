"""instruments service"""

from datetime import datetime

from tinkoff.invest import Client, Future, InstrumentIdType, GetDividendsRequest, GetDividendsResponse, Dividend
from tinkoff.invest.exceptions import RequestError

from env.config import TOKEN
from t_client.instrument_service.instruments_id_types import InstrumentsIdTypes
from t_client.instrument_service.schema.schema import DividendsSchema, NormalizedDividendsSchema
from t_client.schemas.nearest_coupon_schema import NearestCouponSchema
from t_client.utils.data_converter import t_quotation_to_float
from utils.logger.common_logger import common_logger


class InstrumentsService:
    """Сервис предназначен для получения информации об инструментах"""

    def __init__(self, instrument_figi: str = '', from_date: datetime = None, to_date: datetime = None):

        self._token = TOKEN
        self.figi = instrument_figi
        self.from_date = from_date
        self.to_date = to_date

    def set_instrument(self, instrument_figi):
        """Set figi class attrib"""
        self.figi = instrument_figi

    def set_from_date(self, from_date: datetime):
        """Set from_date class attrib for historic requests"""
        self.from_date = from_date

    def set_to_date(self, to_date: datetime):
        """Set to_date class attrib for historic requests"""
        self.to_date = to_date


    def get_bond_by_figi(self, figi):
        """Метод возвращает данные об инструменте типа Bond
        по его figi идентификатору
        """
        with Client(self._token) as client:
            try:
                common_logger.info(
                    "%s -> try to get_bond_by_figi() -> figi: %s", __name__, figi
                )
                response_data = client.instruments.bond_by(id_type=1, id=figi)
            except RequestError as err:
                response_data = None
                common_logger.error("%s -> get_bond_by_figi() -> %s", __name__, err)

        return response_data

    def get_bond_coupons_list(self, figi_id):
        """GetBondCoupons метод возвращает массив объектов типа Coupon"""
        with Client(self._token) as client:
            try:
                common_logger.info(
                    "%s -> try to get_bond_coupons() -> figi: %s", __name__, figi_id
                )
                response_data = client.instruments.get_bond_coupons(figi=figi_id)
            except RequestError as err:
                response_data = None
                common_logger.error("%s -> get_bond_coupons() -> %s", __name__, err)
        return response_data

    def get_nearest_coupon(self, figi) -> NearestCouponSchema:
        """Метод возвращает дату ближайшего купона и его величину в формате MoneyValue:
        nearest_coupon_date, nearest_coupon_money_value
        """
        response_schema = NearestCouponSchema()
        coupons_list_response = self.get_bond_coupons_list(figi)
        coupons_list = coupons_list_response.events
        now = datetime.now().timestamp()
        future_coupon_list = []
        for i, coupon in enumerate(coupons_list):
            if coupon.coupon_date.timestamp() > now:
                future_coupon_list.append(coupon)

        for i, future_coupon in enumerate(future_coupon_list):
            if future_coupon.coupon_number < future_coupon_list[i - 1].coupon_number:
                response_schema.date = future_coupon_list[
                    len(future_coupon_list) - 1
                ].coupon_date
                response_schema.money_value = future_coupon_list[
                    len(future_coupon_list) - 1
                ].pay_one_bond

        return response_schema

    def get_currencies(self):
        """Метод возвращает список валют на рынке,
        имеющих статус 1 (Базовый список инструментов (по умолчанию).
        Инструменты доступные для торговли через TINKOFF INVEST API.)
        """
        with Client(self._token) as client:
            response_data = client.instruments.currencies(instrument_status=1)
        return response_data

    def get_currency_by(self, currency_id):
        """Метод получения валюты по её идентификатору"""
        with Client(self._token) as client:
            response_data = client.instruments.currency_by(id_type=1, id=currency_id)
        return response_data

    def get_instrument_by(
        self, instrument_id, market_id_type: InstrumentsIdTypes, class_code: str = ""
    ):
        """GetInstrumentBy
        Метод получения основной информации об инструменте.
        Тело запроса:
        InstrumentRequest https://tinkoff.github.io/investAPI/instruments/#instrumentrequest
        Тело ответа:
        InstrumentResponse https://tinkoff.github.io/investAPI/instruments/#instrumentresponse
        """
        type_num = market_id_type.get_id_type
        with Client(self._token) as client:
            if market_id_type == InstrumentsIdTypes.INSTRUMENT_ID_TYPE_TICKER:
                response_data = client.instruments.get_instrument_by(
                    id_type=InstrumentIdType(type_num),
                    id=instrument_id,
                    class_code=class_code,
                )
            else:
                response_data = client.instruments.get_instrument_by(
                    id_type=InstrumentIdType(type_num), id=instrument_id
                )
        return response_data.instrument

    def get_shares_list(self):
        """Получить список всех акций доступных к торговле"""
        with Client(self._token) as client:
            shares_response = client.instruments.shares()
        instruments_list = shares_response.instruments
        return instruments_list

    def get_bonds_list(self):
        """Получить список всех облигаций доступных к торговле"""
        with Client(self._token) as client:
            bonds_response = client.instruments.bonds()
        instruments_list = bonds_response.instruments
        return instruments_list

    def get_etf_list(self):
        """Получить список всех фондов доступных к торговле"""
        with Client(self._token) as client:
            etfs_response = client.instruments.etfs()
        instruments_list = etfs_response.instruments
        return instruments_list

    def get_futures_list(self):
        """Return futures list"""
        with Client(self._token) as client:
            futures_response = client.instruments.futures()
        instruments_list = futures_response.instruments
        return instruments_list

    def get_futures_by(
        self, future_id: str, market_id_type: InstrumentsIdTypes, class_code: str = ""
    ) -> Future:
        """Returns futures object by future id"""
        type_num = market_id_type.get_id_type
        with Client(self._token) as client:
            if market_id_type == InstrumentsIdTypes.INSTRUMENT_ID_TYPE_TICKER:
                response = client.instruments.future_by(
                    id_type=InstrumentIdType(type_num),
                    id=future_id,
                    class_code=class_code,
                )
            else:
                response = client.instruments.future_by(
                    id_type=InstrumentIdType(type_num), id=future_id
                )
        return response.instrument

    def get_dividends_from_t(self) -> list[Dividend]:
        """T API GetDividends method
        body = GetDividendsRequest
        """

        with Client(self._token) as client:
            get_dividends_response = client.instruments.get_dividends(figi=self.figi,
                                                                      from_=self.from_date,
                                                                      to=self.to_date)
        return get_dividends_response.dividends

    def get_expected_dividends(self) -> list[NormalizedDividendsSchema]:
        """Returns normalized data for future using"""
        result: list[NormalizedDividendsSchema] = []
        div_data = self.get_dividends_from_t()

        for item in div_data:
            value = t_quotation_to_float(item.yield_value)
            last_buy_date = item.last_buy_date
            currency = item.dividend_net.currency
            new_item = NormalizedDividendsSchema(value=value,
                                                 last_buy_date=last_buy_date,
                                                 currency=currency)
            result.append(new_item)

        return result

