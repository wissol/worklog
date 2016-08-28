"""
Work Log, being a script to log the work of a small team on csv files

by Miguel de Luis

Started on 260816

"""
# import csv
# from datetime import datetime
from sys import exit

# constants


WORK_LOG_FILE_NAME = "work_log.csv"

MENU_CHOICES = {"a": "add entry", "f": "search entries", "e": "edit entry",
                "d": "delete entry", "q": "quit"}

"""
MENU_FUNCTIONS = {char:function_name} will contain the functions called from the menu, yet it's
declared after those functions have been defined
"""

MENU_KEYS = sorted(MENU_CHOICES)

# Classes

class Task():
    def __init__(self, description, time_spent, notes, task_date):
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
    """ Treehouse code from battleship
    033 = ESC so this is <ESC> + c -> clear terminal
    found on http://askubuntu.com/questions/25077/how-to-really-clear-the-terminal
    """
    print("\033c", end="\v")  # adding some white spacea


def input_task_notes(task_notes):
    """
    Generates a collection with all the notes associated to a task
    :param task_notes: [string]
    :return: [string]
    """
    my_note = input("Add a note for this task, if any or hit enter to end adding notes:> ")
    if not my_note:
        return task_notes
    else:
        task_notes.append(my_note)
        return input_task_notes(task_notes)


def input_time_spent(validation_message):
    """
    Evaluates a string and returns the time spent in minutes
    raw_time_spent: string
    :param validation_message string ... error message
    :return: integer ... total minutes
    """

    if validation_message:
        print("\v\t " + validation_message)

    raw_time_spent = input("Enter time spent, in minutes:> ")
    if raw_time_spent.isnumeric():
        try:
            return int(raw_time_spent)
        except ValueError:
            return input_time_spent(validation_message="\aPlease only whole numbers")
    else:
        return input_time_spent(validation_message="\aPlease use only whole numbers")

def add_entry():
    """
    Adds an entry
    :return:
    """
    task_description = input("Task Description:> ")
    time_spent = input_time_spent("")
    task_notes = input_task_notes([])

    print(task_description)
    print(time_spent)
    print(task_notes)

    # update worklog file


def search_entries():
    print("search entry")


def edit_entry():
    print("edit_entry")


def delete_entry():
    print("delete entry")

MENU_FUNCTIONS = {"a": add_entry, "f": search_entries, "e": edit_entry,
                  "d": delete_entry, "q": exit}


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
