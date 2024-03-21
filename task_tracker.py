import os
import json
from datetime import datetime
from rich import print
from rich.console import Console
from rich.table import Table

# Initialise rich console
console = Console()

# Define the filename for storing tasks
TASKS_FILE = "tasks.json"

def reset_table():
    #Makes table variable global (such that all functions may use it)
    global table
    #Reinitialised the table and adds it's columns
    table = Table(title="Tasks")

    table.add_column("T. No.", style="blue")
    table.add_column("Task", style="cyan")
    table.add_column("Importance", style="cyan")
    table.add_column("Has Description", style="green")
    table.add_column("Date Made", style="yellow")
    table.add_column("Due Date", style="yellow")
    table.add_column("Status", justify="right", style="orange1")
    table.add_column("RAG rating", style="orange1")

def load_tasks(task_json):

    # Uses os path to open TASKS_FILE json, if it exists. Uses json library to open loaded json
    if os.path.exists(task_json):
        with open(task_json, 'r', encoding="utf-8") as taskfile:
            return json.load(taskfile)
    else:
        return []

def save_tasks(task_dir, tasks):
    '''
    with the TASKS_FILE json open as taskfile, 
    append tasks to taskfile with an indent of 4 so it isn't grumpy
    '''
    with open(task_dir, 'w', encoding="utf-8") as taskfile:
        json.dump(tasks, taskfile, indent=4)

def show_task(tasks, task_index):
    #A function to show a task in it's entirety, try except for safety
    try:
        #Common in this program, insures index is not out of range
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            print(f"\n[bold red]{task['name']}[/bold red] [cyan]Task Details[/cyan]")
            print(f"Task Number - {task_index + 1}")
            print(f"Description - {task['description']}")
            print(f"Has Description - {task['has_description']}")
            print(f"Importance - {task['importance']}")
            print(f"Date Made - {task['date_made']}")
            print(f"Due Date - {task['due_date']}")
            print(f"Status - {task['status']}")
            print(f"RAG rating - {task['rag']}")
            '''Pause variable as an input, facilitates this typical return-pause 
            functionality... Old-School!'''
            input("\nPress RETURN to Continue...")
        else:
            print("Invalid task number")
    except Exception as e:
        #Exception handling, something I learned to make things pretty & professional : )
        print(f"An error occurred while showing task details: {e}")

def check_rag(due_date_string, status):

    current_date = datetime.now()

    due_date = datetime.strptime(due_date_string, '%Y-%m-%d')

    if due_date < current_date and status != "Completed" :
        return "red"
    elif due_date < current_date and status == "Completed" :
        return "amber"
    else:
        return "green"

def show_tasks(tasks):

    # if tasks exists, enumerate over tasks, printing each and their individual details
    if tasks:
        #calls reset_table function for aesthetic reasons
        reset_table()

        for index, task in enumerate(tasks,1):
            '''iterates over each item in tasks whilst keeping track of the index, 
            index starts at 1 for ease.'''
            task['rag'] = check_rag(str(task['due_date']), task['status'])
            # Sets each row to a different colour depending on rag rating
            # RED = late due date and incomplete, ORANGE = late due date but complete, GREEN = timely due date
            if task['rag'] == "red":
                table.add_row(str(index), task['name'], task['importance'], str(task['has_description']), task['date_made'], task['due_date'], task['status'], task['rag'], style="white on red")
            elif task['rag'] == "amber" :
                table.add_row(str(index), task['name'], task['importance'], str(task['has_description']), task['date_made'], task['due_date'], task['status'], task['rag'], style="white on orange_red1")
            elif task['rag'] == "green" :
                table.add_row(str(index), task['name'], task['importance'], str(task['has_description']), task['date_made'], task['due_date'], task['status'], task['rag'], style="white on green")


        # Prints the table using rich library to make things pretty
        console.print(table)

    # if tasks don't exist, print the below
    else:
        print("No tasks found.")

def add_task(task_dir, tasks):

    # Clears terminal, generally "prettier" :)
    os.system('clear')

    # takes in a description, due date, applies a status of "Pending" and appends to tasks
    try:
        try:
            name = str(input("Enter task name: ")).strip()
            if not name:
                raise ValueError("Name cannot be empty")
            description = input("Enter task description: ")
            if not description:
                has_description = False
            else:
                has_description = True
            valid_importance = ["high", "medium", "low"]
            importance = str(input("Enter task importance (high, medium, low): "))
            if importance not in valid_importance:
                raise ValueError("Invalid importance. Please choose from 'high', 'medium', or 'low'.")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            if not validate_date(due_date):
                raise ValueError("Invalid due date format. Please use YYYY-MM-DD.")
            elif not due_date:
                raise ValueError("Date cannot be empty")
            date_made = str(datetime.today().strftime('%Y-%m-%d'))
            status = "Pending"
        except Exception as e:
            print(f"Error: {e}")
            input("^^^")
        tasks.append({"name": name, "description": description, "has_description": has_description, "importance": importance, "date_made": date_made, "due_date": due_date, "status": status, "rag": check_rag(due_date,status)})
        save_tasks(task_dir, tasks)
        print("Task added successfully.")
    except:
        print(f"Failed to add Task sucessfully")


