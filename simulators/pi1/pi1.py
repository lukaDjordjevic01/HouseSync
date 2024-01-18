import threading
import time

from simulators.device.db import core as db
from simulators.device.dht import core as dht
from simulators.device.dl import core as dl
from simulators.device.dms import core as dms
from simulators.device.ds import core as ds
from simulators.device.dus import core as dus
from simulators.device.pir import core as pir
from simulators.settings.settings import load_settings


def main():
    threads = {}
    settings = load_settings()
    stop_event = threading.Event()
    ds.run('DS1', threads, settings['DS1'], stop_event, True)
    dl.run('DL', threads, settings['DL'], stop_event, True)
    dus.run('DUS1', threads, settings['DUS1'], stop_event, True)
    dms.run('DMS', threads, settings['DMS'], stop_event, True)
    pir.run('DPIR1', threads, settings['DPIR1'], stop_event, True)
    pir.run('RPIR1', threads, settings['RPIR1'], stop_event, True)
    pir.run('RPIR2', threads, settings['RPIR2'], stop_event, True)
    dht.run('RDHT1', threads, settings['RDHT1'], stop_event, True)
    dht.run('RDHT2', threads, settings['RDHT2'], stop_event, True)
    db.run('DB', threads, settings['DB'], stop_event, True)


if __name__ == '__main__':
    main()
    while True:
        time.sleep(2)
