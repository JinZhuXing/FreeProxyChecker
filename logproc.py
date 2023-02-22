import logging

# configuration logger with utf-8
def configure_logger(logger, log_file, log_level):
    # set log format
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(LOG_FORMAT)

    # set log handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # set log level
    logger.setLevel(log_level)

    # add handler to logger
    logger.addHandler(file_handler)


# initialize log
def init_logger(log_file):
    configure_logger(logging.getLogger(), log_file, logging.INFO)

# write log to file and print
def info_logger(log_message, color = ''):
    logging.info(log_message)
    if (color != ''):
        print(color + log_message + '\033[0m')
    else:
        print(log_message)

def error_logger(log_message):
    logging.critical(log_message)
    print(log_message)