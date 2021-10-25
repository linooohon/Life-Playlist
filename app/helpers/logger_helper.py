import logging
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file_list = [
    "dashboard_update.log",
    "send_soulmate_email.log",
    "userplaylist_update.log",
    "thesoundsofspotifyplaylist_update_to_bigquery.log",
    ]

def setup_logger(name, log_file, level=logging.INFO):
    """To setup multiple logger

    Args:
        name (str): logger name
        log_file (str): logger file name
        level: logging level
    """

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def clean_logger():
    for log_file in log_file_list:
        with open(f"{log_file}", "w+") as f:
            f.write("\n New Month Start")
