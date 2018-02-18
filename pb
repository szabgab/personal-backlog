#!/usr/bin/env python
import argparse
import PersonalBacklog
import re
import readline
import sys
from cmd import Cmd

if sys.version_info.major < 3:
    exit("Python 3 is required")

class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        '''exit the application. Shorthand: x q.'''
        print("Bye")
        return True

    def do_add(self, inp):
        '''
            Add task.
            Will ask for title, estimate, and priority.
        '''
        title = input("Task Title: ")
        estimate = input("Estimate (1, 2, 3, 5, 8, 13, 21, 34, 55): ")
        priority = input("Priority (0 = now, x = max time, some number): ")
        ret = self.pb.add(title, estimate, priority)
        if 'error' in ret:
            print(ret['error'])


    def do_cal(self, inp):
        '''Show calendar
           cal      (default = today)
           cal 0    (today)
           cal 1    (tomorrow)
           cal 2    (2 days from now)
           cal -1   (yesterday)
        '''
        if inp == '':
            inp = '0'
        ret = self.pb.list_calendar(inp)
        if 'error' in ret:
            print(ret['error'])

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)

        print("Unhandled command: {}".format(inp))


def input_with_prefill(prompt, text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result

def main():
    arp = argparse.ArgumentParser()
    arp.add_argument("file", help="Name of the JSON file which is our 'database'")
    args = arp.parse_args()

    cli = MyPrompt()
    cli.pb = PersonalBacklog.PB(args.file)
    cli.cmdloop()

    #     re_delete = '\Ad\s+(\d+)\Z'
    #     re_edit = '\Ae\s+(\d+)\Z'
    #
    #     ret = {}
    #     elif re.search(re_delete, choice):
    #         m = re.search(re_delete, choice)
    #         ret = pb.delete(m.group(1))
    #     elif re.search(re_edit, choice):
    #         m = re.search(re_edit, choice)
    #         entry = pb.get(m.group(1))
    #         if 'error' in entry:
    #             print(entry['error'])
    #         else:
    #             entry["title"] = input_with_prefill("edit title> ", entry["title"])
    #             pb.update(m.group(1), entry)
    #     elif choice == 'lt':
    #         pb.list_todo()
    #     elif choice == 'm':
    #             show_menu()
    #     elif choice == 's':
    #             title = input("Schedule Title: ")
    #             start_date = input("Start Date YYYY-MM-DD 0=today 1=tomorrow: ")
    #             start_time = input("Start time HH:MM: ")
    #             end_date   = input("End Date YYYY-MM-DD ENTER=same as start date")
    #             end_time   = input("End time HH::MM: ")
    #             location   = input("Location (free text): ")
    #             ret = pb.schedule(title, start_date, start_time, end_date, end_time, location)
    #     elif choice == 'x' or choice == 'q':
    #         pb.save()
    #         exit()
    #     elif re.search('\A\d+\s', choice):
    #         pb.process_cli(choice)
    #     else:
    #         print("Invalid choice '{}'".format(choice))
    #
    #     if 'error' in ret:
    #         print(ret['error'])

def show_menu():
    print("d N) Delete")
    print("e N Edit")
    print("lt) List todo")
    print("m) Menu")
    print("s) Schedule")
    print("x) eXit")


if __name__ == '__main__':
    main()

