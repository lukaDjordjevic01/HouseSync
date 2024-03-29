import threading
import time

from simulators.device.dht import core as dht
from simulators.device.gsg import core as gsg
from simulators.device.lcd import core as lcd
from simulators.device.ds import core as ds
from simulators.device.dus import core as dus
from simulators.device.pir import core as pir
from simulators.settings.settings import load_settings

stop_event = threading.Event()


def main():
    threads = {}
    settings = load_settings()
    ds.run('DS2', threads, settings['DS2'], stop_event, True)
    dus.run('DUS2', threads, settings['DUS2'], stop_event, True)
    pir.run('DPIR2', threads, settings['DPIR2'], stop_event, True)
    dht.run('GDHT', threads, settings['GDHT'], stop_event, True)
    gsg.run('GSG', threads, settings['GSG'], stop_event, True)
    lcd.run('GLCD', threads, settings['GLCD'], stop_event, True)
    pir.run('RPIR3', threads, settings['RPIR3'], stop_event, True)
    dht.run('RDHT3', threads, settings['RDHT3'], stop_event, True)


if __name__ == '__main__':
    try:
        main()
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        stop_event.set()
