import random

import math
from Strategy_Vehicle_ver1 import Vehicle
from classes import Task
from VRPTW_functions import euclidean_distance


def is_task_assignable_with_or_tools(vehicle, new_task,dep_x,dep_y):
    global max_weight
    # タスクがまだ割り当てられていない場合や、車両にまだタスクが割り当てられていない場合
    if len(vehicle.tasks) > 4:
        return False
    if vehicle.current_weight + new_task.weight > max_weight:
        return False
    current_time = 0
    # 車両の開始位置から新しいタスクまでの距離を計算
    start_task = Task(0, dep_x, dep_y, 0, 0, 0, 0)  # 仮の開始位置
    travel_time_from_start = max(euclidean_distance(start_task, new_task),new_task.ready_time)
    #if travel_time_from_start <= new_task.due_date :
    if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, vehicle.tasks[0]) <= vehicle.tasks[0].due_date: 
        return True
    current_task = vehicle.tasks[0]
    next_task = None
    pre_task = None
    # 各タスク間での新しいタスクの挿入を試みる
    for i in range(len(vehicle.tasks) - 1):
        current_task = vehicle.tasks[i]
        next_task = vehicle.tasks[i + 1]
        if i == 0:
            current_time = max(euclidean_distance(start_task, current_task),current_task.ready_time)
            current_time += current_task.service_time
            # 現在のタスクの終了時間を計算
        else:
            current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
            #current_timeをカレントタスクの開始時間に更新
            current_time += current_task.service_time
        
        # 新しいタスクへの移動に必要な時間を計算
        travel_time_to_new_task = euclidean_distance(current_task, new_task)

        # 新しいタスクのサービス終了時間を計算
        new_task_end_time = current_time + travel_time_to_new_task + new_task.service_time

        # 次のタスクへの移動に必要な時間を計算
        travel_time_to_next_task = euclidean_distance(new_task, next_task)

        # 次のタスクの開始時間を計算
        next_task_start_time = new_task_end_time + travel_time_to_next_task
        
        pre_task = current_task
        # 新しいタスクがdue_date前に終了し、次のタスクが時間内に開始できるかどうかを確認
        if current_time + travel_time_to_new_task <= new_task.due_date and next_task_start_time <= next_task.due_date:
            return True
    #current_timeは最後から二番目のタスクの終了時間
    if next_task != None:
        current_task = next_task
        current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
        current_time += current_task.service_time
        next_task = new_task
        current_time = max(current_time + euclidean_distance(current_task, next_task),next_task.ready_time)
        if current_time <= next_task.due_date:
            return True
    else:
        current_task = vehicle.tasks[-1]
        pre_task = current_task
        current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
        current_time += current_task.service_time
        next_task = new_task
        current_time = max(current_time + euclidean_distance(current_task, next_task),next_task.ready_time)
        if current_time <= next_task.due_date:
            return True
    return False


def check_task(vehicle,new_task,dep_x,dep_y):
    dep_task = Task(0, dep_x, dep_y, 0, 0, 0, 0)  # 仮の開始位置
    current_time = 0
    travel_time_from_start = max(euclidean_distance(dep_task, new_task),new_task.ready_time)
    if travel_time_from_start <= new_task.due_date :
        if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, vehicle.tasks[0]) <= vehicle.tasks[0].due_date: 
            return True
    current_task = vehicle.tasks[0]
    next_task = None
    pre_task = None
    current_time = max(euclidean_distance(dep_task, current_task),current_task.ready_time)
    current_time += current_task.service_time
    if len(vehicle.tasks) != 1:
        for i in range(1,len(vehicle.tasks)-1):
            #current_timeはcurrent_taskへの到着時刻となっている
            current_task = vehicle.tasks[i]
            next_task = vehicle.tasks[i + 1]
            current_time = max(current_time, current_task.ready_time)
            current_time += current_task.service_time
            
            # 新しいタスクへの移動に必要な時間を計算
            travel_time_to_new_task = euclidean_distance(current_task, new_task)

            # 新しいタスクのサービス終了時間を計算
            new_task_end_time = max(current_time + travel_time_to_new_task,new_task.ready_time) + new_task.service_time

            # 次のタスクへの移動に必要な時間を計算
            travel_time_to_next_task = euclidean_distance(new_task, next_task)

            # 次のタスクの開始時間を計算
            next_task_start_time = new_task_end_time + travel_time_to_next_task
            
            if current_time + travel_time_to_new_task <= new_task.due_date and next_task_start_time <= next_task.due_date:
                return True
            pre_task = current_task
            # 新しいタスクがdue_date前に終了し、次のタスクが時間内に開始できるかどうかを確認
            current_time = euclidean_distance(current_task, next_task)
    
    current_task = vehicle.tasks[-1]
    travel_time_to_new_task = euclidean_distance(current_task, new_task)
    if current_time + travel_time_to_new_task <= new_task.due_date:
        return True
    return False
