"""
Work Log, being a script to log the work of a small team on csv files

by Miguel de Luis

Started on 260816

"""
#
import csv
import datetime

# constants


WORK_LOG_FILE_NAME = "work_log.csv"

MENU_CHOICES = {"a": "add entry", "f": "search entries", "e": "edit entry", "d": "delete entry", "q": "quit"}

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



def menu():
    """
    Shows the main menu, returns the menu option chosen
    :return: string with the option
    """
    for k in MENU_KEYS:
        print(k, MENU_CHOICES[k].title())


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
