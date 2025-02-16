import json
import os

# File to save tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the file if it exists."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks(todo_list):
    """Save tasks to the file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(todo_list, file)

def show_menu():
    print("\n--- To-Do List Menu ---")
    print("1. View To-Do List")
    print("2. Add a Task")
    print("3. Mark a Task as Completed")
    print("4. Mark a Task as Not Completed")
    print("5. Delete a Task")
    print("6. Exit")

def view_tasks(todo_list):
    if not todo_list:
        print("\nYour to-do list is empty!")
    else:
        print("\n--- Your To-Do List ---")
        for index, task in enumerate(todo_list, start=1):
            status = "Done" if task["completed"] else "Not Done"
            print(f"{index}. {task['name']} [{status}]")

def add_task(todo_list):
    task_name = input("\nEnter the task: ")
    todo_list.append({"name": task_name, "completed": False})
    save_tasks(todo_list)  # Save tasks after adding
    print(f"Task '{task_name}' added!")

def mark_completed(todo_list):
    view_tasks(todo_list)
    try:
        task_number = int(input("\nEnter the task number to mark as completed: "))
        if 1 <= task_number <= len(todo_list):
            todo_list[task_number - 1]["completed"] = True
            save_tasks(todo_list)  # Save tasks after marking
            print(f"Task '{todo_list[task_number - 1]['name']}' marked as completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def mark_not_completed(todo_list):
    view_tasks(todo_list)
    try:
        task_number = int(input("\nEnter the task number to mark as not completed: "))
        if 1 <= task_number <= len(todo_list):
            todo_list[task_number - 1]["completed"] = False
            save_tasks(todo_list)  # Save tasks after marking
            print(f"Task '{todo_list[task_number - 1]['name']}' marked as not completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task(todo_list):
    view_tasks(todo_list)
    try:
        task_number = int(input("\nEnter the task number to delete: "))
        if 1 <= task_number <= len(todo_list):
            deleted_task = todo_list.pop(task_number - 1)
            save_tasks(todo_list)  # Save tasks after deleting
            print(f"Task '{deleted_task['name']}' deleted!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    todo_list = load_tasks()  # Load tasks from file at startup
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-6): ")
        if choice == "1":
            view_tasks(todo_list)
        elif choice == "2":
            add_task(todo_list)
        elif choice == "3":
            mark_completed(todo_list)
        elif choice == "4":
            mark_not_completed(todo_list)
        elif choice == "5":
            delete_task(todo_list)
        elif choice == "6":
            print("\nExiting the application. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()