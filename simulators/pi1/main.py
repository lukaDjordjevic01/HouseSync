import threading

import keyboard

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
    option = input("Pick a sumulation: ")
    return option


def main():
    threads = {}
    current_sim = ''
    settings = load_settings()
    while True:
        option = menu()
        if option == '1':
            ds.run('DS1')
        elif option == '2':
            dl.run('DL')
        elif option == '3':
            dus.run('DUS1')
        elif option == '4':
            db.run('DB')
        elif option == '5':
            pir.run('DPIR1')
        elif option == '6':
            dms.run('DMS')
        elif option == '7':
            pir.run('RPIR1')
        elif option == '8':
            pir.run('RPIR2')
        elif option == '9':
            stop_event = threading.Event()
            current_sim = 'RDHT1'
            dht.run('RDHT1', threads, settings['RDHT1'], stop_event)
        elif option == '10':
            stop_event = threading.Event()
            current_sim = 'RDHT2'
            dht.run('RDHT2', threads, settings['RDHT2'], stop_event)
        else:
            print("Invalid option.")


if __name__ == '__main__':
    main()
