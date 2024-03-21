import os
import json
from datetime import datetime
from io import StringIO
import pytest
from task_tracker import load_tasks, save_tasks, add_task, delete_task, validate_date, update_task

# Define a pytest fixture to create a temporary tasks json file
@pytest.fixture
def temporary_tasks_file(tmpdir):
    # wiki told me to do it... joking, this is to join path to temp tasks.json
    temp_tasks_file = tmpdir.mkdir("sub").join("tasks.json")
    # creates a sort of string to call on behalf of temporary_tasks_file
    yield str(temp_tasks_file)

# Test case for trying to loading tasks from a null/blank file
def test_load_tasks_non_existing_file(temporary_tasks_file):
    tasks = load_tasks(temporary_tasks_file)
    assert tasks == []

# Test case for loading tasks from an existing tasks json file
def test_load_tasks_existing_file(temporary_tasks_file):
    # mock tasks data set
    tasks_data = [
        {"name": "Task 1", "description": "Description 1", "has_description": True, "importance": "high", 
         "date_made": "2024-10-01", "due_date": "2024-12-31", "status": "Pending", "rag": "green"},
        {"name": "Task 2", "description": "", "has_description": False, "importance": "low", 
         "date_made": "2023-03-01", "due_date": "2024-11-31", "status": "In Progress", "rag": "green"},
    ]
    
    #usage of inbuilt open library with indent (as used in application)
    with open(temporary_tasks_file, 'w') as f:
        json.dump(tasks_data, f, indent=4)
    
    tasks = load_tasks(temporary_tasks_file)

    #asserting that we have 2 tasks and each names are "Task 1" & "Task 2"
    assert len(tasks) == 2
    assert tasks[0]["name"] == "Task 1"
    assert tasks[1]["name"] == "Task 2"

# Test case for saving tasks to a file
def test_save_tasks(temporary_tasks_file):
    # mock tasks data set (again lol)
    tasks_data = [
        {"name": "Task 1", "description": "Description 1", "has_description": True, "importance": "high", 
         "date_made": "2024-10-01", "due_date": "2024-12-31", "status": "Pending", "rag": "green"},
        {"name": "Task 2", "description": "", "has_description": False, "importance": "low", 
         "date_made": "2023-03-01", "due_date": "2024-11-31", "status": "In Progress", "rag": "green"},
    ]
    
    save_tasks(temporary_tasks_file, tasks_data)
    
    # asserts that the saved temp file is the exact same as the task data appended
    assert load_tasks(temporary_tasks_file) == tasks_data

# Test case for adding a task
def test_add_task(temporary_tasks_file, monkeypatch):

    # empty mock of tasks json
    tasks_data = []

    # Mock user input using monkeypatch (was a pain to work)
    monkeypatch.setattr("sys.stdin", StringIO("AbCdEfG123\nTask Description\nhigh\n2024-12-31\n"))

    add_task(temporary_tasks_file, tasks_data)

    # this is bad practice? with open wasn't playing ball for some reason
    tasks = load_tasks(temporary_tasks_file)
    
    # asserts that there is one task with name "Task 1" & that name is my ridiculous made up thingy variable input
    assert len(tasks) == 1
    assert tasks[0]["name"] == "AbCdEfG123"

# Test case for deleting a task
def test_delete_task(temporary_tasks_file, monkeypatch):
    # Mock task data set (bet you never saw that coming)
    tasks_data = [
        {"name": "Task 1", "description": "Description 1", "has_description": True, "importance": "high", 
         "date_made": "2024-10-01", "due_date": "2024-12-31", "status": "Pending", "rag": "green"},
        {"name": "Task 2", "description": "", "has_description": False, "importance": "low", 
         "date_made": "2023-03-01", "due_date": "2024-11-31", "status": "In Progress", "rag": "green"},
    ]
    
    # with open library to write to temp tasks.json with mock data
    with open(temporary_tasks_file, "w") as f:
        json.dump(tasks_data, f)
    
    # Mock user input again
    monkeypatch.setattr("sys.stdin", StringIO("1\n"))

    delete_task(temporary_tasks_file, tasks_data)

    # Check if task is deleted
    with open(temporary_tasks_file, "r") as f:
        tasks = json.load(f)
    
    # assert that only 1 task exists and it's name is "Task 2" to avoid fluke
    assert len(tasks) == 1
    assert tasks[0]["name"] == "Task 2"

# Test case for validating date format
def test_validate_date():
    # basically bullying the command into filtering some random formats lol
    assert validate_date("2024-12-31") == True
    assert validate_date("12/31/2024") == False
    assert validate_date("31-12-2024") == False