def task_add(vehicle, new_task,dep_x, dep_y):
    dep_task = Task(0, dep_x, dep_y, 0, 0, 0, 0)  # 仮の開始位置
    current_time = 0
    travel_time_from_start = max(euclidean_distance(dep_task, new_task),new_task.ready_time)
    if travel_time_from_start <= new_task.due_date :
        if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, vehicle.tasks[0]) <= vehicle.tasks[0].due_date: 
            vehicle.tasks.insert(0,new_task)
            vehicle.current_weight += new_task.weight
            return 
            return True
    current_task = vehicle.tasks[0]
    next_task = None
    pre_task = None
    current_time = max(euclidean_distance(dep_task, current_task),current_task.ready_time)
    current_time += current_task.service_time
    if len(vehicle.tasks) != 1:
        for i in range(1,len(vehicle.tasks)-1):
            #current_timeはcurrent_taskへの到着時刻となっている
            current_task = vehicle.tasks[i]
            next_task = vehicle.tasks[i + 1]
            current_time = max(current_time, current_task.ready_time)
            current_time += current_task.service_time
            
            # 新しいタスクへの移動に必要な時間を計算
            travel_time_to_new_task = euclidean_distance(current_task, new_task)

            # 新しいタスクのサービス終了時間を計算
            new_task_end_time = max(current_time + travel_time_to_new_task,new_task.ready_time) + new_task.service_time

            # 次のタスクへの移動に必要な時間を計算
            travel_time_to_next_task = euclidean_distance(new_task, next_task)

            # 次のタスクの開始時間を計算
            next_task_start_time = new_task_end_time + travel_time_to_next_task
            
            if current_time + travel_time_to_new_task <= new_task.due_date and next_task_start_time <= next_task.due_date:
                vehicle.tasks.insert(i+1,new_task)
                vehicle.current_weight += new_task.weight

                return True
            pre_task = current_task
            # 新しいタスクがdue_date前に終了し、次のタスクが時間内に開始できるかどうかを確認
            current_time = euclidean_distance(current_task, next_task)
    
    current_task = vehicle.tasks[-1]
    travel_time_to_new_task = euclidean_distance(current_task, new_task)
    if current_time + travel_time_to_new_task <= new_task.due_date:
        vehicle.tasks.append(new_task)
        vehicle.current_weight += new_task.weight
        return True
    return False

def task_go(vehicle, new_task,dep_x, dep_y):
    # 車両の開始位置から新しいタスクまでの距離を計算
    start_task = Task(0, dep_x, dep_y, 0, 0, 0, 0)  # 仮の開始位置
    travel_time_from_start = max(euclidean_distance(start_task, new_task),new_task.ready_time)
    if travel_time_from_start <= new_task.due_date :
        if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, vehicle.tasks[0]) <= vehicle.tasks[0].due_date: 
            vehicle.tasks.insert(0,new_task)
            vehicle.current_weight += new_task.weight
            return 
    current_time = 0
    current_task = vehicle.tasks[0]
    next_task = None
    pre_task = None

    # 各タスク間での新しいタスクの挿入を試みる
    for i in range(len(vehicle.tasks) - 1):

        current_task = vehicle.tasks[i]
        next_task = vehicle.tasks[i + 1]
        if i == 0:
            current_time = max(euclidean_distance(start_task, current_task),current_task.ready_time)
            current_time += current_task.service_time
            i = 1
            # 現在のタスクの終了時間を計算
        else:
            current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
            #current_timeをカレントタスクの開始時間に更新
            current_time += current_task.service_time

        # 新しいタスクへの移動に必要な時間を計算
        travel_time_to_new_task = euclidean_distance(current_task, new_task)

        # 新しいタスクのサービス終了時間を計算
        new_task_end_time = current_time + travel_time_to_new_task + new_task.service_time

        # 次のタスクへの移動に必要な時間を計算
        travel_time_to_next_task = euclidean_distance(new_task, next_task)

        # 次のタスクの開始時間を計算
        next_task_start_time = new_task_end_time + travel_time_to_next_task

        pre_task = current_task
        # 新しいタスクがdue_date前に終了し、次のタスクが時間内に開始できるかどうかを確認
        if current_time + travel_time_to_new_task <= new_task.due_date and next_task_start_time <= next_task.due_date:
            vehicle.tasks.insert(i+1,new_task)
            vehicle.current_weight += new_task.weight
            return 

    # すべてのタスクの後に新しいタスクを追加する場合の判定
    if next_task != None:
        current_task = next_task
        current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
        current_time += current_task.service_time
        next_task = new_task
        current_time = max(current_time + euclidean_distance(current_task, next_task),next_task.ready_time)
        if current_time <= next_task.due_date:
            vehicle.tasks.append(new_task)
            vehicle.current_weight += new_task.weight
            return
    else:
        current_task = vehicle.tasks[0]
        current_time = max(euclidean_distance(start_task, current_task),current_task.ready_time)
        current_time += current_task.service_time
        next_task = new_task
        current_time = max(current_time + euclidean_distance(current_task, next_task),next_task.ready_time)
        if current_time <= next_task.due_date:
            vehicle.tasks.append(new_task)
            vehicle.current_weight += new_task.weight
            return
    return False

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
            for car in vehicles:
                if check_task(car, task,dep_x, dep_y) == True:
                    apt_cars.append(car)
            if len(apt_cars) == 0:
                new_vehicle = Vehicle(run_num, max_weight,dep_x, dep_y)
                new_vehicle.tasks.append(task)
                new_vehicle.current_weight += task.weight
                vehicles.append(new_vehicle)
                run_num += 1
            elif len(apt_cars)==1:
                task_add(apt_cars[0],task,dep_x,dep_y)
            else:
                rad = random.randint(0, len(apt_cars)-1)
                task_add(apt_cars[rad],task,dep_x,dep_y)


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
                print(task.ready_time)
                print(task.due_date)
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
        
