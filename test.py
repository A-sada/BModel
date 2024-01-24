from balletin_are_search import *
from classes import *
from VRPTW_functions import *
from Strategy_Vehicle_ver1 import *
tasks = [
    Task(1,5,5,1,0,1000,1),
    Task(2,15,15,1,0,1000,1),
    Task(3,25,25,1,0,1000,1),
    Task(4,35,35,1,0,1000,1),
    Task(5,45,45,1,0,1000,1),
    Task(6,55,55,1,0,1000,1),
    Task(7,65,65,1,0,1000,1),
    Task(8,75,75,1,0,1000,1),
    Task(9,85,85,1,0,1000,1),
    Task(10,95,95,1,0,1000,1),
]
car = [Vehicle(1,100,0,0)]
car[0].tasks = tasks
# print(plot_vehicle_routes(car))                                                                                                                                     
# print(most_stayed_area_dynamic(tasks,100,10,create_time_zones(100,7),10,0,0))
