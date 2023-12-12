import threading

from db import core as db
from dht import core as dht
from dl import core as dl
from dms import core as dms
from ds import core as ds
from dus import core as dus
from pir import core as pir
from settings import load_settings


def menu():
    print("1: DS1")
    print("2: DL")
    print("3: DUS1")
    print("4: DB")
    print("5: DPIR1")
    print("6: DMS")
    print("7: RPIR1")
    print("8: RPIR2")
    print("9: RDHT1")
    print("10: RDHT2")
    print("11: All sensor simulators")
    option = input("Pick a sumulation: ")
    return option


def main():
    threads = {}
    settings = load_settings()
    while True:
        option = menu()
        if option == '1':
            stop_event = threading.Event()
            ds.run('DS1', threads, settings['DS1'], stop_event)
        elif option == '2':
            dl.run('DL', settings['DL'])
        elif option == '3':
            stop_event = threading.Event()
            dus.run('DUS1', threads, settings['DUS1'], stop_event)
        elif option == '4':
            db.run('DB', settings['DB'])
        elif option == '5':
            stop_event = threading.Event()
            pir.run('DPIR1', threads, settings['DPIR1'], stop_event)
        elif option == '6':
            stop_event = threading.Event()
            dms.run('DMS', threads, settings['DMS'], stop_event)
        elif option == '7':
            stop_event = threading.Event()
            pir.run('RPIR1', threads, settings['RPIR1'], stop_event)
        elif option == '8':
            stop_event = threading.Event()
            pir.run('RPIR2', threads, settings['RPIR2'], stop_event)
        elif option == '9':
            stop_event = threading.Event()
            dht.run('RDHT1', threads, settings['RDHT1'], stop_event)
        elif option == '10':
            stop_event = threading.Event()
            dht.run('RDHT2', threads, settings['RDHT2'], stop_event)
        elif option == '11':
            stop_event = threading.Event()
            ds.run('DS1', threads, settings['DS1'], stop_event, True)
            dus.run('DUS1', threads, settings['DUS1'], stop_event, True)
            dms.run('DMS', threads, settings['DMS'], stop_event, True)
            pir.run('DPIR1', threads, settings['DPIR1'], stop_event, True)
            pir.run('RPIR1', threads, settings['RPIR1'], stop_event, True)
            pir.run('RPIR2', threads, settings['RPIR2'], stop_event, True)
            dht.run('RDHT1', threads, settings['RDHT1'], stop_event, True)
            dht.run('RDHT2', threads, settings['RDHT2'], stop_event, True)
        else:
            print("Invalid option.")


if __name__ == '__main__':
    main()
