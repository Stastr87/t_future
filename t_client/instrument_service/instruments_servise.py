"""instruments service"""

from datetime import datetime

from tinkoff.invest import Client
from tinkoff.invest.exceptions import RequestError

from env.config import TOKEN
from t_client.schemas.nearest_coupon_schema import NearestCouponSchema
from utils.logger.common_logger import common_logger


class InstrumentsService:
    """Сервис предназначен для получения информации об инструментах"""

    def __init__(self, **kwargs):

        self.set_token()
        self.request_body = kwargs.get("BODY")

    def set_token(self):
        """Sets token attrib"""
        self._token = TOKEN

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

    def get_instrument_by(self, instrument_id):
        """GetInstrumentBy
        Метод получения основной информации об инструменте.
        Тело запроса:
        InstrumentRequest https://tinkoff.github.io/investAPI/instruments/#instrumentrequest
        Тело ответа:
        InstrumentResponse https://tinkoff.github.io/investAPI/instruments/#instrumentresponse
        """
        with Client(self._token) as client:
            response_data = client.instruments.get_instrument_by(
                id_type=1, id=instrument_id
            )
        return response_data

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
