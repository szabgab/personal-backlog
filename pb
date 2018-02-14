#!/usr/bin/env python
import argparse
import PersonalBacklog

def main():
    arp = argparse.ArgumentParser()
    arp.add_argument("file", help="Name of the JSON file which is our 'database'")
    args = arp.parse_args()
    pb = PersonalBacklog.PB(args.file)

    while True:
        choice = input()
        if choice == 'm':
            show_menu()
        elif choice == 'x':
            pb.save()
            exit()
        else:
            print("Invalid choice '{}'".format(choice))


def show_menu():
    print("m) Menu")
    print("x) eXit")


if __name__ == '__main__':
    main()

