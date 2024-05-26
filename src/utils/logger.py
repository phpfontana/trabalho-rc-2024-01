import logging


class Logger:
    def __init__(
        self,
        filename=".app.log",
        debug_mode=False,
        level=logging.DEBUG,
    ):
        self.logger = logging.getLogger(__name__)
        if debug_mode:
            self.logger.setLevel(level)

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
            )

            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
        else:
            logging_off = logging.CRITICAL + 1
            self.logger.setLevel(logging_off)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
