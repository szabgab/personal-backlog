#!/usr/bin/env python
import argparse
import PersonalBacklog
import re

def main():
    arp = argparse.ArgumentParser()
    arp.add_argument("file", help="Name of the JSON file which is our 'database'")
    args = arp.parse_args()
    pb = PersonalBacklog.PB(args.file)

    show_menu()
    while True:
        choice = input("pb> ")

        ret = {}
        if choice == 'a':
                title = input("Task Title: ")
                estimate = input("Estimate (1, 2, 3, 5, 8, 13, 21, 34, 55): ")
                priority = input("Priority (0 = now, x = max time, some number): ")
                pb.add(title, estimate, priority)
        elif re.search('\Ad\s+(.+)', choice):
            ret = pb.delete(m.group(1))
        elif choice == 'lt':
            pb.list_todo()
        elif choice == 'lc':
            pb.list_calendar()
        elif choice == 'm':
                show_menu()
        elif choice == 's':
                title = input("Schedule Title: ")
                start_date = input("Start Date YYYY-MM-DD 0=today 1=tomorrow: ")
                start_time = input("Start time HH:MM: ")
                end_date   = input("End Date YYYY-MM-DD ENTER=same as start date")
                end_time   = input("End time HH::MM: ")
                location   = input("Location (free text): ")
                ret = pb.schedule(title, start_date, start_time, end_date, end_time, location)
        elif choice == 'x':
            pb.save()
            exit()
        else:
            print("Invalid choice '{}'".format(choice))

        if 'error' in ret:
            print(ret['error'])

def show_menu():
    print("a) Add task")
    print("d) Delete")
    print("lt) List todo")
    print("lc) List calendar")
    print("m) Menu")
    print("s) Schedule")
    print("x) eXit")


if __name__ == '__main__':
    main()

