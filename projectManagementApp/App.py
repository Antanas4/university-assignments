import tkinter as tk
from HomeView import HomeView
from ProjectView import ProjectView
from User import User

class App:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Project Management System")
        root.geometry("1000x500")
        self.homeView = HomeView(root, self, self.user)

        self.currentFrame = self.homeView
        self.currentFrame.pack()

    def ShowProject(self, projectName, homeView):
        self.currentFrame.pack_forget()
        self.projectView = ProjectView(self.root, self, self.user, projectName, homeView)
        self.currentFrame = self.projectView
        self.currentFrame.pack()

    def ShowHome(self):
        self.currentFrame.pack_forget()
        self.homeView = HomeView(self.root, self, self.user)
        self.currentFrame = self.homeView
        self.currentFrame.pack()

    def Run(self):
        self.root.mainloop()
