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


# Classes

class Task():
    def __init__(self, description, time_spent, notes, task_date):
        """
        Creates a task entry

        :param description: string ... Task description
        :param time_spent: integer ... Time spent on the task in minutes
        :param notes: string Notes ... Can be empty
        :param task_date: datetime ... either supplied by the logger or supplied by the system
        """
        self.description = description
        self.time_spent = time_spent
        self.notes = notes
        self.task_date = task_date

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def show_task(self):
        """
        Shows the Task on Screen
        :return: None
        """
        print("\v")
        print("-" * 12)
        print("Task Date:", self.task_date)
        print("Description:", self.description)
        print("Time Spent:", self.time_spent)
        print("\v")
        if self.notes:
            print("Notes")
            print("----")
            print(self.notes)
        else:
            print("Task without notes")
        print("")
        print("=" * 12)
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
    generates today's date from system clock
    :return: string ... "dd/mm/yyyy"
    """
    return datetime.today().strftime(DATE_FORMAT)


def show_validation_message(validation_message):
    """
    Shows a validation message, if any
    :param validation_message: string
    :return:
    """
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
    if not task_log:
        print("\n\a\t*** Sorry the log file seems empty. *** \n")
    return task_log


def show_tasks(task_list, not_found_message="Sorry, not tasks to show.\v"):
    """
    Show the tasks of a task list, allows navigation, returns selected task if any
    :param task_list: [Task]
    :param not_found_message: string
    :return: Task ... selected task, if any or None
    """

    def show_next_task(task_index):
        """
        Shows next task, and add pagination
        :param task_index: integer
        :return: integer ... updated task integer
        """
        task_index += 1
        try:
            task_list[task_index].show_task()
            print("Task {} of {}\n".format(task_index + 1, len(task_list)))
            return task_index
        except:
            print("\a Sorry, no more tasks to show.\v")
            task_index -= 1
            return task_index

    def show_previous_task(task_index):
        """
        Shows previous task, and add pagination
        :param task_index: integer
        :return: integer ... updated task integer
        """
        if task_index == 0:
            print("\a Sorry, this is the first task.\v")
        else:
            task_index -= 1
            task_list[task_index].show_task()
            print("Task {} of {}\n".format(task_index + 1, len(task_list)))
        return task_index

    def input_nav_menu():
        """
        Handles the navigation menu input
        :return: character ... user choice
        """
        nav_menu_items = ["n for next task", "p for previous tasks", "b back", "s select task"]
        for nav_menu_item in nav_menu_items:
            print(nav_menu_item)

        x = input("Choose :> ").strip().lower()
        if x not in "npbs":
            return input_nav_menu()
        else:
            return x

    def nav_menu(task_index):
        """
        Handles the navigation menu
        :param task_index: integer
        :return: Calls the appropiate function
        """
        option = input_nav_menu()

        if option == "n":
            task_index = show_next_task(task_index)
        elif option == "p":
            task_index = show_previous_task(task_index)
        elif option == "b":
            return None
        elif option == "s":
            return task_index
        else:
            print("\a")
        return nav_menu(task_index)

    if task_list:
        task_list[0].show_task()
        print("Task {} of {}\n".format(1, len(task_list)))
        selected_task_index = nav_menu(0)
        if isinstance(selected_task_index, int):
            # selected_task_index can be zero
            return task_list[selected_task_index]
        else:
            return None
    else:
        print(not_found_message)
        return None


# User Input and Validation


def input_task_date(validation_message):
    """
    Ask user for task date, validates,
    :return: string ... dd/mm/yyyy
    """

    show_validation_message(validation_message)

    raw_task_date = input("Please enter the date for this task. Enter help for help:> ") \
        .replace(" ", "").replace(".", "/").replace("-", "/").strip("").lower()
    # some countries use . for the / https://en.wikipedia.org/wiki/Date_format_by_country

    if raw_task_date == "help":
        help_message = """
