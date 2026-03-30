import enum
import logging


class ToolMode(enum.IntEnum):
    DEVELOPMENT = 0
    RELEASE = 1


def configureLogging(toolMode: ToolMode) -> logging.Logger:
    logger: logging.Logger = logging.getLogger("param_collector")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    streamHandler: logging.StreamHandler = logging.StreamHandler()

    if toolMode == ToolMode.DEVELOPMENT:
        streamHandler.setLevel(logging.DEBUG)
        streamHandler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
            )
        )

    else:
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
        )

    logger.addHandler(streamHandler)

    return logger

