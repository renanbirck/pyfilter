#!/usr/bin/python3

VERSION = "0.0.0"

#from engine import analog, digital

def do_analog_filter():
    pass

def do_digital_filter():
    pass

def main_menu():
    """ The main menu of pyfilter. Used for development before
        we have a GUI. """
    print("This is pyfilter {version}".format(version=VERSION))
    print("Pick the type of filter: ")
    filter_selector()
    return True

def filter_selector():
    choices = {'A': ('Analog', do_analog_filter()),
               'D': ('Digital', do_digital_filter())}
    for possible_choice in choices:
        print("[{}] {}".format(possible_choice, choices[possible_choice][0]))
    option = input("> ")

if __name__ == '__main__':
    main_menu()
