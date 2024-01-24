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
from simulators.device.b4sd import core as b4sd
from simulators.device.ir_receiver import core as ir_receiver

stop_event = threading.Event()


def main():
    threads = {}
    settings = load_settings()
    pir.run('RPIR4', threads, settings['RPIR4'], stop_event, True)
    dht.run('RDHT4', threads, settings['RDHT4'], stop_event, True)
    db.run('BB', threads, settings['BB'], stop_event, True)
    b4sd.run('B4SD', threads, settings['B4SD'], stop_event, True)
    pir.run('BIR', threads, settings['BIR'], stop_event, True)
    rgb.run('BRGB', threads, settings['BRGB'], stop_event, True)
    ir_receiver.run('RECEIVER', threads, settings['RECEIVER'], stop_event, True)


if __name__ == '__main__':
    try:
        main()
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        stop_event.set()
