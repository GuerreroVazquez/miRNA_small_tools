import logging


logger = logging.getLogger()

logger = logging.getLogger("databaseAnalysis_log")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")
# Alternative formatting available on python 3.2+:
# formatter = logging.Formatter(
#     "{asctime} {threadName:>11} {levelname} {message}", style='{')

# Log to file
filehandler = logging.FileHandler("debug.txt", "w")
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

# Log to stdout too
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)