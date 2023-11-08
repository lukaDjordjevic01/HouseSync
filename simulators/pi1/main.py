from db import core as db
from dht import core as dht
from dl import core as dl
from dms import core as dms
from ds import core as ds
from dus import core as dus
from pir import core as pir


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
    while True:
        option = menu()
        if option == '1':
            ds.run('ds1')
        elif option == '2':
            dl.run('dl')
        elif option == '3':
            dus.run('dus1')
        elif option == '4':
            db.run('db')
        elif option == '5':
            pir.run('dpir1')
        elif option == '6':
            dms.run('dms')
        elif option == '7':
            pir.run('rpir1')
        elif option == '8':
            pir.run('rpir2')
        elif option == '9':
            dht.run('rdht1')
        elif option == '10':
            dht.run('rdht2')
        else:
            print("Invalid option.")


if __name__ == '__main__':
    main()
