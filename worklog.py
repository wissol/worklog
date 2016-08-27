"""
Work Log, being a script to log the work of a small team on csv files

by Miguel de Luis

Started on 260816

"""
#
from sys import exit

# constants


WORK_LOG_FILE_NAME = "work_log.csv"

MENU_CHOICES = {"a": "add entry", "f": "search entries", "e": "edit entry",
                "d": "delete entry", "q": "quit", "s": "so_stuff"}

"""
MENU_FUNCTIONS = {} will contain the functions called from the menu, yet it's
declared after those functions have been defined
"""

MENU_KEYS = sorted(MENU_CHOICES)

# Classes

class Task():
    def __init__(self, person, description, time_spent, notes, task_date):
        """
        Creates a task entry

        :param description: string ... Task description
        :param time_spent: integer ... Time spent on the task in minutes
        :param notes: [string] Notes ... Can be empty
        :param task_date: datetime ... either supplied by the logger or supplied by the system
        """
        self.description = description
        self.time_spent = time_spent
        self.notes = notes
        self.task_date = task_date


def clear_screen():
    """ Treehouse code from battleship """
    print("\033c", end="")


def do_stuff_a():
    print("stuff a")


def add_entry():
    print("add entry")


def search_entries():
    print("search entry")


def edit_entry():
    print("edit_entry")


def delete_entry():
    print("delete entry")


def quit_program():
    print("quit program")
    exit()


MENU_FUNCTIONS = {"a": add_entry, "f": search_entries, "e": edit_entry,
                  "d": delete_entry, "q": quit_program, "s": do_stuff_a}


def ask_for_choice(error_message):
    """
    Shows the main menu, returns the menu option chosen
    :return: string with the option
    """

    clear_screen()

    if error_message:
        print(error_message)

    for k in MENU_KEYS:
        print(k, MENU_CHOICES[k].title())

    choice = input("Your choice:> ").lower().strip()

    if choice not in MENU_KEYS:
        return ask_for_choice("Sorry, not in menu")
    else:
        return choice


def menu():
    while True:
        user_choice = ask_for_choice("")
        print(user_choice)
        MENU_FUNCTIONS[user_choice]()


# def main():
#     keep_logging = True
#
#     while keep_logging:
#         option = menu()
#         # do_stuff(option)
#
#
# main()

menu()
