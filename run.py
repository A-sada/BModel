from classes import Task
from Vehicle_Base import Vehicle_Base as Vehicle
tasks = [
    Task(id=1, x_coordinate=0, y_coordinate=0, weight=10, ready_time=0, due_date=10, service_time=2),
    Task(id=5, x_coordinate=3, y_coordinate=7, weight=5,  ready_time=8, due_date=30, service_time=4),
    Task(id=2, x_coordinate=1, y_coordinate=2, weight=20, ready_time=1, due_date=15, service_time=3),

    Task(id=4, x_coordinate=6, y_coordinate=1, weight=10, ready_time=10, due_date=25, service_time=2),
    Task(id=3, x_coordinate=4, y_coordinate=4, weight=15, ready_time=5, due_date=20, service_time=1),
]
car = Vehicle(1,1000)
car.tasks.append (tasks[-1])
for i in range(4):
    if car.add(tasks[i]) == False:
        print("errow")
        i += -1

print(car.tasks)