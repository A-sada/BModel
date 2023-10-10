import random

import math
from Vehicle_Task import Vehicle,Task


# タスク間または車両とタスク間のユークリッド距離を計算する関数
def euclidean_distance(task1, task2):
    return math.sqrt((task1.x_coordinate - task2.x_coordinate)**2 + (task1.y_coordinate - task2.y_coordinate)**2)
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def is_task_assignable_with_or_tools(vehicle, new_task):
    global max_weight
    # タスクがまだ割り当てられていない場合や、車両にまだタスクが割り当てられていない場合
    if len(vehicle.tasks) > 4:
        return False
    if vehicle.current_weight + new_task.weight > max_weight:
        return False
    
    # 車両の開始位置から新しいタスクまでの距離を計算
    start_task = Task(0, 0, 0, 0, 0, 0, 0)  # 仮の開始位置
    travel_time_from_start = euclidean_distance(start_task, new_task)
    if travel_time_from_start <= new_task.due_date :
        if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, vehicle.tasks[0]) <= vehicle.tasks[0].due_date: 
            return True

    # 各タスク間での新しいタスクの挿入を試みる
    for i in range(len(vehicle.tasks) - 1):
        current_task = vehicle.tasks[i]
        next_task = vehicle.tasks[i + 1]

        # 現在のタスクの終了時間を計算
        current_task_end_time = current_task.ready_time + current_task.service_time

        # 新しいタスクへの移動に必要な時間を計算
        travel_time_to_new_task = euclidean_distance(current_task, new_task)

        # 新しいタスクのサービス終了時間を計算
        new_task_end_time = current_task_end_time + travel_time_to_new_task + new_task.service_time

        # 次のタスクへの移動に必要な時間を計算
        travel_time_to_next_task = euclidean_distance(new_task, next_task)

        # 次のタスクの開始時間を計算
        next_task_start_time = new_task_end_time + travel_time_to_next_task

        # 新しいタスクがdue_date前に終了し、次のタスクが時間内に開始できるかどうかを確認
        if current_task_end_time + travel_time_to_new_task <= new_task.due_date and next_task_start_time <= next_task.due_date:
            return True

    # すべてのタスクの後に新しいタスクを追加する場合の判定
    last_task = vehicle.tasks[-1]
    last_task_end_time = last_task.ready_time + last_task.service_time
    travel_time_to_new_task = euclidean_distance(last_task, new_task)
    if last_task_end_time + travel_time_to_new_task <= new_task.due_date:
        return True

    return False

def task_go(vehicle, new_task):
    # 車両の開始位置から新しいタスクまでの距離を計算
    start_task = Task(0, 0, 0, 0, 0, 0, 0)  # 仮の開始位置
    travel_time_from_start = euclidean_distance(start_task, new_task)
    if travel_time_from_start <= new_task.due_date :
        if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, vehicle.tasks[0]) <= vehicle.tasks[0].due_date: 
            vehicle.tasks.insert(0,new_task)
            vehicle.current_weight += new_task.weight
            return 

    # 各タスク間での新しいタスクの挿入を試みる
    for i in range(len(vehicle.tasks) - 1):
        current_task = vehicle.tasks[i]
        next_task = vehicle.tasks[i + 1]

        # 現在のタスクの終了時間を計算
        current_task_end_time = current_task.ready_time + current_task.service_time

        # 新しいタスクへの移動に必要な時間を計算
        travel_time_to_new_task = euclidean_distance(current_task, new_task)

        # 新しいタスクのサービス終了時間を計算
        new_task_end_time = current_task_end_time + travel_time_to_new_task + new_task.service_time

        # 次のタスクへの移動に必要な時間を計算
        travel_time_to_next_task = euclidean_distance(new_task, next_task)

        # 次のタスクの開始時間を計算
        next_task_start_time = new_task_end_time + travel_time_to_next_task

        # 新しいタスクがdue_date前に終了し、次のタスクが時間内に開始できるかどうかを確認
        if current_task_end_time + travel_time_to_new_task <= new_task.due_date and next_task_start_time <= next_task.due_date:
            vehicle.tasks.insert(i+1,new_task)
            vehicle.current_weight += new_task.weight
            return 

    # すべてのタスクの後に新しいタスクを追加する場合の判定
    last_task = vehicle.tasks[-1]
    last_task_end_time = last_task.ready_time + last_task.service_time
    travel_time_to_new_task = euclidean_distance(last_task, new_task)
    if last_task_end_time + travel_time_to_new_task <= new_task.due_date:
       vehicle.tasks.append(new_task)
       vehicle.current_weight += new_task.weight

def assign_tasks_to_vehicles_with_insert(tasks, vehicles,run_num):
    # global run_num
    for task in tasks:
        if run_num == 0:
            new_vehicle = Vehicle(run_num, max_weight)
            new_vehicle.tasks.append(task)
            new_vehicle.current_weight += task.weight
            vehicles.append(new_vehicle)
            run_num += 1
        else:
            apt_cars=[]
            for car in vehicles:
                if is_task_assignable_with_or_tools(car, task) == True:
                    apt_cars.append(car)
            if len(apt_cars) == 0:
                new_vehicle = Vehicle(run_num, max_weight)
                new_vehicle.tasks.append(task)
                new_vehicle.current_weight += task.weight
                vehicles.append(new_vehicle)
                run_num += 1
            elif len(apt_cars)==1:
                task_go(apt_cars[0],task)
            else:
                rad = random.randint(0, len(apt_cars)-1)
                task_go(apt_cars[rad],task)


def read_task(filename,tasks):
    global max_weight
    with open(filename, "r") as file:
        current_section="no"
        for line in file:
            line = line.strip()  # 末尾の空白を削除
            if not line:  # 空行をスキップ
                continue
            # セクションの切り替え
            if line == "VEHICLE":
                current_section = "VEHICLE"
                continue
            elif line == "CUSTOMER":
                current_section = "CUSTOMER"
                continue
            
            # 各セクションに応じてデータを処理
            if current_section == "VEHICLE":
                if "NUMBER" in line:
                        continue  # ヘッダー行はスキップ 
                parts = line.split()
                max_num, max_weight= map(int, parts)
            if current_section == "CUSTOMER":
                if "CUST NO." in line:
                    continue  # ヘッダー行はスキップ
                parts = line.split()
                id, x_coordinate, y_coordinate, weight, ready_time, due_date, service_time = map(int, parts)
                task = Task(id, x_coordinate, y_coordinate, weight, ready_time, due_date, service_time)
                tasks.append(task)


class exchange_tasks:
    def __init__(self, taskA, taskB, id, vehicleA, vehicleB) :
        self.id = id
        self.vehicleA = vehicleA
        self.vehicleB = vehicleB
        self.taskA = taskA
        self.taskB = taskB
        
