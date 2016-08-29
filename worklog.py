"""
Work Log, being a script to log the work of a small team on csv files

by Miguel de Luis

Started on 260816

"""
import csv
from datetime import datetime
from sys import exit

# constants

DATE_FORMAT = "%d/%m/%Y"

DEVELOPING = True
WORK_LOG_FILE_NAME = "work_log_developing.csv" if DEVELOPING else "work_log.csv"

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



# Auxiliary Functions

def clear_screen():
    """ Treehouse code from battleship
    033 = ESC so this is <ESC> + c -> clear terminal
    found on http://askubuntu.com/questions/25077/how-to-really-clear-the-terminal
    """
    print("\033c", end="\v")  # adding some white spacea


def get_task_date():
    """
    generates date from datetime
    :return: string ... "dd/mm/yyyy"
    """
    return datetime.today().strftime(DATE_FORMAT)


def show_validation_message(validation_message):
    if validation_message:
        print("\a\v\t " + validation_message)

# User Input and Validation

def input_task_date(validation_message):
    """
    Ask user for task date, validates,
    :return: string ... dd/mm/yyyy
    """

    show_validation_message(validation_message)

    raw_task_date = input("Please enter the date for this task as dd/mm/yyyy or press enter for today:> ") \
        .replace(" ", "").strip()

    if raw_task_date:
        try:
            datetime.strptime(raw_task_date, DATE_FORMAT)
            # The idea is to use strptime to raise a Value Error if the string provided does not conform to
            # Date_Format
            return raw_task_date
        except ValueError:
            return input_task_date("Please enter the date as dd/mm/yyyy or just press enter for today")
    else:
        return datetime.strftime(datetime.today(), DATE_FORMAT)


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

    show_validation_message(validation_message)

    raw_time_spent = input("\vEnter time spent on task, in minutes:> ")
    if raw_time_spent.isnumeric():
        try:
            return int(raw_time_spent)
        except ValueError:
            return input_time_spent(validation_message="\aPlease only whole numbers")
    else:
        return input_time_spent(validation_message="\aPlease use only whole numbers")


# File Functions

def append_task_to_log(task_entry):
    """

    :param task_entry:
    :return:
    """
    print(task_entry)
    with open(WORK_LOG_FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(task_entry)


# Command Functions

def add_entry():
    """
    Adds an entry
    :return:
    """
    task_description = input("Task Description:> ")
    time_spent = input_time_spent("")
    task_notes = input_task_notes([])
    task_date = input_task_date("")

    print(task_description)
    print(time_spent)
    print(task_notes)

    append_task_to_log([task_date, task_description, time_spent, task_notes])

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
