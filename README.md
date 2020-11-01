# BLE
Course project: Электронные ценники

## Description

Этот модуль полностью посвящен работе с Raspberry Pi A+.

Этот модуль визуализирует ценники на основе файла [data.json](./data/data.json).

Сами настройки ценника можно найти в файле [settings.json](./settings/settings.json).

## [data.json](./data/data.json)

Этот json должен будет загружаться post методом в данную папку перед запуском самого ценника.
Если файл пришел во время работы ценника, то он должен перезагрузиться и обновить данные на экране.

TODO: необходимо поднять сервер REST API запросов для этого.
Сервер - raspberry pi, а клиент - ноутбук админа.
Можно также рассмотреть ситуацию наоборот: много клиентов raspberry pi и 1 сервер.
Минусы данного подхода: необходима связь wifi у raspberry pi для обнаружения его внутри сети.

Пример:
```
{
  "product": "Product Name",
  "RUB": 1000,
  "USD": 12.65,
  "EUR": 10.81,
  "GBP": 9.75
}
```

## [settings.json](./settings/settings.json)
Пример:
```
{
  "default_currency": "RUB",
  "default_buttons_currency": [
    "RUB",
    "USD",
    "EUR",
    "GBP"
  ],
  "version": "1604248006.302461"
}
```

default_currency - стандартная валюта, которая высвечивается до нажатий кнопок.

default_buttons_currency - это названия валют, которые используются на кнопках.

version - версия настроек, дата в timestamp.

## Запуск ценника
1. Create env on raspberry pi
1. ```pip install -r requirements.txt```
1. Connect remote debugger using pycharm
1. Run test: ```python3 epd_2in7_test.py```
1. ```python3 display.py```
1. profit = )

## Links:
1. [How to calculate distance using rssi: My code](https://repl.it/@DmitriyRomakin/DistanceiBeacon)
1. [2.7inch e-Paper HAT: tutorial](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT)
1. [epd-library-python: demo files](https://github.com/soonuse/epd-library-python/tree/master/2.7inch_e-paper/raspberrypi/python)
1. [e-Paper](https://github.com/waveshare/e-Paper)
1. [E-Ink для Raspberry Pi 2,7](http://wiki.amperka.ru/products:display-e-ink-paper-hat-2n7in#%D1%81%D1%85%D0%B5%D0%BC%D0%B0_%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F)
1. [A simple interface to GPIO devices with Raspberry Pi.](https://github.com/gpiozero/gpiozero)
1. [Getting started with the Waveshare 2.7" ePaper HAT on Raspberry Pi](https://dev.to/ranewallin/getting-started-with-the-waveshare-2-7-epaper-hat-on-raspberry-pi-41m8)
1. [Example project: Clock + weather + AQI + traffic - on Raspberry Pi & e-paper](https://github.com/pskowronek/epaper-clock-and-more)
1. [Test Waveshare ePaper (eInk) 2.7” inch SPI screen on Raspberry Pi in Python](https://diyprojects.io/test-waveshare-epaper-eink-2-7-spi-screen-raspberry-pi-python/#.X56Wu1MzadY)

## Helpful methods for remote development code in Raspberry Pi using pycharm
1. [Configure an interpreter using SSH](https://www.jetbrains.com/help/pycharm/configuring-remote-interpreters-via-ssh.html)
1. [Tutorial: Deployment in PyCharm](https://www.jetbrains.com/help/pycharm/deployment-in-PyCharm.html#dowloading)

