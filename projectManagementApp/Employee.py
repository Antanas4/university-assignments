from collections import deque
import os

class Employee:
    position = ""
    taskDeque = deque()
    
    def __init__(self, position):
        self.position = position
        self.taskDeque = deque(maxlen = 10)

    def UpdateEmployee(self, position, task):
        self.position = position

        if task is not None:
            self.taskDeque.append(task)
    
    def RemoveTask(self, task):
        self.taskDeque.remove(task)

    def CreateTaskFile(self):
        downloadsFolder = os.path.expanduser("~/Downloads")
        filePath = os.path.join(downloadsFolder,f"{self.position}.txt")

        if os.path.exists(filePath) == 0:
            with open (filePath, "w") as file:
                for task in self.taskDeque:
                    file.write(f"Task Name: {task.name}\n")
                    file.write(f"Task Status: {task.status}\n")
                    file.write("\n")
        else:
            with open (filePath, "a") as file:
                for task in self.taskDeque:
                    file.write(f"Task Name: {task.name}\n")
                    file.write(f"Task Status: {task.status}\n")
                    file.write("\n")