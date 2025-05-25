"""Operation types"""

from enum import Enum


class OperationTypes(Enum):
    """Operation types enum"""

    OPERATION_TYPE_UNSPECIFIED = 0  # (0, 'Тип операции не определён')
    OPERATION_TYPE_INPUT = 1  # (1, 'Пополнение брокерского счёта')
    OPERATION_TYPE_BOND_TAX = 2  # (2, 'Удержание НДФЛ по купонам')
    OPERATION_TYPE_OUTPUT_SECURITIES = 3  # (3, 'Вывод ЦБ')
    OPERATION_TYPE_OVERNIGHT = 4  # (4, 'Доход по сделке РЕПО овернайт')
    OPERATION_TYPE_TAX = 5  # (5, 'Удержание налога')
    OPERATION_TYPE_BOND_REPAYMENT_FULL = 6  # (6, 'Полное погашение облигаций')
    OPERATION_TYPE_SELL_CARD = 7  # (7,' Продажа ЦБ с карты')
    OPERATION_TYPE_DIVIDEND_TAX = 8  # (8, 'Удержание налога по дивидендам')
    OPERATION_TYPE_OUTPUT = 9  # (9, 'Вывод денежных средств')
    OPERATION_TYPE_BOND_REPAYMENT = 10  # (10, 'Частичное погашение облигаций')
    OPERATION_TYPE_TAX_CORRECTION = 11  # (11, 'Корректировка налога')
    OPERATION_TYPE_SERVICE_FEE = (
        12  # (12, 'Удержание комиссии за обслуживание брокерского счёта')
    )
    OPERATION_TYPE_BENEFIT_TAX = 13  # (13, 'Удержание налога за материальную выгоду')
    OPERATION_TYPE_MARGIN_FEE = 14  # (14, 'Удержание комиссии за непокрытую позицию')
    OPERATION_TYPE_BUY = 15  # (15, 'Покупка ЦБ')
    OPERATION_TYPE_BUY_CARD = 16  # (16, 'Покупка ЦБ с карты')
    OPERATION_TYPE_INPUT_SECURITIES = (
        17  # (17, 'Перевод ценных бумаг из другого депозитария')
    )
    OPERATION_TYPE_SELL_MARGIN = 18  # (18, 'Продажа в результате Margin-call')
    OPERATION_TYPE_BROKER_FEE = 19  # (19, 'Удержание комиссии за операцию')
    OPERATION_TYPE_BUY_MARGIN = 20  # (20,' Покупка в результате Margin-call')
    OPERATION_TYPE_DIVIDEND = 21  # (21, 'Выплата дивидендов')
    OPERATION_TYPE_SELL = 22  # (22, 'Продажа ЦБ')
    OPERATION_TYPE_COUPON = 23  # (23, 'Выплата купонов')
    OPERATION_TYPE_SUCCESS_FEE = 24  # (24, 'Удержание комиссии SuccessFee')
    OPERATION_TYPE_DIVIDEND_TRANSFER = 25  # (25, 'Передача дивидендного дохода')
    OPERATION_TYPE_ACCRUING_VARMARGIN = 26  # (26, 'Зачисление вариационной маржи')
    OPERATION_TYPE_WRITING_OFF_VARMARGIN = 27  # (27, 'Списание вариационной маржи')
    OPERATION_TYPE_DELIVERY_BUY = (
        28  # (28, 'Покупка в рамках экспирации фьючерсного контракта')
    )
    OPERATION_TYPE_DELIVERY_SELL = (
        29  # (29, 'Продажа в рамках экспирации фьючерсного контракта')
    )
    OPERATION_TYPE_TRACK_MFEE = (
        30  # (30, 'Комиссия за управление по счёту автоследования')
    )
    OPERATION_TYPE_TRACK_PFEE = (
        31  # (31, 'Комиссия за результат по счёту автоследования')
    )
    OPERATION_TYPE_TAX_PROGRESSIVE = 32  # (32, 'Удержание налога по ставке 15%')
    OPERATION_TYPE_BOND_TAX_PROGRESSIVE = (
        33  # (33, 'Удержание налога по купонам по ставке 15%')
    )
    OPERATION_TYPE_DIVIDEND_TAX_PROGRESSIVE = (
        34  # (34, 'Удержание налога по дивидендам по ставке 15%')
    )
    OPERATION_TYPE_BENEFIT_TAX_PROGRESSIVE = (
        35  # (35, 'Удержание налога за материальную выгоду по ставке 15%')
    )
    OPERATION_TYPE_TAX_CORRECTION_PROGRESSIVE = (
        36  # (36, 'Корректировка налога по ставке 15%')
    )
    OPERATION_TYPE_TAX_REPO_PROGRESSIVE = (
        37  # (37, 'Удержание налога за возмещение по сделкам РЕПО по ставке 15%')
    )
    OPERATION_TYPE_TAX_REPO = (
        38  # (38, 'Удержание налога за возмещение по сделкам РЕПО')
    )
    OPERATION_TYPE_TAX_REPO_HOLD = 39  # (39, 'Удержание налога по сделкам РЕПО')
    OPERATION_TYPE_TAX_REPO_REFUND = 40  # (40, 'Возврат налога по сделкам РЕПО')
    OPERATION_TYPE_TAX_REPO_HOLD_PROGRESSIVE = (
        41  # (41, 'Удержание налога по сделкам РЕПО по ставке 15%')
    )
    OPERATION_TYPE_TAX_REPO_REFUND_PROGRESSIVE = (
        42  # (42, 'Возврат налога по сделкам РЕПО по ставке 15%')
    )
    OPERATION_TYPE_DIV_EXT = 43  # (43, 'Выплата дивидендов на карту')
    OPERATION_TYPE_TAX_CORRECTION_COUPON = 44  # (44, 'Корректировка налога по купонам')
    OPERATION_TYPE_CASH_FEE = 45  # (45, 'Комиссия за валютный остаток')
    OPERATION_TYPE_OUT_FEE = 46  # (46, 'Комиссия за вывод валюты с брокерского счета')
    OPERATION_TYPE_OUT_STAMP_DUTY = 47  # (47, 'Гербовый сбор')
    OPERATION_TYPE_OUTPUT_SWIFT = 50  # (50, 'SWIFT-перевод')
    OPERATION_TYPE_INPUT_SWIFT = 51  # (51, 'SWIFT-перевод')
    OPERATION_TYPE_OUTPUT_ACQUIRING = 53  # (53, 'Перевод на карту')
    OPERATION_TYPE_INPUT_ACQUIRING = 54  # (54, 'Перевод с карты')
    OPERATION_TYPE_OUTPUT_PENALTY = 55  # (55, 'Комиссия за вывод средств')
    OPERATION_TYPE_ADVICE_FEE = 56  # (56, 'Списание оплаты за сервис Советов')
    OPERATION_TYPE_TRANS_IIS_BS = (
        57  # (57, 'Перевод ценных бумаг с ИИС на Брокерский счет')
    )
    OPERATION_TYPE_TRANS_BS_BS = (
        58  # (58, 'Перевод ценных бумаг с одного брокерского счета на другой')
    )
    OPERATION_TYPE_OUT_MULTI = 59  # (59, 'Вывод денежных средств со счета')
    OPERATION_TYPE_INP_MULTI = 60  # (60, 'Пополнение денежных средств со счета')
    OPERATION_TYPE_OVER_PLACEMENT = 61  # (61, 'Размещение биржевого овернайта')
    OPERATION_TYPE_OVER_COM = 62  # (62, 'Списание комиссии')
    OPERATION_TYPE_OVER_INCOME = 63  # (63, 'Доход от оверанайта')
    OPERATION_TYPE_OPTION_EXPIRATION = 64  # (64, 'Экспирация')

    def __init__(self, num):
        self.num = num

    def get_translation(self) -> str:  # pylint: disable=R0915
        """Возвращает тектовый формат операции на русском языке"""

        translate: str = ""

        match self.num:
            case 0:
                translate = "Тип операции не определён"
            case 1:
                translate = "Пополнение брокерского счёта"
            case 2:
                translate = "Удержание НДФЛ по купонам"
            case 3:
                translate = "Вывод ЦБ"
            case 4:
                translate = "Доход по сделке РЕПО овернайт"
            case 5:
                translate = "Удержание налога"
            case 6:
                translate = "Полное погашение облигаций"
            case 7:
                translate = "Продажа ЦБ с карты"
            case 8:
                translate = "Удержание налога по дивидендам"
            case 9:
                translate = "Вывод денежных средств"
            case 10:
                translate = "Частичное погашение облигаций"
            case 11:
                translate = "Корректировка налога"
            case 12:
                translate = "Удержание комиссии за обслуживание брокерского счёта"
            case 13:
                translate = "Удержание налога за материальную выгоду"
            case 14:
                translate = "Удержание комиссии за непокрытую позицию"
            case 15:
                translate = "Покупка ЦБ"
            case 16:
                translate = "Покупка ЦБ с карты"
            case 17:
                translate = "Перевод ценных бумаг из другого депозитария"
            case 18:
                translate = "Продажа в результате Margin-call"
            case 19:
                translate = "Удержание комиссии за операцию"
            case 20:
                translate = "Покупка в результате Margin-call"
            case 21:
                translate = "Выплата дивидендов"
            case 22:
                translate = "Продажа ЦБ"
            case 23:
                translate = "Выплата купонов"
            case 24:
                translate = "Удержание комиссии SuccessFee"
            case 25:
                translate = "Передача дивидендного дохода"
            case 26:
                translate = "Зачисление вариационной маржи"
            case 27:
                translate = "Списание вариационной маржи"
            case 28:
                translate = "Покупка в рамках экспирации фьючерсного контракта"
            case 29:
                translate = "Продажа в рамках экспирации фьючерсного контракта"
            case 30:
                translate = "Комиссия за управление по счёту автоследования"
            case 31:
                translate = "Комиссия за результат по счёту автоследования"
            case 32:
                translate = "Удержание налога по ставке 15%"
            case 33:
                translate = "Удержание налога по купонам по ставке 15%"
            case 34:
                translate = "Удержание налога по дивидендам по ставке 15%"
            case 35:
                translate = "Удержание налога за материальную выгоду по ставке 15%"
            case 36:
                translate = "Корректировка налога по ставке 15%"
            case 37:
                translate = (
                    "Удержание налога за возмещение по сделкам РЕПО по ставке 15%"
                )
            case 38:
                translate = "Удержание налога за возмещение по сделкам РЕПО"
            case 39:
                translate = "Удержание налога по сделкам РЕПО"
            case 40:
                translate = "Возврат налога по сделкам РЕПО"
            case 41:
                translate = "Удержание налога по сделкам РЕПО по ставке 15%"
            case 42:
                translate = "Возврат налога по сделкам РЕПО по ставке 15%"
            case 43:
                translate = "Выплата дивидендов на карту"
            case 44:
                translate = "Корректировка налога по купонам"
            case 45:
                translate = "Комиссия за валютный остаток"
            case 46:
                translate = "Комиссия за вывод валюты с брокерского счета"
            case 47:
                translate = "Гербовый сбор"
            case 50:
                translate = "SWIFT-перевод"
            case 51:
                translate = "SWIFT-перевод"
            case 53:
                translate = "Перевод на карту"
            case 54:
                translate = "Перевод с карты"
            case 55:
                translate = "Комиссия за вывод средств"
            case 56:
                translate = "Списание оплаты за сервис Советов"
            case 57:
                translate = "Перевод ценных бумаг с ИИС на Брокерский счет"
            case 58:
                translate = "Перевод ценных бумаг с одного брокерского счета на другой"
            case 59:
                translate = "Вывод денежных средств со счета"
            case 60:
                translate = "Пополнение денежных средств со счета"
            case 61:
                translate = "Размещение биржевого овернайта"
            case 62:
                translate = "Списание комиссии"
            case 63:
                translate = "Доход от оверанайта"
            case 64:
                translate = "Экспирация"
            case _:
                translate = f"{self.num} тип операции не определен"
        return translate
