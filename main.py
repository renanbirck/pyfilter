#!/usr/bin/python3

VERSION = "0.0.0"

from engine import calculation


def main_menu():
    """ The main menu of pyfilter. Used for development before
        we have a GUI. """
    print("This is pyfilter {version}".format(version=VERSION))
    return True

if __name__ == '__main__':
    main_menu()
