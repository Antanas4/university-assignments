import tkinter as tk
import tkinter.simpledialog

class ErrorDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, message):
        self.message = message
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text=self.message, wraplength=300, justify="left").grid(row=0, column=0)

    def buttonbox(self):
        box = tk.Frame(self)
        
        okButton = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        okButton.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack()
