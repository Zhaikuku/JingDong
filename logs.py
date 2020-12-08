import pandas
import logging
import os

def Log(name):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(r"logs\log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

