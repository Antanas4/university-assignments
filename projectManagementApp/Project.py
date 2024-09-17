from llist import sllist

from Employee import Employee
from Task import Task
from collections import deque
from ErrorDialog import ErrorDialog
import random

class Project:
    projectStatus = False
    employeesList = sllist()
    name = ""
    startingDate = ""
    employeesQuantity = ""
    projectEndDate = ""
    seenTaskNames = set()

    def __init__(self, name, startingDate, employeesQuantity):
        self.projectStatus = False
        self.name = name
        self.startingDate = startingDate
        self.projectEndDate = ""
        self.seenTaskNames = set()

        self.employeesList = sllist()
        self.employeesQuantity = employeesQuantity

        for i in range(employeesQuantity):
            self.employeesList.append(Employee("Enter Position"))

    def UpdateEmployeePosition(self, event, index):
        position = event.widget.get()
        node = self.employeesList.nodeat(index)
        node.value.position = position

    def GenerateEmployeeTaskFiles(self):
        for employee in self.employeesList:
            employee.CreateTaskFile()
    
    def RedistributeTasks(self, projectView):
        notFinishedTasks = []

        for index, employee in enumerate(self.employeesList):
            for task in employee.taskDeque:
                if task.status == "In progress. Will not be completed in time":
                    notFinishedTasks.append((index, task))

        for (employeeIndex, task) in notFinishedTasks:
            employee = self.employeesList[employeeIndex]
            taskToRemove = next((t for t in employee.taskDeque if t.name == task.name and t.status == "In progress. Will not be completed in time"), None)
            if taskToRemove:
                employee.taskDeque.remove(taskToRemove)
            
        for (employee_index, task) in notFinishedTasks:
            employee = self.employeesList[employee_index]
            task.status = "Completed"
            available_employee = self.ShortestTaskDequeEmployee(employee.position)
            if available_employee:
                available_employee.taskDeque.append(task)
        projectView.UpdateEmployeeListbox()

    def ShortestTaskDequeEmployee(self, notAvailableEmployee):
        minLen = 100
        availableEmployee = None

        for employee in self.employeesList:
            if len(employee.taskDeque) < minLen and employee.position != notAvailableEmployee:
                availableEmployee = employee
                minLen = len(employee.taskDeque)
        
        return availableEmployee
    
    def AddTask(self, projectView):
        employeePosition = projectView.employeePositionEntry.get()
        taskName = projectView.taskNameEntry.get()
        taskStatus = random.choice(["Completed", 
                                    "In progress. Will be completed in time", 
                                    "In progress. Will not be completed in time"])

        validEmployee = self.ValidateEmployee(employeePosition)

        if validEmployee != None:
            validTask = self.ValidateTask(validEmployee, taskName)
            if validTask == "":
                newTask = Task(taskName, taskStatus)
                validEmployee.taskDeque.append(newTask)
                projectView.employeePositionEntry.delete(0, "end")
                projectView.taskNameEntry.delete(0, "end")
                projectView.UpdateEmployeeListbox()
            else:
                ErrorDialog(projectView, validTask)
        else:
                ErrorDialog(projectView, "Employee does not exist")

        
    def ValidateEmployee(self, employeePosition):
        validEmployee = None

        for employee in self.employeesList:
            if employee.position == employeePosition:
                validEmployee = employee
                break
            else:
                validEmployee == None

        return validEmployee
    
    def ValidateTask(self, validEmployee, taskName):

        if taskName and taskName.strip():
            if len(taskName) < 21:
                for task in validEmployee.taskDeque:
                    if taskName in self.seenTaskNames:
                        return "Can not create task's with the same name"
                self.seenTaskNames.add(taskName)
            else:
                return "Task name too long (max 20 characters)"
        else:
            return "Enter a task name!"

        return ""