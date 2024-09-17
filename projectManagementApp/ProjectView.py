import tkinter as tk
import tkinter.simpledialog
from tkinter import ttk
from ErrorDialog import ErrorDialog
import random

class ProjectView(tk.Frame):
    def __init__(self, parent, app, user, projectName, homeView):
        super().__init__(parent)
        self.app = app
        self.user = user
        self.homeView = homeView
        self.projectName = projectName
        self.project = self.user.GetCurrentProject(self.projectName)

        self.employeeListbox = []

        self.employeePositionLabel = tk.Label(self, text = "Employee's position: ")
        self.employeePositionEntry = tk.Entry(self)
        
        self.taskNameLabel = tk.Label(self, text = "Task Name: ")
        self.taskNameEntry = tk.Entry(self)

        self.employeePositionLabel.grid(row = 0, column = 2, padx = 5, pady = 1, sticky = "w")
        self.employeePositionEntry.grid(row = 0, column = 3, padx = 5, pady = 1, sticky = "w")
        self.taskNameLabel.grid(row = 1, column = 2, padx = 5, pady = 1, sticky = "w")
        self.taskNameEntry.grid(row = 1, column = 3, padx = 5, pady = 1, sticky = "w")

        self.HomePageButton()
        self.AddTaskButton()
        self.EndProjectButton()
        self.GenerateTaskFileButton()
        self.DisplayEmployees()
        self.EmployeeListbox()
        self.RedistributeTasksButton()

    def AddTaskButton(self):
        self.TaskButton = tk.Button(self, text = "Add Task", command = lambda: self.project.AddTask(self))
        self.TaskButton.grid(row = 3, column = 2, padx = 5, pady = 1, sticky = "w")

    def HomePageButton(self):
        self.homeButton = tk.Button(self, text="Home Page", command = lambda: self.app.ShowHome())
        self.homeButton.grid(row = 4, column = 2, padx = 5, pady = 1, sticky = "w")

    def GenerateTaskFileButton(self):
        self.GenerateButton = tk.Button(self, text = "Generate Task Files", command = lambda: self.project.GenerateEmployeeTaskFiles())
        self.GenerateButton.grid(row = 5, column = 2, padx = 5, pady = 1, sticky = "w")

    def RedistributeTasksButton(self):
        self.RedistributeTasks = tk.Button(self, text = "Redistribute tasks", command = lambda: self.project.RedistributeTasks(self))
        self.RedistributeTasks.grid(row = 6, column = 2, padx = 5, pady = 1, sticky = "w")

    def EndProjectButton(self):
        self.endButton = tk.Button(self, text = "End Project", command = lambda: self.EndProjecStatusDialog())
        self.endButton.grid(row = 7, column = 2, padx = 5, pady = 1, sticky = "w")
    
    def EndProjecStatusDialog(self):
        projectStatus = tkinter.simpledialog.askstring("Project Status", "Enter project status: ")
        
        if projectStatus != "":
            self.user.EndProject(self.projectName, projectStatus)
            self.homeView.UpdateProjectsListbox(self.projectName, None, True)
            self.app.ShowHome()
        else:
            ErrorDialog(self, "Enter Project Status!")

    def EmployeeListbox(self):
         for i, employee in enumerate (self.project.employeesList):
            self.employeeListbox.append(tk.Listbox(self, selectmode=tk.SINGLE, height=5, width=40))
            self.employeeListbox[i].grid(row=i, column=1, padx=10, pady=5, sticky="w")
            for task in employee.taskDeque:
                taskInfo = f"Name: {task.name}  Status: {task.status}"
                self.employeeListbox[i].insert(tk.END, taskInfo)

    def DisplayEmployees(self):
        for i, employee in enumerate(self.project.employeesList):
            entry = tk.Entry(self, width=15)
            entry.insert(0, employee.position)
            entry.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry.bind("<FocusOut>", lambda event, i=i: self.project.UpdateEmployeePosition(event, i))

        self.employeePositionEntry.delete(0, "end")
        self.taskNameEntry.delete(0, "end")

    def UpdateEmployeeListbox(self):

        for listbox in self.employeeListbox:
            listbox.delete(0, tk.END)

        for i, employee in enumerate(self.project.employeesList):
            for task in employee.taskDeque:
                taskInfo = f"Name: {task.name}  Status: {task.status}"
                self.employeeListbox[i].insert(tk.END, taskInfo)

        self.user.WriteChangesFile(self.projectName)


    

    
    