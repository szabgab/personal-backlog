#!/usr/bin/env python
import argparse
import PersonalBacklog
import re

def main():
    arp = argparse.ArgumentParser()
    arp.add_argument("file", help="Name of the JSON file which is our 'database'")
    args = arp.parse_args()
    pb = PersonalBacklog.PB(args.file)

    while True:
        choice = input("pb> ")
        if choice == 'a':
                title = input("Task Title: ")
                estimate = input("Estimate (1, 2, 3, 5, 8, 13, 21, 34, 55): ")
                priority = input("Priority (0 = now, x = max time, some number): ")
                pb.add(title, estimate, priority)
        elif re.search('\Ad\s(\d+)\Z', choice):
            m = re.search('\Ad\s(\d+)\Z', choice)
            pb.delete(int(m.group(1)))
        elif choice == 'l':
            pb.list()
        elif choice == 'm':
                show_menu()
        elif choice == 'x':
            pb.save()
            exit()
        else:
            print("Invalid choice '{}'".format(choice))


def show_menu():
    print("m) Menu")
    print("a) Add task")
    print("l) List")
    print("x) eXit")


if __name__ == '__main__':
    main()

