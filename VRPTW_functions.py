import math
from classes import Task,pac_task
# タスク間または車両とタスク間のユークリッド距離を計算する関数
def euclidean_distance(task1, task2):
    return (int)(math.sqrt((task1.x_coordinate - task2.x_coordinate)**2 + (task1.y_coordinate - task2.y_coordinate)**2))

def slack_time_list(self, route,slist):
        total_time = 0  # total time spent so far in the route
        slack_time = 0
        
        for i in range(len(route)):
            task = route[i]           
            
            if i != 0:
                total_time += euclidean_distance(route[i-1], task)
                slack_time[i] = max(0, task.due_date - total_time)
                # Wait for the task's service to start if necessary
                if total_time < task.ready_time:
                    total_time = task.ready_time
                
                total_time += task.service_time
            else:
                distance = euclidean_distance(Task(0,0,0,0,0,0,0), task)
                if distance < task.ready_time:
                    distance = task.ready_time
                total_time += distance
                
                total_time += task.service_time
            
        return slack_time

def find_time_zone(t, zones):
    for zone_name, (start, end) in zones.items():
        if start <= t < end:
            return zone_name
    return False  # t がどの時間帯にも属さない場合

import pandas as pd

def find_neighboring_areas(area):
    alphabet_part = area[0]  # 最初の文字（アルファベット）
    number_part = int(area[1:])  # 2文字目以降（数字）
    # アルファベットの前後の値を決定
    prev_alphabet = chr(ord(alphabet_part) - 1) if ord(alphabet_part) > ord('A') else None
    next_alphabet = chr(ord(alphabet_part) + 1) 

    # 隣接するエリアのリストを作成
    neighboring_areas = []
    for alpha in [prev_alphabet, alphabet_part, next_alphabet]:
        if alpha:
            for num in [number_part - 1, number_part, number_part + 1]:
                if num >= 0:  # エリア番号は正の数でなければならない
                    neighboring_areas.append(f"{alpha}{num}")

    return neighboring_areas

def find_vehicles_in_neighboring_areas(time, area, df):
    neighbors = find_neighboring_areas(area)
    vehicles = []
    if time in df.columns:
        for neighbor in neighbors:
            # neighborがtime列に存在するかチェック
            if neighbor in df[time].values:
                matching_vehicles = df[df[time] == neighbor]['id'].tolist()
                vehicles.extend(matching_vehicles)

    return vehicles

def find_vehicle_by_id(vehicle_id, vehicles):
    for vehicle in vehicles:
        if vehicle.id == vehicle_id:
            return vehicle
    return None  # IDと一致するvehicleが見つからなかった場合

def earliest_start_time_list(tasks : list[pac_task]):
    #リストで計算する
    current_time = tasks[0].task.ready_time
    i = 0 
    for task in tasks:
        if i == 0:
            task.earliest_start_time = current_time
            current_time += task.task.service_time
            i += 1
            pre_task =task
        else:
            current_time += euclidean_distance(pre_task.task,task.task)

            task.earliest_start_time = current_time
            current_time += task.task.service_time
            pre_task =task
            


def calculate_earliest_start_time(previous_task, current_task,current_time):
    # 前のタスクのサービス終了時刻がcurrent_time
    current_time += euclidean_distance(previous_task.task,current_task.task)
    current_time = max(current_task.task.ready_time,current_time)

    return current_time

def latest_start_time_list(tasks : list[pac_task]):
    current_time = tasks[-1].task.due_date
    i = 0
    for task in reversed(tasks):
        if i == 0:
            task.late_start_time = current_time
            pre_task =task
            i += 1
        else:
            current_time -= euclidean_distance(pre_task.task,task.task)
            current_time -= task.task.service_time
            task.late_start_time = current_time
            current_time = min(current_time,task.task.due_date)
            task.late_start_time = current_time
            pre_task = task

    