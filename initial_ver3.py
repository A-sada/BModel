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
def aaaa(task_to_route):
    routes = [
    [98, 96, 95, 94, 92, 93, 97, 100, 99],  # Route 1
    [57, 55, 54, 53, 56, 58, 60, 59],        # Route 2
    [13, 17, 18, 19, 15, 16, 14, 12],        # Route 3
    [32, 33, 31, 35, 37, 38, 39, 36, 34],    # Route 4
    [81, 78, 76, 71, 70, 73, 77, 79, 80],    # Route 5
    [43, 42, 41, 40, 44, 46, 45, 48, 51, 50, 52, 49, 47],  # Route 6
    [90, 87, 86, 83, 82, 84, 85, 88, 89, 91],  # Route 7
    [67, 65, 63, 62, 74, 72, 61, 64, 68, 66, 69],  # Route 8
    [5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1, 75],   # Route 9
    [20, 24, 25, 27, 29, 30, 28, 26, 23, 22, 21]  # Route 10
    ]


    # タスクIDとルート番号をマッピングする辞書を作成
    for route_number, tasks in enumerate(routes, start=1):
        for task_id in tasks:
            task_to_route[task_id] = route_number


def assign_tasks_to_vehicles_with_insert(tasks, vehicles,run_num,dep_x, dep_y):
    # global run_num
    route_id ={}
    aaaa(route_id)
    print(route_id)
    for i in range(10):
        new_vehicle = Vehicle(run_num, max_weight,dep_x, dep_y)
        vehicles.append(new_vehicle)
    for task in tasks:
        car_id = route_id[task.id]
        vehicle = vehicles[car_id-1]
        if len(vehicle.tasks) == 0:
            vehicle.tasks.append(task)
            vehicle.current_weight += task.weight
        else:
            task_add(vehicle,task,dep_x,dep_y)
    for vehicle in vehicles:
        print(vehicle.tasks)
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
        
