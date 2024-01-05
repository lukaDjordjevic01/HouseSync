import threading
import time

from simulators.device.db import core as db
from simulators.device.dht import core as dht
from simulators.device.dl import core as dl
from simulators.device.dms import core as dms
from simulators.device.ds import core as ds
from simulators.device.dus import core as dus
from simulators.device.pir import core as pir
from simulators.device.rgb import core as rgb
from simulators.settings.settings import load_settings


def main():
    threads = {}
    settings = load_settings()
    stop_event = threading.Event()
    # pir.run('RPIR4', threads, settings['RPIR4'], stop_event, True)
    # dht.run('RDHT4', threads, settings['RDHT4'], stop_event, True)
    db.run('BB', threads, settings['BB'], stop_event, True)
    # B4SD
    # pir.run('BIR', threads, settings['BIR'], stop_event, True)
    rgb.run('BRGB', settings['BRGB'])


if __name__ == '__main__':
    main()
    while True:
        time.sleep(2)
