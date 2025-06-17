import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from datetime import datetime
from task_manager import TaskManager

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rash's Office Tasks")
        self.root.geometry("900x650")
        
        # Dark theme configuration
        self.style = Style(theme='darkly')
        self.style.configure('TFrame', background='#2e2e2e')
        self.style.configure('TLabel', background='#2e2e2e', foreground='#e0e0e0')
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('Treeview', background='#3a3a3a', fieldbackground='#3a3a3a', 
                           foreground='#e0e0e0', rowheight=25)
        self.style.configure('Treeview.Heading', background='#252525', foreground='#ffffff', 
                           font=('Segoe UI', 10, 'bold'))
        self.style.configure('TCombobox', fieldbackground='#3a3a3a', foreground='#e0e0e0')
        self.style.configure('TEntry', fieldbackground='#3a3a3a', foreground='#e0e0e0')
        self.style.configure('TLabelframe', background='#2e2e2e', foreground='#e0e0e0')
        self.style.configure('TLabelframe.Label', background='#2e2e2e', foreground='#64b5f6')
        
        self.task_manager = TaskManager()
        self.create_main_menu()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Frame(self.root, style='TFrame')
        status_bar.pack(side='bottom', fill='x', padx=10, pady=5)
        ttk.Label(status_bar, textvariable=self.status_var, foreground='#aaaaaa', 
                 font=('Segoe UI', 9)).pack(side='right')
    
    def create_main_menu(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, ttk.Frame):  # Keep status bar
                widget.destroy()
        
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill='x', pady=(0, 30))
        ttk.Label(header, text="Rash's Office Tasks", font=('Segoe UI', 24, 'bold'), 
                 foreground='#64b5f6').pack(side='left')
        ttk.Label(header, text="© Rashodha Senevirathne", font=('Segoe UI', 10),
                 foreground='#aaaaaa').pack(side='right')
        
        # Menu buttons
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(pady=20)
        
        menu_items = [
            ("➕ Create New Task", "success-outline", self.create_task_window),
            ("📋 View All Tasks", "info-outline", lambda: self.show_tasks()),
            ("✅ View Completed Tasks", "success", lambda: self.show_tasks(completed=True)),
            ("⏰ View Upcoming Deadlines", "warning-outline", self.show_upcoming_tasks),
            ("🧍‍♂️ View Assigned People", "primary-outline", self.show_assigned_people),
            ("🔎 Filter Tasks", "secondary-outline", self.filter_tasks_window)
        ]
        
        for text, bootstyle, command in menu_items:
            btn = ttk.Button(
                menu_frame, 
                text=text,
                command=command,
                width=25,
                bootstyle=bootstyle
            )
            btn.pack(pady=8)
    
    def create_task_window(self):
        window = tk.Toplevel(self.root)
        window.title("Create New Task")
        window.geometry("500x450")
        
        content = ttk.Frame(window)
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(content, text="Task Details", font=('Segoe UI', 12, 'bold')).pack(pady=(0, 15))
        
        # Task form
        form_frame = ttk.Frame(content)
        form_frame.pack(fill='x', pady=5)
        
        ttk.Label(form_frame, text="Task Title:").grid(row=0, column=0, padx=5, pady=8, sticky='w')
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=8, sticky='w')
        deadline_entry = ttk.Entry(form_frame, width=20)
        deadline_entry.grid(row=1, column=1, padx=5, pady=8, sticky='w')
        
        ttk.Label(form_frame, text="Assign To:").grid(row=2, column=0, padx=5, pady=8, sticky='w')
        assigned_entry = ttk.Entry(form_frame, width=30)
        assigned_entry.grid(row=2, column=1, padx=5, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, padx=5, pady=8, sticky='w')
        priority_combo = ttk.Combobox(form_frame, values=["High", "Medium", "Low"])
        priority_combo.current(0)
        priority_combo.grid(row=3, column=1, padx=5, pady=8, sticky='w')
        
        # Button frame
        btn_frame = ttk.Frame(content)
        btn_frame.pack(fill='x', pady=20)
        
        def submit_task():
            if not title_entry.get():
                messagebox.showerror("Error", "Task title is required!")
                return
                
            task = self.task_manager.add_task(
                title=title_entry.get(),
                deadline=deadline_entry.get(),
                assigned_to=assigned_entry.get(),
                priority=priority_combo.get()
            )
            self.status_var.set(f"Task '{task['title']}' created successfully")
            window.destroy()
        
        ttk.Button(btn_frame, text="Create Task", command=submit_task, 
                  bootstyle="success").pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=window.destroy).pack(side='right', padx=5)
    
    def show_tasks(self, completed=False):
        window = tk.Toplevel(self.root)
        window.title("Completed Tasks" if completed else "All Tasks")
        window.geometry("1000x600")
        
        container = ttk.Frame(window)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ("ID", "Title", "Created", "Deadline", "Assigned To", "Priority", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Configure columns
        col_widths = [50, 250, 120, 120, 150, 80, 100]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor='center' if col in ["ID", "Priority", "Status"] else 'w')
            tree.heading(col, text=col)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        # Add tasks
        tasks = self.task_manager.get_tasks(completed)
        for task in tasks:
            status = "✅ Completed" if task['completed'] else "🟡 Pending"
            tree.insert("", "end", values=(
                task['id'],
                task['title'],
                task['created'],
                task['deadline'],
                task['assigned_to'],
                task['priority'],
                status
            ), tags=("completed" if task['completed'] else "pending"))
        
        # Color tags
        tree.tag_configure("completed", background='#2d572c')
        tree.tag_configure("pending", background='#4e3f31')
        
        # Action buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill='x', pady=10)
        
        if not completed:
            ttk.Button(btn_frame, text="Mark Complete", command=lambda: self.toggle_complete(tree), 
                      bootstyle="success").pack(side='left', padx=5)
        else:
            ttk.Button(btn_frame, text="Mark Incomplete", command=lambda: self.toggle_complete(tree), 
                      bootstyle="warning").pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="Delete Task", command=lambda: self.delete_task(tree), 
                  bootstyle="danger").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Edit Task", command=lambda: self.edit_task(tree), 
                  bootstyle="info").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Close", command=window.destroy).pack(side='right', padx=5)
    
    def show_upcoming_tasks(self):
        window = tk.Toplevel(self.root)
        window.title("Upcoming Deadlines")
        window.geometry("1000x500")
        
        container = ttk.Frame(window)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="Tasks with Closest Deadlines", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Treeview setup (similar to show_tasks)
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ("ID", "Title", "Created", "Deadline", "Assigned To", "Priority", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        col_widths = [50, 250, 120, 120, 150, 80, 100]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor='center' if col in ["ID", "Priority", "Status"] else 'w')
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        # Add upcoming tasks
        tasks = self.task_manager.get_upcoming_tasks()
        for task in tasks:
            status = "✅ Completed" if task['completed'] else "🟡 Pending"
            tree.insert("", "end", values=(
                task['id'],
                task['title'],
                task['created'],
                task['deadline'],
                task['assigned_to'],
                task['priority'],
                status
            ), tags=("completed" if task['completed'] else "pending"))
        
        tree.tag_configure("completed", background='#2d572c')
        tree.tag_configure("pending", background='#4e3f31')
        
        # Action buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text="Mark Complete", command=lambda: self.toggle_complete(tree), 
                  bootstyle="success").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=lambda: self.delete_task(tree), 
                  bootstyle="danger").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Edit Task", command=lambda: self.edit_task(tree), 
                  bootstyle="info").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Close", command=window.destroy).pack(side='right', padx=5)
    
    def show_assigned_people(self):
        window = tk.Toplevel(self.root)
        window.title("Assigned People")
        window.geometry("400x350")
        
        container = ttk.Frame(window)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="People with Assigned Tasks", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 15))
        
        people = self.task_manager.get_assigned_people()
        if not people:
            ttk.Label(container, text="No people assigned yet", 
                     foreground='#aaaaaa').pack(expand=True)
            return
        
        list_frame = ttk.Frame(container)
        list_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(list_frame, bg='#3a3a3a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for person in people:
            ttk.Label(scrollable_frame, text=f"• {person}", 
                     font=('Segoe UI', 11)).pack(anchor='w', pady=3, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def filter_tasks_window(self):
        window = tk.Toplevel(self.root)
        window.title("Filter Tasks")
        window.geometry("500x300")
        
        container = ttk.Frame(window)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text="Filter Criteria", 
                 font=('Segoe UI', 12, 'bold')).pack(pady=(0, 15))
        
        # Filter options
        options_frame = ttk.LabelFrame(container, text="Select Filters")
        options_frame.pack(fill='x', pady=10)
        
        ttk.Label(options_frame, text="Priority:").grid(row=0, column=0, padx=5, pady=10, sticky='w')
        priority_combo = ttk.Combobox(options_frame, values=["", "High", "Medium", "Low"])
        priority_combo.grid(row=0, column=1, padx=5, pady=10, sticky='ew')
        
        ttk.Label(options_frame, text="Assigned To:").grid(row=1, column=0, padx=5, pady=10, sticky='w')
        assigned_combo = ttk.Combobox(options_frame, values=[""] + self.task_manager.get_assigned_people())
        assigned_combo.grid(row=1, column=1, padx=5, pady=10, sticky='ew')
        
        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill='x', pady=10)
        
        def apply_filters():
            filtered = self.task_manager.filter_tasks(
                priority=priority_combo.get() if priority_combo.get() else None,
                assigned=assigned_combo.get() if assigned_combo.get() else None
            )
            window.destroy()
            self.display_filtered_results(filtered)
        
        ttk.Button(btn_frame, text="Apply Filters", command=apply_filters, 
                  bootstyle="primary").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=window.destroy).pack(side='right', padx=5)
    
    def display_filtered_results(self, tasks):
        window = tk.Toplevel(self.root)
        window.title("Filtered Tasks")
        window.geometry("1000x500")
        
        container = ttk.Frame(window)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(container, text=f"Found {len(tasks)} matching tasks", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        if not tasks:
            ttk.Label(container, text="No tasks match your criteria", 
                     foreground='#aaaaaa').pack(expand=True)
            ttk.Button(container, text="Close", command=window.destroy).pack(pady=20)
            return
        
        # Treeview setup (similar to show_tasks)
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ("ID", "Title", "Created", "Deadline", "Assigned To", "Priority", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        col_widths = [50, 250, 120, 120, 150, 80, 100]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor='center' if col in ["ID", "Priority", "Status"] else 'w')
            tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        # Add tasks
        for task in tasks:
            status = "✅ Completed" if task['completed'] else "🟡 Pending"
            tree.insert("", "end", values=(
                task['id'],
                task['title'],
                task['created'],
                task['deadline'],
                task['assigned_to'],
                task['priority'],
                status
            ), tags=("completed" if task['completed'] else "pending"))
        
        tree.tag_configure("completed", background='#2d572c')
        tree.tag_configure("pending", background='#4e3f31')
        
        # Action buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text="Mark Complete", command=lambda: self.toggle_complete(tree), 
                  bootstyle="success").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=lambda: self.delete_task(tree), 
                  bootstyle="danger").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Edit Task", command=lambda: self.edit_task(tree), 
                  bootstyle="info").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Close", command=window.destroy).pack(side='right', padx=5)
    
    def toggle_complete(self, treeview):
        selected = treeview.selection()
        if not selected:
            self.status_var.set("Please select a task first")
            return
            
        item = treeview.item(selected[0])
        task_id = item['values'][0]
        updated_task = self.task_manager.toggle_completion(task_id)
        
        # Update treeview
        status = "✅ Completed" if updated_task['completed'] else "🟡 Pending"
        treeview.item(selected[0], values=(
            updated_task['id'],
            updated_task['title'],
            updated_task['created'],
            updated_task['deadline'],
            updated_task['assigned_to'],
            updated_task['priority'],
            status
        ), tags=("completed" if updated_task['completed'] else "pending"))
        
        self.status_var.set(f"Task {task_id} marked as {'completed' if updated_task['completed'] else 'pending'}")
    
    def delete_task(self, treeview):
        selected = treeview.selection()
        if not selected:
            self.status_var.set("Please select a task first")
            return
            
        if messagebox.askyesno(
            "Confirm Delete", 
            "Are you sure you want to delete this task?",
            icon='warning'
        ):
            item = treeview.item(selected[0])
            task_id = item['values'][0]
            self.task_manager.delete_task(task_id)
            treeview.delete(selected[0])
            self.status_var.set(f"Task {task_id} deleted successfully")
    
    def edit_task(self, treeview):
        selected = treeview.selection()
        if not selected:
            self.status_var.set("Please select a task first")
            return
            
        item = treeview.item(selected[0])
        task_id = item['values'][0]
        
        # Find the task
        task = None
        for t in self.task_manager.tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if not task:
            messagebox.showerror("Error", "Task not found")
            return
        
        # Edit window
        window = tk.Toplevel(self.root)
        window.title("Edit Task")
        window.geometry("500x450")
        
        content = ttk.Frame(window)
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(content, text="Edit Task Details", font=('Segoe UI', 12, 'bold')).pack(pady=(0, 15))
        
        # Task form
        form_frame = ttk.Frame(content)
        form_frame.pack(fill='x', pady=5)
        
        ttk.Label(form_frame, text="Task Title:").grid(row=0, column=0, padx=5, pady=8, sticky='w')
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.insert(0, task['title'])
        title_entry.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=8, sticky='w')
        deadline_entry = ttk.Entry(form_frame, width=20)
        deadline_entry.insert(0, task['deadline'])
        deadline_entry.grid(row=1, column=1, padx=5, pady=8, sticky='w')
        
        ttk.Label(form_frame, text="Assign To:").grid(row=2, column=0, padx=5, pady=8, sticky='w')
        assigned_entry = ttk.Entry(form_frame, width=30)
        assigned_entry.insert(0, task['assigned_to'])
        assigned_entry.grid(row=2, column=1, padx=5, pady=8, sticky='ew')
        
        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, padx=5, pady=8, sticky='w')
        priority_combo = ttk.Combobox(form_frame, values=["High", "Medium", "Low"])
        priority_combo.set(task['priority'])
        priority_combo.grid(row=3, column=1, padx=5, pady=8, sticky='w')
        
        # Button frame
        btn_frame = ttk.Frame(content)
        btn_frame.pack(fill='x', pady=20)
        
        def submit_edit():
            self.task_manager.edit_task(
                task_id=task_id,
                title=title_entry.get(),
                deadline=deadline_entry.get(),
                assigned_to=assigned_entry.get(),
                priority=priority_combo.get()
            )
            
            # Update treeview
            treeview.item(selected[0], values=(
                task_id,
                title_entry.get(),
                task['created'],
                deadline_entry.get(),
                assigned_entry.get(),
                priority_combo.get(),
                "✅ Completed" if task['completed'] else "🟡 Pending"
            ))
            
            self.status_var.set(f"Task {task_id} updated successfully")
            window.destroy()
        
        ttk.Button(btn_frame, text="Save Changes", command=submit_edit, 
                  bootstyle="success").pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=window.destroy).pack(side='right', padx=5)