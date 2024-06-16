import logging
import sys


class Colors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


class Logger:
    class Colored:
        def __init__(self, logger):
            self.log = logger


        def in_(self, level, message):
            sys.stdout.write(Colors.GREEN)
            log_record = self.log.makeRecord(
                name=self.log.name,
                level=level,
                fn=sys._getframe(1).f_code.co_filename,
                lno=sys._getframe(1).f_lineno,
                msg=message,
                args=None,
                exc_info=None,
                func=sys._getframe(1).f_code.co_name,
            )
            self.log.handle(log_record)
            sys.stdout.write(Colors.RESET)

        def out(self, level, message):
            sys.stdout.write(Colors.YELLOW)
            log_record = self.log.makeRecord(
                name=self.log.name,
                level=level,
                fn=sys._getframe(1).f_code.co_filename,
                lno=sys._getframe(1).f_lineno,
                msg=message,
                args=None,
                exc_info=None,
                func=sys._getframe(1).f_code.co_name,
            )
            self.log.handle(log_record)
            sys.stdout.write(Colors.RESET)

        def custom(self, level, color, message):
            sys.stdout.write(color)
            log_record = self.log.makeRecord(
                name=self.log.name,
                level=level,
                fn=sys._getframe(1).f_code.co_filename,
                lno=sys._getframe(1).f_lineno,
                msg=message,
                args=None,
                exc_info=None,
                func=sys._getframe(1).f_code.co_name,
            )
            self.log.handle(log_record)
            sys.stdout.write(Colors.RESET)


    def __init__(
        self,
        filename=None,
        enabled=True,
        level=logging.INFO,
    ):
        self.filename = filename
        self.enabled = enabled
        self.level = level
        self.log = self.__set_logger()
        self.log_colored = self.Colored(self.log)
        self.__logger_tutorial()


    def __logger_tutorial(self):
        sys.stdout.write("Connection/data in --> " + Colors.GREEN + "Green\n" + Colors.RESET)
        sys.stdout.write("Connection/data out --> " + Colors.YELLOW + "Yellow\n" + Colors.RESET)

    def __set_logger(self):
        logger = logging.getLogger(__name__)
        if self.enabled:
            logger.setLevel(self.level)

            formatter = logging.Formatter(
                "%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s"
            )

            if self.filename:
                file_handler = logging.FileHandler(self.filename)
                file_handler.setFormatter(formatter)
                self.log.addHandler(file_handler)

            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
        else:
            logging_off = logging.CRITICAL + 1
            logger.setLevel(logging_off)
        return logger
