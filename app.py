"""
app.py

created by dromakin as 10.10.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201116'

import uvicorn
import multiprocessing as mp

from core.routing import app

from config.settings import HOST, PORT, DEBUG

if __name__ == "__main__":
    if DEBUG is True:
        uvicorn.run("app:app", host=HOST, port=PORT, log_level="trace", debug=DEBUG,
                    workers=1, reload=True)
    else:
        uvicorn.run("app:app", host=HOST, port=PORT, log_level="info",
                    workers=mp.cpu_count())
