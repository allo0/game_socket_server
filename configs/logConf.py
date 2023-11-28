import logging


class LogConfig:
    LOGGER_NAME: str = "miami_server"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - {%(module)s->%(funcName)s:%(lineno)d} - %(message)s"
    LOG_LEVEL: int = 0

    """
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50
    """


def configure_logging():
    logging.basicConfig(
        format=LogConfig.LOG_FORMAT,
        style='%',
        level=LogConfig.LOG_LEVEL,
        handlers=
        [
            logging.FileHandler("miami_server.log", mode='w', encoding='utf-8', ),
            logging.StreamHandler()
        ]
    )


logger = logging.getLogger(LogConfig.LOGGER_NAME)
