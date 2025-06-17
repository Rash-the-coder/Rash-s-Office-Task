import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()
        
    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        with open(TASKS_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=4)
    
    def add_task(self, title, deadline, assigned_to, priority):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "deadline": deadline,
            "assigned_to": assigned_to,
            "priority": priority,
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_tasks(self, completed=False):
        return [task for task in self.tasks if task['completed'] == completed]
    
    def get_upcoming_tasks(self):
        return sorted(
            [t for t in self.tasks if not t['completed']],
            key=lambda x: x['deadline']
        )[:5]
    
    def get_assigned_people(self):
        return list(set(task['assigned_to'] for task in self.tasks))
    
    def toggle_completion(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
        self.save_tasks()
        return task
    
    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_tasks()
    
    def edit_task(self, task_id, title, deadline, assigned_to, priority):
        for task in self.tasks:
            if task['id'] == task_id:
                task['title'] = title
                task['deadline'] = deadline
                task['assigned_to'] = assigned_to
                task['priority'] = priority
        self.save_tasks()
        return task
    
    def filter_tasks(self, priority=None, assigned=None):
        results = self.tasks
        if priority:
            results = [t for t in results if t['priority'] == priority]
        if assigned:
            results = [t for t in results if t['assigned_to'] == assigned]
        return results