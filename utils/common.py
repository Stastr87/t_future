"""common utils"""

from threading import Thread
from traceback import print_exc
from typing import Any

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