Enter dates as dd/mm/yyyy.
    * If you want to use the alternative format of mm/dd/yyyy write the letter M before your date as in M12/23/2016.

    * If you want to use the alternative format of yyyy/mm/dd write the letter Y before the date as in Y2016/12/23.

    * You may also substitute / for . or - with or without spaces
        """
        return input_task_date(help_message)

    if raw_task_date:
        if raw_task_date[0] == "m":
            month = raw_task_date[1:3]
            day = raw_task_date[4:6]
            year = raw_task_date[7:]
            raw_task_date = "{}/{}/{}".format(day, month, year)
        elif raw_task_date[0] == "y":
            year = raw_task_date[1:5]
            month = raw_task_date[6:8]
            day = raw_task_date[9:]
            raw_task_date = "{}/{}/{}".format(day, month, year)
            print(raw_task_date)
        else:
            pass

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
    Generates a string with all the notes associated to a task separated by new lines characters
    :param task_notes: string
    :return: string ... task notes
    """
    my_note = input("Add a new line for the notes of this task, if any or hit enter to stop adding notes:> ")
    if not my_note:
        return task_notes
    else:
        task_notes += my_note + "\n"
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
    faster and less error prone to type an index number rather than a date.
    :param validation_message: string
    :param total_dates: integer ... number of different dates that have tasks
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
    Appends a task to the log
    :param task_entry: string
    :return:
    """
    with open(WORK_LOG_FILE_NAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(task_entry)


def rewrite_log_file(tasks_list):
    """
    rewrites the log file with new data
    :param tasks_list: string
    :return:
    """
    tasks_to_save = []
    for task in tasks_list:
        task_date = task.task_date
        task_description = task.description
        task_time_spent = str(task.time_spent)
        task_notes = task.notes
        tasks_to_save.append([task_date, task_description, task_time_spent, task_notes])
        with open(WORK_LOG_FILE_NAME, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tasks_to_save)

# Search Functions


def order_dates(dates_list):
    """
    Orders a list of dates, formated as strings,

    :param dates_list: string
    :return: string
    """
    dates_as_datetimes = []
    for date_item in dates_list:
        dates_as_datetimes.append(datetime.strptime(date_item, DATE_FORMAT))

    dates_list = []

    dates_as_datetimes = sorted(dates_as_datetimes)

    for d in dates_as_datetimes:
        dates_list.append(d.strftime(DATE_FORMAT))

    return dates_list


def find_dates_with_tasks(tasks):
    """
    Find the dates that have tasks, returns a list of strings that represent such dates, ordered as dates should be
    ordered
    :param tasks: [Task]
    :return: [string] ... dates that have tasks
    """
    dates_with_tasks = []

    for t in tasks:
        if t.task_date not in dates_with_tasks:
            dates_with_tasks.append(t.task_date)

    return order_dates(dates_with_tasks)


def show_dates_with_tasks(tasks):
    """
    Shows the dates that have tasks
    :param tasks: [Task]
    :return: [string] ... dates that have tasks
    """
    clear_screen()
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
    Handles the searching by date
    :return: selected task, if any
    """
    all_tasks = read_log_file()
    found_tasks = []  # [Task]
    # show dates with tasks
    dates_that_have_tasks = show_dates_with_tasks(all_tasks)

    if dates_that_have_tasks:
        range_dates = input("\nDo you want to search for entries within a range of dates? (y/N)>: ").strip().lower()
        if range_dates == "y":
            f_date_index = input_date_to_search("\n1. Enter the index of the first date",
                                                len(dates_that_have_tasks) - 1)
            s_date_index = input_date_to_search("2. Enter the index of the second date", len(dates_that_have_tasks) - 1)
            f_date_to_search = dates_that_have_tasks[f_date_index]
            s_date_to_search = dates_that_have_tasks[s_date_index]
            f_date_to_search = datetime.strptime(f_date_to_search, DATE_FORMAT)
            s_date_to_search = datetime.strptime(s_date_to_search, DATE_FORMAT)
            for task_item in all_tasks:
                if datetime.strptime(task_item.task_date, DATE_FORMAT) >= f_date_to_search:
                    if datetime.strptime(task_item.task_date, DATE_FORMAT) <= s_date_to_search:
                        found_tasks.append(task_item)

        else:
            date_index = input_date_to_search("", len(dates_that_have_tasks) - 1)
            date_to_search = dates_that_have_tasks[date_index]

            # search
            for task_item in all_tasks:
                if task_item.task_date == date_to_search:
                    found_tasks.append(task_item)

        selected_task = show_tasks(found_tasks, not_found_message="Sorry, no tasks found with that date")
        return selected_task

    else:
        print("Sorry no dates with task have been found.")
        return None


def find_by_time_spent():
    """
    Handles finding Tasks by time spent on them
    :return: Task ... selected Task, if any
    """
    found_tasks = []
    all_tasks = read_log_file()
    r_time = input("\nDo you want to find entries within a range of time spent on a task? y/N").strip().lower()
    if r_time == "y":
        f_time_spent = input_time_spent("\n 1. Enter the smaller item of the range:> ")
        s_time_spent = input_time_spent("2. Enter the larger item of the range:> ")
        for task_item in all_tasks:
            tits = int(task_item.time_spent)  # tits ^_^
            print(f_time_spent, s_time_spent, tits)
            if f_time_spent <= tits <= s_time_spent:
                found_tasks.append(task_item)
    else:
        time_spent_to_search = input_time_spent("")
        # search
        for task_item in all_tasks:
            if int(time_spent_to_search) == int(task_item.time_spent):
                found_tasks.append(task_item)
    # show list of tasks
    selected_task = show_tasks(found_tasks)
    return selected_task


def find_by_exact_search():
    """
    Handles searching Task by exact search.
    :return: Task ... selected Task if any
    """
    found_tasks = []
    string_to_search = input("\nEnter the exact words that you want to find:> ").strip().strip("\n")
    # ask for user input

    all_tasks = read_log_file()

    # search
    for task_item in all_tasks:
        if string_to_search == task_item.description:
            found_tasks.append(task_item)
        else:
            if string_to_search == task_item.notes.strip("\n"):
                found_tasks.append(task_item)

    selected_task = show_tasks(found_tasks)
    return selected_task


