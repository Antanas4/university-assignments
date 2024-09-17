import tkinter as tk
from ErrorDialog import ErrorDialog

class HomeView(tk.Frame):
    def __init__(self, parent, app, user):
        super().__init__(parent)
        self.app = app
        self.user = user
        self.projectsListBox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.InputProjectNameWidget()
        self.InputProjectStartingDateWidget()
        self.InputMembersQuantityWidget()
        self.CreateNewProjectButton()
        self.OpenProjectButton()
        self.ListBoxWidget()

    def ListBoxWidget (self):

        for project in self.user.projectsList:
            self.projectsListBox.insert(tk.END, project.name)

        self.projectsListBox.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")

    def InputProjectNameWidget(self):
        tk.Label(self, text="Project Name: ").grid(row=0, column=0, sticky="w")
        self.projectNameEntry = tk.Entry(self)
        self.projectNameEntry.grid(row=0, column=1)

    def InputProjectStartingDateWidget(self):
        tk.Label(self, text="Starting Date (year-month-day): ").grid(row=1, column=0, sticky="w")
        self.projectStartingDateEntry = tk.Entry(self)
        self.projectStartingDateEntry.grid(row=1, column=1)
    
    def InputMembersQuantityWidget(self):
        tk.Label(self, text="Members Quantity:").grid(row=2, column=0, sticky="w")
        self.projectEmployeesQuantityEntry = tk.Entry(self)
        self.projectEmployeesQuantityEntry.grid(row=2, column=1)
        
    def CreateNewProjectButton(self):
        self.createProjectBtn = tk.Button(self, text="Create New Project", command=lambda: self.user.CreateNewProject(self))
        self.createProjectBtn.grid(row=4, column=0, columnspan=2)

    def OpenProjectButton(self):
        self.openProjectBtn = tk.Button(self, text="Open Project", command=self.OpenProject)
        self.openProjectBtn.grid(row=4, column=2, columnspan=2)

    def OpenProject(self):
        selectedIndex = self.projectsListBox.curselection()
        if selectedIndex:
            projectName = self.projectsListBox.get(selectedIndex[0])
            self.app.ShowProject(projectName, self)

    def UpdateProjectsListbox(self, projectName, error, delete):
        if delete:
            for i in range(self.projectsListBox.size()):
                item = self.projectsListBox.get(i)
                if item == projectName:
                    self.projectsListBox.delete(i)
                    break 
        elif not delete:
            if projectName != None and error == None:
                self.projectsListBox.insert(tk.END, projectName)
                self.projectNameEntry.delete(0, 'end')
                self.projectStartingDateEntry.delete(0, 'end')
                self.projectEmployeesQuantityEntry.delete(0, 'end')
                self.app.ShowHome
            elif projectName == None and error != None:
                self.projectNameEntry.delete(0, 'end')
                self.projectStartingDateEntry.delete(0, 'end')
                self.projectEmployeesQuantityEntry.delete(0, 'end')
                ErrorDialog(self, error)
            elif projectName == None and error == None:
                pass
        else:
            pass
