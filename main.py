import os
import json
import time
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
    table.add_column("Due Date", style="green")
    table.add_column("Status", justify="right", style="green")

def load_tasks():

    # Uses os path to oepn TASKS_FILE json, if it exists. Uses json library to open loaded json
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as taskfile:
            return json.load(taskfile)
    else:
        return []

def save_tasks(tasks):
    # with the TASKS_FILE json open as taskfile, append tasks to taskfile with an indent of 4 so it isn't grumpy
    with open(TASKS_FILE, 'w') as taskfile:
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
            print(f"Due Date - {task['due_date']}")
            print(f"Status - {task['status']}")
            #Pause variable as an input, facilitates this typical return-pause functionality... Old-School!
            pause = input("\nPress RETURN to Continue...")
        else:
            print("Invalid task number")
    except Exception as e:
        #Exception handling, something I learned to make things pretty & professional : )
        print(f"An error occurred while showing task details: {e}")


def show_tasks(tasks):

    # if tasks exists, enumerate over tasks, printing each and their individual details
    if tasks:
        #calls reset_table function for aesthetic reasons
        reset_table()
        #utlised datetime library to create a variable of the current date
        current_date = datetime.now()

        for index, task in enumerate(tasks,1):

            due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")

            if due_date < current_date and task['status'] != "Completed" :
                table.add_row(str(index), task['name'], task['due_date'], task['status'], style="red")
            elif due_date < current_date and task['status'] == "Completed" :
                table.add_row(str(index), task['name'], task['due_date'], task['status'], style="orange1")
            else:
                table.add_row(str(index), task['name'], task['due_date'], task['status'], style="green")

        console.print(table)

    # if tasks don't exist, print the below
    else:
        print("No tasks found.")

def add_task(tasks):

    # Clears terminal, generally "prettier" :)
    os.system('clear')

    # takes in a description, due date, applies a status of "Pending" and appends to tasks
    try:
        name = input("Enter task name: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        tasks.append({"name": name, "description": description, "due_date": due_date, "status": "Pending"})
        save_tasks(tasks)
        print("Task added successfully.")
    except:
        print("Failed to add Task successfully")

def delete_task(tasks):
    while True:
        # Show existing tasks
        show_tasks(tasks)

        # Get user input for the task number to delete
        try:
            task_index = int(input("Enter task number to delete (or 0 to cancel): ")) - 1
            if task_index == -1:
                print("Deletion canceled.")
                break
            elif 0 <= task_index < len(tasks):
                del tasks[task_index]
                save_tasks(tasks)
                print("Task deleted successfully.")
                break
            else:
                print("Invalid task number. Please enter a valid task number.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")


def validate_date(date_string):
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
            if not (0 <= index < len(tasks)):
                raise ValueError("Invalid task number.")
            
            task_to_update = tasks[index]
            
            print("Select what you want to update:")
            print("1. Name")
            print("2. Description")
            print("3. Due Date")
            print("4. Status")
            option = input("Enter your choice (1-4): ").strip()
            
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
                            raise ValueError("Description cannot be empty")
                        task_to_update["description"] = new_description
                        break
                    except Exception as e:
                        print(f"Error updating description: {e}")

            elif option == '3':
                while True:
                    try:
                        new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                        if not validate_date(new_due_date):
                            raise ValueError("Invalid due date format. Please use YYYY-MM-DD.")
                        task_to_update["due_date"] = new_due_date
                        break
                    except ValueError as ve:
                        print(f"Error: {ve}")
            elif option == '4':
                try:
                    valid_statuses = ["In Progress", "Pending", "Completed"]
                    new_status = input("Enter new status (In Progress, Pending, or Completed): ").strip()
                    if new_status not in valid_statuses:
                        raise ValueError("Invalid status. Please choose from 'In Progress', 'Pending', or 'Completed'.")
                    task_to_update["status"] = new_status
                except Exception as e:
                    print(f"Error updating status: {e}")
            else:
                print("Invalid option. Please select a number between 1 and 4.")
                continue
            
            save_tasks(tasks)
            print("Task updated successfully.")
            break
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")





def main():

    # Load tasks from the JSON file
    tasks = load_tasks()

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
                    add_task(tasks)
                case '3':
                    delete_task(tasks)
                case '4':
                    update_task(tasks)
                case '5':
                    print("Exiting...")
                    os.system('clear')
                    break
                case _:
                    raise Exception("Invalid input")

        except:
            pause = input("Invalid Input (press ENTER to retry):")


if __name__ == "__main__":
    main()