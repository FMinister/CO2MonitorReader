from CO2Meter import *
import configparser
from datetime import datetime
import json
import logging
import requests
import time


logging.basicConfig(
    filename="./logs/reader_log.log", encoding="utf-8", level=logging.DEBUG
)
logger = logging.getLogger("co2ReaderLogger")

config = configparser.ConfigParser()
config.read("./app/co2Reader.ini")


def start():
    """
    Start reading from sensor.
    Little annotation: Getting the right hidraw-path works in Linux with: ls -la /dev/hidraw*
    :return: sensor-data (co2- and temperature-data)
    """
    logger.debug("Started.")
    sensor = CO2Meter("/dev/hidraw16")

    return sensor


def read_sensor_data(sensor):
    """
    Getting the data from CO2Meter, preparing it for further functions
    :param self: co2- and temperature-value from CO2Meter
    :return: data (co2- and temperature-value as list), co2-value and temperature-value
    """
    while True:
        time.sleep(60)
        data = sensor.get_data()
        if bool(data):
            try:
                send_data_to_API(data)
            except:
                logger.error(f"Failed to send data: {data}.")


def send_data_to_API(sensor_data):
    """
    Sending the sensor_data to the API.
    :param sensor_data: co2- and temperature-value from CO2Meter
    """
    data = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Temp": sensor_data["temperature"],
        "CO2": sensor_data["co2"],
    }

    try:
        url = config["API"]["URL"]
    except:
        logger.error(
            "Can' reach ini-file. Setting url to http://172.30.0.2:8000/api/postData ."
        )
        url = "http://172.30.0.2:8000/api/postData"

    try:
        requests.post(url, json.dumps(data))
    except:
        logger.error(f"Error, could not send data: {data} to url: {url}")


if __name__ == "__main__":
    sensor = start()
    read_sensor_data(sensor)
