import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET",
            RESET_SEQ).replace(
            "$BOLD",
            BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': MAGENTA,
    'FATAL': MAGENTA,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLOR_SEQ % (
                30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class ColoredLogger(logging.Logger):
    format = "[%(levelname)-16s]  %(message)s  ($BOLD%(filename)s$RESET:%(lineno)d)"
    color_format = format.replace(
        "$RESET",
        RESET_SEQ).replace(
        "$BOLD",
        BOLD_SEQ)

    def __init__(self, name):
        logging.Logger.__init__(self, 'crawler', logging.DEBUG)
        color_formatter = ColoredFormatter(self.color_format)
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)


def initLogger():
    logging.getLogger("urllib3.connection").setLevel(logging.WARNING)
    logging.getLogger("urllib3.response").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("urllib3.poolmanager").setLevel(logging.WARNING)
    logging.getLogger("urllib3.contrib.pyopenssl").setLevel(logging.WARNING)
    logging.getLogger("urllib3.contrib").setLevel(logging.WARNING)
    logging.getLogger("socks").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("pyasn1").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.setLoggerClass(ColoredLogger)
