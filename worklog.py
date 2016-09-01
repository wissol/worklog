"""
Work Log, being a script to log the work of a small team on csv files

by Miguel de Luis

Started on 260816

"""
import csv
from ast import literal_eval  # evaluates literal expressions
from datetime import datetime
from sys import exit

# constants

DATE_FORMAT = "%d/%m/%Y"

DEVELOPING = True
WORK_LOG_FILE_NAME = "work_log_developing.csv" if DEVELOPING else "work_log.csv"


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
        self.notes = literal_eval(notes)
        self.task_date = task_date

    def show_task(self):
        """
        Shows the Task on Screen
        :return:
        """
        print("Task Date", self.task_date)
        print("Description", self.description)
        print("Time Spent", self.time_spent)
        print("Notes")
        for note in self.notes:
            print("*", note)
        print("\v")



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


def read_log_file():
    """
    reads the log file into a list of Task objects
    :return: [Task]
    """
    with open(WORK_LOG_FILE_NAME, 'r', newline='') as rf:
        task_log = []
        reader = csv.reader(rf)
        for row in reader:
            this_task = Task(task_date=row[0], description=row[1],
                             time_spent=row[2], notes=row[3])
            task_log.append(this_task)
    return task_log


def show_tasks(task_list, not_found_message="Sorry, not tasks to show"):
    if task_list:
        for task_list_item in task_list:
            task_list_item.show_task()
    else:
        print(not_found_message)

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


def input_date_to_search(validation_message, total_dates):
    """
    Ask for input for the date to choose among those offered. The rationale for this function is that it's much
    faster to type an index number than a date.
    :param validation_message:
    :param total_dates:
    :return:
    """
    show_validation_message(validation_message)

    raw_date_index = input("Please enter the number of the date to search for:> ")

    try:
        raw_date_index = abs(int(raw_date_index))
        # I assume nobody would enter a negative number, except by mistfake and as we are only showing information,
        # there are no major risks
    except ValueError:
        return input_date_to_search("Please enter a _number_ of the date to search for:> ", total_dates)

    if raw_date_index > total_dates:
        return input_date_to_search("Sorry we don't have that date. Choose a smaller number", total_dates)
    else:
        return raw_date_index


# File Functions

def append_task_to_log(task_entry):
    """

    :param task_entry:
    :return:
    """
    with open(WORK_LOG_FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(task_entry)


# Search Functions

def find_dates_with_tasks(tasks):
    dates_with_tasks = []
    for t in tasks:
        if t.task_date not in dates_with_tasks:
            dates_with_tasks.append(t.task_date)
    return dates_with_tasks


def show_dates_with_tasks(tasks):
    dates_with_tasks = find_dates_with_tasks(tasks)
    if dates_with_tasks:
        print("These are the dates that have tasks")
        i = 0
        for d in dates_with_tasks:
            print("{}. {}".format(i, d))
            i += 1
        return dates_with_tasks
    else:
        return None


def find_by_date():
    """

    :return:
    """
    all_tasks = read_log_file()
    found_tasks = []  # [Task]
    # show dates with task
    dates_that_have_tasks = show_dates_with_tasks(all_tasks)
    # ask user for date
    if dates_that_have_tasks:
        date_index = input_date_to_search("", len(dates_that_have_tasks) - 1)
        date_to_search = dates_that_have_tasks[date_index]

        # validate
        # search
        for task_item in all_tasks:
            if task_item.task_date == date_to_search:
                found_tasks.append(task_item)

        show_tasks(found_tasks, not_found_message="Sorry, no tasks found with that date")

            # show a list of date
    else:
        print("Sorry no dates with task have been found.")

def find_by_time_spent():
    """

    :return:
    """
    found_tasks = []
    # ask for user input
    # validate
    time_spent_to_search = input_time_spent("")
    all_tasks = read_log_file()
    # search
    for task_item in all_tasks:
        if int(time_spent_to_search) == int(task_item.time_spent):
            found_tasks.append(task_item)
    # show list of tasks
    show_tasks(found_tasks)

def find_by_exact_search():
    """

    :return:
    """
    found_tasks = []
    string_to_search = input("Enter the exact words that you want to find:> ").strip()
    # ask for user input

    all_tasks = read_log_file()

    # search
    for task_item in all_tasks:
        if string_to_search == task_item.description:
            found_tasks.append(task_item)
        else:
            for note in task_item.notes:
                if string_to_search == note:
                    found_tasks.append(task_item)

    show_tasks(found_tasks)


def find_by_pattern():
    """

    :return:
    """
    # ask for user input
    # validate
    # search
    # show list of tasks


FIND_MENU_FUNCTIONS = {}

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

    append_task_to_log([task_date, task_description, time_spent, task_notes])

    # update worklog file


def search_entries():
    print("search entry")
    search_menu_functions = {"p": find_by_pattern, "d": find_by_date, "x": find_by_exact_search,
                             "t": find_by_time_spent, "m": main}
    search_menu_items = {"p": "find pattern", "d": "find by date", "x": "find by exact match",
                         "t": "find by time spent", "m": "back to main menu"}
    menu(search_menu_functions, search_menu_items)

def edit_entry():
    print("edit_entry")


def delete_entry():
    print("delete entry")


def ask_for_choice(error_message, menu_choices):
    """
    Shows the main menu, returns the menu option chosen
    :return: string with the option
    """
    menu_keys = sorted(menu_choices)

    clear_screen()

    print("\v")

    if error_message:
        print("\a\t*** {} \v".format(error_message))

    for k in menu_keys:
        print(k, menu_choices[k].title())

    print("\v")

    choice = input("Your choice:> ").lower().strip()

    if choice not in menu_keys:
        return ask_for_choice("Sorry, not in menu", menu_choices)
    else:
        return choice


def helper():
    print("To edit or delete an entry you must search it first")


def menu(menu_functions, menu_items):
    """

    :param menu_functions: dictionary ... menu functions
    :param menu_items: dictionary ... contains strings with the menu items
    :return:
    """
    while True:
        user_choice = ask_for_choice("", menu_items)
        print(user_choice)
        menu_functions[user_choice]()


def main():
    main_menu_functions = {"a": add_entry, "f": search_entries, "q": exit, "h": helper}
    main_menu_items = {"a": "add entry", "f": "search entries", "q": "quit", "h": "help"}

    menu(main_menu_functions, main_menu_items)


main()
