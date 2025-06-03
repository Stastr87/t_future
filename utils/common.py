"""common utils"""

from json import JSONDecodeError, load
from threading import Thread
from traceback import print_exc
from typing import Any

from utils.exceptions import UtilException
from utils.logger.common_logger import common_logger


class CustomThread(Thread):
    """Customization of Thread class to run and handle possible exceptions"""

    def __init__(
        self,
        name: str,
        func: Any,
        *args,
        hello_msg: str = "",
        daemon: bool = False,
        **kwargs,
    ):
        super().__init__(name=name)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.test_exception = False
        self.daemon = daemon
        self.msg = hello_msg

    def run(self) -> None:
        """run method"""

        if self.msg:
            common_logger.info("%s: %s", self.func.__name__, self.msg)
        else:
            common_logger.info("%s started", self.func.__name__)

        try:
            self.func(**self.kwargs)

        except Exception as error:  # pylint: disable=W0718
            self.test_exception = True
            common_logger.error(str(error), exc_info=True)
            print_exc()

    def join(self, timeout: float = None) -> None:
        """Join method"""

        super().join(timeout)
        common_logger.info("%s Thread join method.", self.name)


def display_result(func):
    """Deco for print into terminal"""

    def wrapper(*args, **kwargs):
        """Wrapper func"""
        result = func(*args, **kwargs)
        if result:
            print(result)

    return wrapper


def load_json_from_file(file_path: str) -> Any:
    """Load json data from file"""

    with open(file_path, encoding="utf-8") as file:
        try:
            result = load(file)
        except JSONDecodeError as error:
            raise UtilException(
                f"Файл {file_path} содержит ошибки в структуре json"
            ) from error

    return result
