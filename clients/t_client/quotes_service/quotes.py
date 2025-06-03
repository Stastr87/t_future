"""Сервис котировок"""

import os
import shelve
from pathlib import Path

from tinkoff.invest import (
    Client,
    GetCandlesResponse,
    GetLastPricesResponse,
    InstrumentClosePriceRequest,
)

from clients.t_client.quotes_service.schema.schema import FigiListSchema
from env.config import TOKEN


class MarketDataService:
    """MarketDataService
    Данный сервис предназначен для получения различной (в т.ч. исторической)
    биржевой информации. Существует два варианта взаимодействия с сервисом
    котировок:

    * Unary-методы — данный вариант следует использовать в случаях,
    когда не требуется оперативность получения информации или для загрузки
    исторических данных. Существует ограничение на количество запросов в минуту,
    подробнее: Лимитная политика.

    * Bidirectional-stream — используется для получения биржевой информации в
    реальном времени с минимально возможными задержками. Для работы со
    стрим-соединениями также существуют ограничения, согласно лимитной политике.

    * Server-side-stream — используется для получения биржевой информации в реальном
    времени с минимально возможными задержками. В отличие от MarketDataStream в
    данном стриме передаётся объект, содержащий все типы подписок.
    ServerSideStream необходим для корректной трансляции маркетдаты в браузерные
    клиенты по gRPC-web, который не поддерживает bidirection стримы.
    Для работы со стрим-соединениями также существуют ограничения,
    согласно лимитной политике.

    Важно! В сервисе TINKOFF INVEST API для отображения цен облигаций и фьючерсов
    используются пункты. Для облигаций один пункт равен одному проценту номинала
    облигации. Для расчёта реальной стоимости фьючерса можно воспользоваться формулой:

    price / min_price_increment * min_price_increment_amount

    Формулы расчета реальной стоимости инструментов в валюте
    price — текущая котировка ценной бумаги;
    nominal — номинал облигации;
    min_price_increment — шаг цены;
    min_price_increment_amount — стоимость шага цены;
    lot - лотность инструмента.

    Акции
    price * lot

    Облигации
    Пункты цены для котировок облигаций представляют собой проценты номинала облигации.
    Для пересчёта пунктов в валюту можно воспользоваться формулой:
    price / 100 * nominal
    price / 100 * nominal + current_nkd Используется для подсчета с учетом НКД
    НКД - накопленный купонный доход. Может возвращаться в параметрах current_nkd или aci_value.

    Валюта
    price * lot / nominalc
    Важно! При торговле валютой необходимо учитывать,
    что такие валюты как Иена, Армянский драм и Тенге имеют nominal = 100

    Фьючерсы
    Стоимость фьючерсов так же предоставляется в пунктах,
    для пересчёта можно воспользоваться формулой:

    price / min_price_increment * min_price_increment_amount

    """

    def __init__(self):
        self.token = TOKEN

    def get_close_prices_request(self, instrument_figi_id):
        """GetClosePricesRequest
        Запрос цен закрытия торговой сессии по инструментам.

        Возвращает Цены закрытия торговой сессии по инструментам.
        Field            Type                                            Description
        close_prices     Массив объектов InstrumentClosePriceResponse    Массив по инструментам.

        В качестве аргумента Массив объектов InstrumentClosePriceRequest
        https://tinkoff.github.io/investAPI/marketdata/#instrumentclosepricerequest
        """

        close_price_req_obj = InstrumentClosePriceRequest("figi")
        close_price_req_obj.instrument_id = instrument_figi_id

        with Client(self.token) as client:
            response = client.market_data.get_close_prices(
                instruments=[close_price_req_obj]
            )
        return response

    def get_quotes_by_figi(self, body: FigiListSchema) -> GetLastPricesResponse:
        """GetLastPrices
        Возвращает которивки инструментов по переданному листу figi
        """

        with Client(self.token) as client:
            response_data_list = client.market_data.get_last_prices(figi=body.figi_list)

        return response_data_list

    def update_local_currencies(self):
        """Обновляет котировки валюты в локальном файле
        для прикладных нужд по следующему списку:
        "BBG0013HGFT4" - USD/RUB
        """

        figi_list = ["BBG0013HGFT4"]
        with Client(self.token) as client:
            last_prices_list = client.market_data.get_last_prices(figi=figi_list)

        last_price_json_list = []
        for item in last_prices_list.last_prices:
            item_price = str(f"{item.price.units},{item.price.nano}")
            last_price_json_item = {"figi": item.figi, "price": item_price}
            last_price_json_list.append(last_price_json_item)

        # Сохраним данные во временном файле
        # Используется библиотека pathlib для
        # корректного присвоения путей в разных ОС
        temp_dir = Path("temp_data")
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)
        temp_file = temp_dir / "temp"
        shelve_file = shelve.open(temp_file)
        shelve_file["currencies"] = last_price_json_list
        shelve_file.close()

    def get_candle_array(self, body) -> GetCandlesResponse:
        """
        Метод запроса исторических свечей по инструменту.
        Тело запроса:
        GetCandlesRequest https://tinkoff.github.io/investAPI/marketdata/#getcandlesrequest
        Тело ответа:
        GetCandlesResponse https://tinkoff.github.io/investAPI/marketdata/#getcandlesresponse
        Возвращает массив объектов:
        HistoricCandle https://tinkoff.github.io/investAPI/marketdata/#historiccandle
        """

        with Client(self.token) as client:
            candle_array = client.market_data.get_candles(
                figi=body.figi,
                from_=body.from_,
                to=body.to,
                interval=body.interval,
                instrument_id=body.instrument_id,
            )
        return candle_array