def delete_task(task_dir, tasks):
    while True:

        # Get user input for the task number to delete
        try:
            # takes index and removes 1 (to "interface" it to how python handles indexes)
            task_index = int(input("Enter task number to delete (or 0 to cancel): ")) - 1
            if task_index == -1:
                # Facilitation of the "(or 0 to cancel)" functionality
                print("Deletion canceled.")
                break
            if 0 <= task_index < len(tasks):
                #ensures index is within range & deletes task with the index selected before breaking loop
                del tasks[task_index]
                save_tasks(task_dir, tasks)
                print("Task deleted successfully.")
                break
        except ValueError as ve:
            #more pretty error exception handling
            print(f"Error: {ve}")


def validate_date(date_string):
    # function created to validate the date_string is in Y-m-d format
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def update_task(tasks):
    # shows existing tasks, sets index to input task number
    show_tasks(tasks)
    while True:
        try:
            index = int(input("Enter task number to update: ")) - 1
            if not(0 <= index < len(tasks)):
                #ensures index is within range, lest raises a ValueError
                raise ValueError("Invalid task number.")
            task_to_update = tasks[index]
            break
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
    while True:
        # Provides a selection for what attribute is wanted to be changed on a task
        print("Select what you want to update:\n1. Name\n2. Description\n3. Importance\n4. Due Date\n5. Status\n6. RAG Rating")
        option = input("Enter your choice (1-7): ").strip()
        if option == '1':
            while True:
                try:
                    new_name = str(input("Enter new name: ")).strip()
                    if not new_name:
                        raise ValueError("Name cannot be empty")
                    task_to_update["name"] = new_name
                    break
                except Exception as e:
                    print(f"Error updating name: {e}")
        elif option == '2':
            while True:
                try:
                    new_description = input("Enter new description: ").strip()
                    if not new_description:
                        task_to_update['has_description'] = "False"
                    task_to_update["description"] = new_description
                    break
                except Exception as e:
                    print(f"Error updating description: {e}")
        elif option == '3':
            try:
                valid_importance = ["high", "medium", "low"]
                new_importance = input("Enter new importance (high, medium, low): ").strip()
                if new_importance not in valid_importance:
                    raise ValueError("Invalid importance. Please choose from 'high', 'medium', or 'low'.")
                task_to_update["importance"] = new_importance
            except Exception as e:
                print(f"Error updating importance: {e}")
        elif option == '4':
            while True:
                try:
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                    if not validate_date(new_due_date):
                        raise ValueError("Invalid due date format. Please use YYYY-MM-DD.")
                    elif not new_due_date:
                        raise ValueError("Date cannot be empty")
                    task_to_update["due_date"] = new_due_date
                    break
                except ValueError as ve:
                    print(f"Error: {ve}")
        elif option == '5':
            try:
                valid_statuses = ["In Progress", "Pending", "Completed"]
                new_status = input("Enter new status (In Progress, Pending, or Completed): ").strip()
                if new_status not in valid_statuses:
                    raise ValueError("Invalid status. Please choose from 'In Progress', 'Pending', or 'Completed'.")
                task_to_update["status"] = new_status
            except Exception as e:
                print(f"Error updating status: {e}")
        elif option == '6':
            # Update RAG Rating
            try:
                new_rag = input("Enter new RAG rating (red, amber, green): ").strip().lower()
                if new_rag not in ["red", "amber", "green"]:
                    raise ValueError("Invalid RAG rating. Please choose from 'red', 'amber', or 'green'.")
                task_to_update["rag"] = new_rag
            except Exception as e:
                print(f"Error updating RAG rating: {e}")
        else:
            print("Invalid option. Please select a number between 1 and 7.")
            break
        save_tasks(TASKS_FILE, tasks)
        print("Task updated successfully.")
        break





def main():

    # Load tasks from the JSON file
    tasks = load_tasks(TASKS_FILE)

    while True:

        # Clears terminal, generally "prettier" :)
        os.system('clear')

        try:
            print("\n[bold red]Task Tracker Menu[/bold red]")

            show_tasks(tasks)

            print("1. Show Task \n2. Add Task \n3. Delete Task \n4. Update Task \n5. Exit")


            option = input('What would you like to do? (Type # then press ENTER to continue): ')

            match option:
                case '1':
                    while True:
                        try:
                            task_index = int(input("Enter task number to show: ")) - 1
                            show_task(tasks, task_index)
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid task number.")
                case '2':
                    add_task(TASKS_FILE, tasks)
                case '3':
                    show_tasks(tasks)
                    delete_task(TASKS_FILE, tasks)
                case '4':
                    update_task(tasks)
                case '5':
                    print("Exiting...")
                    os.system('clear')
                    break
                case _:
                    raise Exception("Invalid input")

        except:
            input("Invalid Input (press ENTER to retry):")


if __name__ == "__main__":
    main()
