import os
import json
from datetime import datetime

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()
        
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.tasks = json.load(file)
            except json.JSONDecodeError:
                print("Error reading tasks file. Starting with empty task list.")
                self.tasks = []
        
    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)
            
    def add_task(self, title, description="", due_date=""):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{title}' added successfully!")
        
    def view_tasks(self, show_completed=True):
        if not self.tasks:
            print("No tasks found!")
            return
            
        print("\n" + "="*60)
        print(f"{'ID':<5}{'TITLE':<30}{'DUE DATE':<15}{'STATUS':<10}")
        print("="*60)
        
        for task in self.tasks:
            if not show_completed and task["completed"]:
                continue
                
            status = "✓" if task["completed"] else "⨯"
            print(f"{task['id']:<5}{task['title'][:28]:<30}{task['due_date'][:13]:<15}{status:<10}")
        print("="*60 + "\n")
        
    def view_task_details(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            print("\n" + "="*60)
            print(f"TASK #{task['id']}: {task['title']}")
            print("-"*60)
            print(f"Description: {task['description']}")
            print(f"Due Date: {task['due_date']}")
            print(f"Status: {'Completed' if task['completed'] else 'Pending'}")
            print(f"Created: {task['created_at']}")
            print("="*60 + "\n")
        else:
            print(f"Task with ID {task_id} not found!")
            
    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
        
    def mark_completed(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task["completed"] = True
            self.save_tasks()
            print(f"Task '{task['title']}' marked as completed!")
        else:
            print(f"Task with ID {task_id} not found!")
            
    def update_task(self, task_id, title=None, description=None, due_date=None):
        task = self.get_task_by_id(task_id)
        if task:
            if title:
                task["title"] = title
            if description:
                task["description"] = description
            if due_date:
                task["due_date"] = due_date
                
            self.save_tasks()
            print(f"Task #{task_id} updated successfully!")
        else:
            print(f"Task with ID {task_id} not found!")
            
    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            # Reindex tasks
            for i, task in enumerate(self.tasks):
                task["id"] = i + 1
                
            self.save_tasks()
            print(f"Task deleted successfully!")
        else:
            print(f"Task with ID {task_id} not found!")

def main():
    todo_list = ToDoList()
    
    while True:
        print("\nTO-DO LIST MANAGER")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. View Task Details")
        print("4. Mark Task as Completed")
        print("5. Update Task")
        print("6. Delete Task")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            due_date = input("Enter due date (optional, format YYYY-MM-DD): ")
            todo_list.add_task(title, description, due_date)
            
        elif choice == '2':
            show_completed = input("Show completed tasks? (y/n): ").lower() == 'y'
            todo_list.view_tasks(show_completed)
            
        elif choice == '3':
            task_id = int(input("Enter task ID: "))
            todo_list.view_task_details(task_id)
            
        elif choice == '4':
            task_id = int(input("Enter task ID to mark as completed: "))
            todo_list.mark_completed(task_id)
            
        elif choice == '5':
            task_id = int(input("Enter task ID to update: "))
            print("Leave field empty if you don't want to update it")
            title = input("Enter new title: ")
            description = input("Enter new description: ")
            due_date = input("Enter new due date (format YYYY-MM-DD): ")
            todo_list.update_task(task_id, title, description, due_date)
            
        elif choice == '6':
            task_id = int(input("Enter task ID to delete: "))
            todo_list.delete_task(task_id)
            
        elif choice == '7':
            print("Thank you for using To-Do List Manager!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()