"""
beacon.py

created by dromakin as 31.12.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201231'

import os
import asyncio
import json
import requests
import datetime
from bleak import BleakScanner

from settings import get_settings
SETTINGS = get_settings()
SERVER_URL = SETTINGS["server_url"]

datadir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')


def get_metres_by_rssi_txpower(rssi, txpower, N=2.3, default_measure_power=-69):
    distance = None

    if txpower == None and rssi <= 0:
        distance = 10 ** ((default_measure_power - rssi) / (10 * N))

    elif txpower == None and rssi >= 0:
        distance = 10 ** ((default_measure_power - (-1 * rssi)) / (10 * N))

    # Filtering anomaly metrics
    elif txpower < 5 and txpower >= 0 and rssi <= 0:
        distance = 10 ** ((default_measure_power - rssi) / (10 * N))

    elif txpower < 5 and txpower >= 0 and rssi >= 0:
        distance = 10 ** ((default_measure_power - (-1 * rssi)) / (10 * N))

    # Normal metrics
    elif rssi <= 0 and txpower <= 0:
        distance = 10 ** ((txpower - rssi) / (10 * N))

    elif rssi >= 0 and txpower >= 0:
        distance = 10 ** (((-1 * txpower) - (-1 * rssi)) / (10 * N))

    elif rssi >= 0 and txpower <= 0:
        distance = 10 ** ((txpower - (-1 * rssi)) / (10 * N))

    elif rssi <= 0 and txpower >= 0:
        distance = 10 ** (((-1 * txpower) - rssi) / (10 * N))

    # while distance > 3:
    #     n = N + 1
    #     distance = get_metres_by_rssi_txpower(rssi, txpower, N=n)

    return distance


def get_metres_from_rssi_by_device(device):
    default_measure_power = -69
    N = 2.3  # 2-4 dbm
    distance = None

    rssi = device.rssi
    txpower = device.details.get('TxPower')

    distance = get_metres_by_rssi_txpower(rssi, txpower)
    return distance


def detection_callback(device, advertisement_data):
    name = device.name
    address = device.address
    rssi = device.rssi

    print(name, address, rssi, end=" ")

    txpower = device.details.get('TxPower')
    print(txpower, end=" ")
    metres = get_metres_from_rssi_by_device(device,)
    print(metres)


async def run(seconds):
    scanner = BleakScanner()
    # scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(seconds)
    await scanner.stop()

    devices = await scanner.get_discovered_devices()
    for d in devices:
        print(d.name, d.rssi, d.details.get('props').get('TxPower'), d.details.get('props').get('UUIDs'), end=" ")
        print(get_metres_by_rssi_txpower(d.rssi, d.details.get('props').get('TxPower')), end=" ")
        print(d.details.get('props'))
        pass


def main():
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(SETTINGS["scanning_seconds"]))


# if __name__ == '__main__':
#     # main()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run())

# Prod functions:


def update_locate_data_by_name(locale_data: dict):
    with open(os.path.join(datadir, "data.json"), 'r') as json_file:
        data = json.load(json_file)

    url_method = "/v1/update_locate_data_by_name"

    data = {
        "name": data['product'],
    }
    data["locate_data"] = json.dumps(locale_data)
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }

    requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
    # response = requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
    # print(response.text)


def send_data_beacon(locale_data: dict):
    with open(os.path.join(datadir, "data.json"), 'r') as json_file:
        data = json.load(json_file)

    url_method = "/v1/add_beacon"

    locale_data["product_name"] = data['product']

    if locale_data["txPower"] is None:
        locale_data["txPower"] = -69

    payload = json.dumps(locale_data)
    headers = {
        'Content-Type': 'application/json'
    }

    requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
    # response = requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
    # print(response.text)


def increase_count_visitors():
    with open(os.path.join(datadir, "data.json"), 'r') as json_file:
        data = json.load(json_file)

    url_method = "/v1/increase_count_visitors"

    data_ = dict()
    data_["name"] = data['product']

    payload = json.dumps(data_)
    headers = {
        'Content-Type': 'application/json'
    }

    requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
    # response = requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
    # print(response.text)


async def find_device():
    # while True:
    scanner = BleakScanner()
    # scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(SETTINGS["scanning_seconds"])
    await scanner.stop()

    devices = await scanner.get_discovered_devices()

    find_flag = False
    visitors = 0

    for d in devices:
        date = datetime.datetime.now().timestamp()
        device_name = d.name
        uuid = d.details.get('props').get('UUIDs')
        if len(uuid) == 0:
            uuid = "No data"
        else:
            uuid = uuid[0]
        address = d.details.get('props').get('Address')
        addressType = d.details.get('props').get('AddressType')
        txPower = d.details.get('props').get('TxPower')
        rssi = d.rssi
        meters = get_metres_by_rssi_txpower(rssi, txPower)

        if meters <= SETTINGS["meters_detection"]:
            locate_data = {
                "date": date,
                "device_name": device_name,
                "uuid": uuid,
                "address": address,
                "addressType": addressType,
                "txPower": txPower,
                "rssi": rssi,
                # "meters": meters,
                "meters": float("{:.2f}".format(meters)),
            }
            update_locate_data_by_name(locale_data=locate_data)
            send_data_beacon(locale_data=locate_data)
            # increase_count_visitors()
            visitors += 1
            find_flag = True

    return visitors, find_flag
