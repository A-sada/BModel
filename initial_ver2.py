import random

import copy
from Strategy_Vehicle_ver4 import Vehicle
from classes import Task
from VRPTW_functions import euclidean_distance
from fun_for_test import route_check   

def check_task(vehicle,new_task,dep_x,dep_y):
    if vehicle.current_weight + new_task.weight > vehicle.max_weight:
        return False
    for i in range(len(vehicle.tasks)):
        route = copy.deepcopy(vehicle.tasks)
        route.insert(i,new_task)
        if route_check(route,dep_x,dep_y) == True:
            return True
    
    return False

def cost_back(vehicle , new_task):
    def calculate_additional_distance(tasks, new_task, insertion_index):
        if not tasks:
            return 0

        # 挿入位置がリストの先頭の場合
        if insertion_index == 0:
            return euclidean_distance(new_task, tasks[0])

        # 挿入位置がリストの末尾の場合
        elif insertion_index == len(tasks):
            return euclidean_distance(tasks[-1], new_task)

        # 挿入位置がリストの中間の場合
        else:
            distance_before_insertion = euclidean_distance(tasks[insertion_index - 1], tasks[insertion_index])
            distance_after_insertion = euclidean_distance(tasks[insertion_index - 1], new_task) + \
                                    euclidean_distance(new_task, tasks[insertion_index])
            return distance_after_insertion - distance_before_insertion
    
        

    min_additional_distance = float('inf')
    optimal_position = None

    for insertion_index in range(len(vehicle.tasks) + 1):

    # 時間窓制約を満たしているかを確認します
        copy_tasks = copy.deepcopy(vehicle.tasks)
        copy_tasks.insert(insertion_index, new_task)
        if route_check(copy_tasks,vehicle.dep_x,vehicle.dep_y):

            additional_distance = calculate_additional_distance(vehicle.tasks, new_task, insertion_index)
            if additional_distance < min_additional_distance:
                min_additional_distance = additional_distance
                optimal_position = insertion_index

        return min_additional_distance 

def task_add(vehicle, new_task,dep_x, dep_y):
    if vehicle.current_weight + new_task.weight > vehicle.max_weight:
        return False
    index = least_cost_time_insertion_index(vehicle,new_task)
    if index != None:
        vehicle.tasks.insert(index,new_task)
        vehicle.current_weight += new_task.weight
        return True
    
    return False
def least_cost_time_insertion_index(vehicle , new_task):

        def calculate_additional_distance(tasks, new_task, insertion_index):
            if not tasks:
                return 0

            # 挿入位置がリストの先頭の場合
            if insertion_index == 0:
                return euclidean_distance(new_task, tasks[0])

            # 挿入位置がリストの末尾の場合
            elif insertion_index == len(tasks):
                return euclidean_distance(tasks[-1], new_task)

            # 挿入位置がリストの中間の場合
            else:
                distance_before_insertion = euclidean_distance(tasks[insertion_index - 1], tasks[insertion_index])
                distance_after_insertion = euclidean_distance(tasks[insertion_index - 1], new_task) + \
                                        euclidean_distance(new_task, tasks[insertion_index])
                return distance_after_insertion - distance_before_insertion
        
            

        min_additional_distance = float('inf')
        optimal_position = None

        for insertion_index in range(len(vehicle.tasks) + 1):

        # 時間窓制約を満たしているかを確認します
            copy_tasks = copy.deepcopy(vehicle.tasks)
            copy_tasks.insert(insertion_index, new_task)
            if route_check(copy_tasks,vehicle.dep_x,vehicle.dep_y):

                additional_distance = calculate_additional_distance(vehicle.tasks, new_task, insertion_index)
                if additional_distance < min_additional_distance:
                    min_additional_distance = additional_distance
                    optimal_position = insertion_index
    
        return optimal_position

def assign_tasks_to_vehicles_with_insert(tasks, vehicles,run_num,dep_x, dep_y):
    # global run_num
    for task in tasks:
        if run_num == 0:
            new_vehicle = Vehicle(run_num, max_weight,dep_x, dep_y)
            new_vehicle.tasks.append(task)
            new_vehicle.current_weight += task.weight
            vehicles.append(new_vehicle)
            run_num += 1
        else:
            apt_cars=[]
            min_cost = 100000
            min_cost_car = None
            for car in vehicles:
                if cost_back(car, task) < min_cost:
                    min_cost = cost_back(car, task)
                    min_cost_car = car
            if min_cost_car == None:
                new_vehicle = Vehicle(run_num, max_weight,dep_x, dep_y)
                new_vehicle.tasks.append(task)
                new_vehicle.current_weight += task.weight
                vehicles.append(new_vehicle)
                run_num += 1
            else:
                task_add(min_cost_car,task,dep_x,dep_y)
    return run_num

def read_task(filename, tasks):
    global max_weight
    max_x_coordinate = float('-inf')  # 初期値を負の無限大に設定
    max_y_coordinate = float('-inf')  # 初期値を負の無限大に設定
    max_due_date = float('-inf')  # 初期値を負の無限大に設定

    with open(filename, "r") as file:
        current_section = "no"
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line == "VEHICLE":
                current_section = "VEHICLE"
                continue
            elif line == "CUSTOMER":
                current_section = "CUSTOMER"
                continue

            if current_section == "VEHICLE":
                if "NUMBER" in line:
                    continue
                parts = line.split()
                max_num, max_weight = map(int, parts)

            if current_section == "CUSTOMER":
                if "CUST NO." in line:
                    continue
                parts = line.split()
                id, x_coordinate, y_coordinate, weight, ready_time, due_date, service_time = map(int, parts)
                task = Task(id, x_coordinate, y_coordinate, weight, ready_time, due_date, service_time)

                tasks.append(task)

                # 最大値の更新
                max_x_coordinate = max(max_x_coordinate, x_coordinate)
                max_y_coordinate = max(max_y_coordinate, y_coordinate)
                max_due_date = max(max_due_date, due_date)

    return [max(max_x_coordinate, max_y_coordinate), max_due_date]


class exchange_tasks:
    def __init__(self, taskA, taskB, id, vehicleA, vehicleB) :
        self.id = id
        self.vehicleA = vehicleA
        self.vehicleB = vehicleB
        self.taskA = taskA
        self.taskB = taskB
        
