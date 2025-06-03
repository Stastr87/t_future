"""Instruments types"""

from enum import Enum


class InstrumentsIdTypes(Enum):
    """Instruments types enum"""

    INSTRUMENT_ID_UNSPECIFIED = (0, "Значение не определено")
    INSTRUMENT_ID_TYPE_FIGI = (1, "Классификация по figi")
    INSTRUMENT_ID_TYPE_TICKER = (2, "Ticker")
    INSTRUMENT_ID_TYPE_UID = (3, "Уникальный идентификатор")
    INSTRUMENT_ID_TYPE_POSITION_UID = (4, "Идентификатор позиции")

    def __init__(self, id_type: int, ru_str: str):
        self.id_type = id_type
        self.ru_str = ru_str

    @property
    def get_ru_str(self) -> str:  # pylint: disable=R0915
        """Возвращает тектовый формат операции на русском языке"""
        return self.ru_str

    @property
    def get_id_type(self) -> int:  # pylint: disable=R0915
        """Возвращает id операции"""
        return self.id_type

    @classmethod
    def get_name_by_type_id(cls, enum_id):
        """Returns enum.name by 1st element in enum.value which type is tuple"""
        for item in cls:
            if enum_id == item.value[0]:
                return item.name
        raise ValueError(f"{enum_id} is not a valid id for {cls.__name__}")


# print(InstrumentsTypes.INSTRUMENT_ID_TYPE_FIGI.get_id_type)
