"""
display.py

created by dromakin as 01.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201101'

import datetime
import sys
import os
import requests
import time
import json
import asyncio

from PIL import Image, ImageDraw, ImageFont

from lib.waveshare_epd import epd2in7
from gpiozero import Button

# import logging
# import traceback

# Beacon
from beacon_module import beacon

from settings import get_settings
from currency import get_symbol, check_price, check_currency

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
settingsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings')

SETTINGS = get_settings()
BUTTONS = SETTINGS["default_buttons_currency"]
DEFAULT_CURRENCY = SETTINGS["default_currency"]
SERVER_URL = SETTINGS["server_url"]

btn1 = Button(5)  # assign each button to a variable
btn2 = Button(6)  # by passing in the pin number
btn3 = Button(13)  # associated with the button
btn4 = Button(19)  #


class DisplayManager:

    def __init__(self, data: dict = None, currency_code: str = None) -> None:
        # 264×176
        self.epd = epd2in7.EPD()  # get the display object and assing to epd
        self.epd.init()  # initialize the display
        self.epd.Clear(0xFF)

        self.product = data['product']
        self.price = check_price(data["currencies"][currency_code])
        self.currency = check_currency(currency_code)
        self.currency_code = get_symbol(self.currency)
        super().__init__()

    def clear_display(self):
        self.epd.init()
        self.epd.Clear(0xFF)

    def update_on_start(self):
        url_method = "/v1/update_turn_by_pi"

        payload = json.dumps({"name": self.product})
        headers = {
            'Content-Type': 'application/json'
        }

        requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
        # response = requests.request("POST", "http://" + SERVER_URL + url_method, headers=headers, data=payload)
        # print(response.text)

    def printToDisplay(self):
        image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        # font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        # print product and price
        draw.text((72, 45), self.product, font=font, fill=0)
        draw.line((29, 88, 264, 88), fill=0)
        draw.text((100, 120), f"{self.price} {self.currency_code}", font=font, fill=0)

        draw.line((29, 0, 29, 176), fill=0)

        if self.currency == BUTTONS[0]:
            draw.rectangle((0, 0, 29, 36), fill=0)
            draw.text((5, 4), get_symbol(self.currency), font=font, fill=255)
            draw.text((5, 44), get_symbol(BUTTONS[1]), font=font, fill=0)
            draw.text((5, 88), get_symbol(BUTTONS[2]), font=font, fill=0)
            draw.text((5, 132), get_symbol(BUTTONS[3]), font=font, fill=0)

        elif self.currency == BUTTONS[1]:
            draw.rectangle((0, 44, 29, 88), fill=0)
            draw.text((5, 4), get_symbol(BUTTONS[0]), font=font, fill=0)
            draw.text((5, 44), get_symbol(self.currency), font=font, fill=255)
            draw.text((5, 88), get_symbol(BUTTONS[2]), font=font, fill=0)
            draw.text((5, 132), get_symbol(BUTTONS[3]), font=font, fill=0)

        elif self.currency == BUTTONS[2]:
            draw.rectangle((0, 88, 29, 132), fill=0)
            draw.text((5, 4), get_symbol(BUTTONS[0]), font=font, fill=0)
            draw.text((5, 44), get_symbol(BUTTONS[1]), font=font, fill=0)
            draw.text((5, 88), get_symbol(self.currency), font=font, fill=255)
            draw.text((5, 132), get_symbol(BUTTONS[3]), font=font, fill=0)

        elif self.currency == BUTTONS[3]:
            draw.rectangle((0, 132, 29, 176), fill=0)
            draw.text((5, 4), get_symbol(BUTTONS[0]), font=font, fill=0)
            draw.text((5, 44), get_symbol(BUTTONS[1]), font=font, fill=0)
            draw.text((5, 88), get_symbol(BUTTONS[2]), font=font, fill=0)
            draw.text((5, 132), get_symbol(self.currency), font=font, fill=255)

        self.epd.display(self.epd.getbuffer(image))


def handleBtnPress(btn):
    switcher = {
        5: BUTTONS[0],
        6: BUTTONS[1],
        13: BUTTONS[2],
        19: BUTTONS[3]
    }

    # get the string based on the passed in button and send it to printToDisplay()
    currency_code = switcher.get(btn.pin.number)

    with open(os.path.join(datadir, "data.json"), 'r') as json_file:
        data = json.load(json_file)

    d = DisplayManager(data=data, currency_code=currency_code)
    d.printToDisplay()


def test():
    with open(os.path.join(datadir, "data.json"), 'r') as json_file:
        data = json.load(json_file)

    d = DisplayManager(data=data, currency_code=DEFAULT_CURRENCY)
    d.update_on_start()
    d.printToDisplay()

    while True:
        btn1.when_pressed = handleBtnPress
        btn2.when_pressed = handleBtnPress
        btn3.when_pressed = handleBtnPress
        btn4.when_pressed = handleBtnPress


def main():
    with open(os.path.join(datadir, "data.json"), 'r') as json_file:
        data = json.load(json_file)

    d = DisplayManager(data=data, currency_code=DEFAULT_CURRENCY)
    d.update_on_start()
    d.printToDisplay()

    loop = asyncio.get_event_loop()

    while loop.run_until_complete(beacon.find_device()):
        btn1.when_pressed = handleBtnPress
        btn2.when_pressed = handleBtnPress
        btn3.when_pressed = handleBtnPress
        btn4.when_pressed = handleBtnPress

    d.clear_display()
    beacon.increase_count_visitors()


if __name__ == '__main__':
    while True:
        loop = asyncio.get_event_loop()
        visitors, answer = loop.run_until_complete(beacon.find_device())
        if answer:
            for i in range(visitors):
                beacon.increase_count_visitors()
            main()
