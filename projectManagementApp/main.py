import tkinter as tk
from App import App
from User import User

if __name__ == "__main__": 
    user = User()
    root = tk.Tk()
    app = App(root, user)
    app.Run()
