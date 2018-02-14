#!/usr/bin/env python


def main():
    while True:
        choice = input()
        if choice == 'm':
            show_menu()
        elif choice == 'x':
            exit()
        else:
            print("Invalid choice '{}'".format(choice))


def show_menu():
    print("m) Menu")
    print("x) eXit")


if __name__ == '__main__':
    main()

