"""
button_example.py

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
import time

from PIL import Image, ImageDraw, ImageFont

from lib.waveshare_epd import epd2in7
from gpiozero import Button

# import logging
# import traceback

from forex_python.converter import CurrencyCodes

btn1 = Button(5)  # assign each button to a variable
btn2 = Button(6)  # by passing in the pin number
btn3 = Button(13)  # associated with the button
btn4 = Button(19)  #

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

# 264×176
epd = epd2in7.EPD()  # get the display object and assing to epd
epd.init()  # initialize the display
# print("Clear...")  # print message to console (not display) for debugging
epd.Clear(0xFF)


def printToDisplay(currency_code):
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    c = CurrencyCodes()

    draw.line((29, 0, 29, 176), fill=0)

    if currency_code == "RUB":
        draw.rectangle((0, 0, 29, 36), fill=0)
        draw.text((5, 4), c.get_symbol(currency_code), font=font, fill=255)
        draw.text((5, 44), "$", font=font, fill=0)
        draw.text((5, 88), c.get_symbol('EUR'), font=font, fill=0)
        draw.text((5, 132), c.get_symbol('GBP'), font=font, fill=0)

    elif currency_code == "USD":
        draw.rectangle((0, 44, 29, 88), fill=0)
        draw.text((5, 4), c.get_symbol('RUB'), font=font, fill=0)
        draw.text((5, 44), "$", font=font, fill=255)
        draw.text((5, 88), c.get_symbol('EUR'), font=font, fill=0)
        draw.text((5, 132), c.get_symbol('GBP'), font=font, fill=0)

    elif currency_code == "EUR":
        draw.rectangle((0, 88, 29, 132), fill=0)
        draw.text((5, 4), c.get_symbol('RUB'), font=font, fill=0)
        draw.text((5, 44), "$", font=font, fill=0)
        draw.text((5, 88), c.get_symbol(currency_code), font=font, fill=255)
        draw.text((5, 132), c.get_symbol('GBP'), font=font, fill=0)

    elif currency_code == "GBP":
        draw.rectangle((0, 132, 29, 176), fill=0)
        draw.text((5, 4), c.get_symbol('RUB'), font=font, fill=0)
        draw.text((5, 44), "$", font=font, fill=0)
        draw.text((5, 88), c.get_symbol('EUR'), font=font, fill=0)
        draw.text((5, 132), c.get_symbol(currency_code), font=font, fill=255)

    epd.display(epd.getbuffer(image))


# Handle button presses
# param Button (passed from when_pressed)
def handleBtnPress(btn):
    # get the button pin number
    pinNum = btn.pin.number

    # python hack for a switch statement. The number represents the pin number and
    # the value is the message we will print
    switcher = {
        5: "RUB",
        6: "USD",
        13: "EUR",
        19: "GBP"
    }

    # get the string based on the passed in button and send it to printToDisplay()
    currency_code = switcher.get(btn.pin.number, "Error")

    # c = CurrencyCodes()
    # msg = f"{currency_code}: {c.get_symbol(currency_code)}"
    # msg = c.get_symbol(currency_code)

    printToDisplay(currency_code)


# tell the button what to do when pressed

def main():
    while True:
        btn1.when_pressed = handleBtnPress
        btn2.when_pressed = handleBtnPress
        btn3.when_pressed = handleBtnPress
        btn4.when_pressed = handleBtnPress


if __name__ == '__main__':
    main()