def find_by_pattern():
    """
    Handles searching Task by RegEx patter.
    :return: Task ... selected Task if any
    """
    import re
    found_tasks = []
    raw_re_string = input("\nEnter your Regular Expression pattern")
    # ask for user input
    compiled_re_string = re.compile(raw_re_string)
    print(compiled_re_string)
    # search
    all_tasks = read_log_file()

    for task_item in all_tasks:
        item_description = task_item.description
        item_notes = task_item.notes

        if compiled_re_string.search(item_description) or compiled_re_string.search(item_notes):
            found_tasks.append(task_item)

    # show list of tasks
    selected_task = show_tasks(found_tasks)
    return selected_task


# Command Functions

def add_entry():
    """
    Adds an entry based on user input
    :return: Calls append_task_to_log, appending it to the log
    """
    clear_screen()
    task_description = input("Task Description:> ")
    time_spent = input_time_spent("")
    task_notes = input_task_notes("").strip()
    task_date = input_task_date("")

    append_task_to_log([task_date, task_description, time_spent, task_notes])

    # update worklog file


def search_entries():
    """
    Searches for an entry, based on a sub-menu
    :return: Calls the appropriate function to edit of deleted any selected task
    """
    clear_screen()
    search_menu_functions = {"p": find_by_pattern, "d": find_by_date, "x": find_by_exact_search,
                             "t": find_by_time_spent, "m": main, "q": quit}
    search_menu_items = {"p": "find pattern", "d": "find by date", "x": "find by exact match",
                         "t": "find by time spent", "m": "back to main menu", "q": "quit the script"}
    selected_task = search_menu(search_menu_functions, search_menu_items)
    if selected_task:
        delete_task_input = input("Delete task? y/N").strip()
        if delete_task_input == "y":
            delete_task(selected_task)
        else:
            edit_task(selected_task)
    main()


def edit_task(task_to_edit):
    """
    Edites the selected Task, based on user input
    :param task_to_edit: Task
    :return: Calls rewrite_log
    """
    print(task_to_edit.description)
    new_description = input("\n\tChange description? y/N").strip().lower()
    if new_description == "y":
        new_description = input("\n\tNew description:> ")
    else:
        new_description = task_to_edit.description

    print(task_to_edit.task_date)
    new_date = input("\n\tChange date? y/N").strip().lower()
    if new_date == "y":
        new_date = input_task_date("")
    else:
        new_date = task_to_edit.task_date

    print(task_to_edit.time_spent)
    new_time_spent = input("\n\tChange time spent? y/N").strip().lower()
    if new_time_spent == "y":
        new_time_spent = input_time_spent("")
    else:
        new_time_spent = task_to_edit.time_spent

    for note in task_to_edit.notes:
        print(note)
    new_notes = input("\n\tChange notes? y/N").strip().lower()
    if new_notes == "y":
        new_notes = input_task_notes("")
    else:
        new_notes = task_to_edit.notes

    new_task = Task(new_description, new_time_spent, new_notes, new_date)

    all_tasks = read_log_file()
    all_tasks.remove(task_to_edit)
    all_tasks.append(new_task)
    rewrite_log_file(all_tasks)


def delete_task(task_to_delete):
    """
    Deletes the selected Task, after confirmation
    :param task_to_delete: Task
    :return: Calls rewrite_log
    """
    print("I am going to delete this entry")
    task_to_delete.show_task()
    sure = input("Are you sure? y/N").strip()
    if sure == "y":
        all_tasks = read_log_file()
        for task in all_tasks:
            if task == task_to_delete:
                all_tasks.remove(task)
                break
        # buckup file?
        rewrite_log_file(all_tasks)


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


def search_menu(menu_functions, menu_items):
    """
    Handles the search menu, pretty much like menu
    :param menu_functions: dictionary character:function name ... menu functions
    :param menu_items: dictionary character:string ... contains strings with the menu items
    :return: returns a calls to a function so it can pass whatever it returns
    """
    while True:
        user_choice = ask_for_choice("", menu_items)
        return menu_functions[user_choice]()


def menu(menu_functions, menu_items):
    """
    Handles the main menu
    :param menu_functions: dictionary character:function name ... menu functions
    :param menu_items: dictionary character:string ... contains strings with the menu items
    :return: just calls a function
    """
    while True:
        user_choice = ask_for_choice("", menu_items)
        menu_functions[user_choice]()


def main():
    """
    Main
    :return: Calls menu
    """
    main_menu_functions = {"a": add_entry, "f": search_entries, "q": exit}
    main_menu_items = {"a": "add entry", "f": "search entries", "q": "quit"}

    menu(main_menu_functions, main_menu_items)


main()
