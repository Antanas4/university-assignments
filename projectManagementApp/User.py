import os
from Project import Project
import tkinter as tk
from datetime import datetime
from ErrorDialog import ErrorDialog

class User:
    projectsList = []
    
    def __init__(self):
        self.projectsList = []
    
    def GetCurrentProject(self, projectName):
        for project in self.projectsList:
            if projectName == project.name:
                return project
            
    def CreateNewProject(self, homeView):
        projectName = homeView.projectNameEntry.get()
        projectStartingDate = homeView.projectStartingDateEntry.get()
        projectEmployeesQuantity_str = homeView.projectEmployeesQuantityEntry.get()

        if not projectName or not projectStartingDate or not projectEmployeesQuantity_str:
            homeView.UpdateProjectsListbox(None, "Please fill in all fields", False)
        else:
            try:
                projectEmployeesQuantity = int(projectEmployeesQuantity_str)
                try:
                    datetime.strptime(projectStartingDate, '%Y-%m-%d')
                    if len(projectName) > 30:
                        homeView.UpdateProjectsListbox(None, "Project name is too long (max 30 characters).", False)
                    elif projectEmployeesQuantity < 6:
                        newProject = Project(projectName, projectStartingDate, projectEmployeesQuantity)
                        self.projectsList.append(newProject)
                        homeView.UpdateProjectsListbox(projectName, None, False)
                        self.GenerateProjectFile(projectName, projectStartingDate)
                    else:
                        homeView.UpdateProjectsListbox(None, "Maximum members quantity is 5", False)
                except ValueError:
                    homeView.UpdateProjectsListbox(None, "Date format must be year-month-day.", False)
            except ValueError:
                homeView.UpdateProjectsListbox(None, "Members Quantity must be a valid integer.", False)

    def GenerateProjectFile(self, projectName, projectStartingDate):
        downloadsFolder = os.path.expanduser("~/Downloads")
        filePath = os.path.join(downloadsFolder,f"{projectName}.txt")

        with open (filePath, "w") as file:
            file.write (f"Project Name: {projectName}\n")
            file.write (f"Project Start Date: {projectStartingDate}\n")

    def EndProject(self, projectName, projectStatus):
        downloadsFolder = os.path.expanduser("~/Downloads")
        filePath = os.path.join(downloadsFolder,f"{projectName}.txt")
        projectEndDate = datetime.today().date()

        with open (filePath, "a") as file:
            file.write (f"Project End Date: {projectEndDate}\n")
            file.write(f"Project Status: {projectStatus}\n")

        project = self.GetCurrentProject(projectName) 
        if project:
            self.projectsList.remove(project)

        self.projectsList = [p for p in self.projectsList if p.name != projectName]
        
    def WriteChangesFile(self, projectName):
        timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        downloadsFolder = os.path.expanduser("~/Downloads")
        project = self.GetCurrentProject(projectName) 
        filePath = os.path.join(downloadsFolder,f"{projectName}_Changes.txt")

        if os.path.exists(filePath) == 0:
            with open (filePath, "w") as file:
                file.write(f"Change Date: {timeStamp}\n")
                for employee in project.employeesList:
                    file.write(f"{employee.position}: \n")
                    for task in employee.taskDeque:
                        file.write(f"{task.name}  {task.status}\n")
                file.write("\n")
        else:
            with open (filePath, "a") as file:
                file.write(f"Change Date: {timeStamp}\n")
                for employee in project.employeesList:
                    file.write(f"{employee.position}: \n")
                    for task in employee.taskDeque:
                        file.write(f"{task.name}  {task.status}\n")
                file.write("\n")

