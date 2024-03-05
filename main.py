import os
import json
from datetime import datetime

# Define the filename for storing tasks
TASKS_FILE = "tasks.json"

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

def show_tasks(tasks):
    # if tasks exists, enumerate over tasks, printing each and their individual details
    if tasks:
        print("Tasks:")
        for index, task in enumerate(tasks, 1):
            print(f"{index}. {task['description']} - Due: {task['due_date']} - Status: {task['status']}")

    # if tasks don't exist, print the below
    else:
        print("No tasks found.")

def add_task(tasks):
    # takes in a description, due date, applies a status of "Pending" and appends to tasks
    try:
        description = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        tasks.append({"description": description, "due_date": due_date, "status": "Pending"})
        save_tasks(tasks)
        print("Task added successfully.")
    except:
        print("Failed to add Task successfully")
        # ADD LOGGING!!!

def update_task(tasks):
    # NEED TO ADAPT
    # shows existing tasks, sets index to input task number
    show_tasks(tasks)
    index = int(input("Enter task number to update: ")) - 1

    # ensures input is within range, then allows for input of new status
    if 0 <= index < len(tasks):
        status = input("Enter new status (e.g., In Progress, Completed): ")
        tasks[index]["status"] = status
        save_tasks(tasks)
        print("Task updated successfully.")
    else:
        # catches failed input
        print("Invalid task number.")

def main():
    # Load tasks from the JSON file
    tasks = load_tasks()

    while True:
        print("\n===== Task Tracker Menu =====")
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Update Task Status")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            update_task(tasks)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()