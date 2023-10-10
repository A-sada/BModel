
from VRPTW_BASE import assign_tasks_to_vehicles_with_insert,read_task
from Vehicle_Task import Task,Vehicle
import random
from negmas import SAOMechanism, AspirationNegotiator, Issue, ResponseType
from typing import Optional, List
from datetime import datetime

run_num = 0
tasks = []  # タスクを保存するためのリスト
vehicles = []
no_runs=[]
# taskのリスト化
import os
# ディレクトリの名前を指定
base_directory_name = "output_files"

# 現在の日時を取得して、文字列形式に変換
current_time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

#if not os.path.exists(base_directory_name):
#    os.makedirs(base_directory_name)
# 実行日時を名前とするフォルダのパスを生成
directory_name = os.path.join(base_directory_name, current_time_str)

# ディレクトリが存在しない場合、作成（親ディレクトリも含めて）
os.makedirs(directory_name, exist_ok=True)
read_task("C1_10_1.txt",tasks)
random.shuffle(tasks)
# タスクを車両に割り当て（時間制約を含む）
assign_tasks_to_vehicles_with_insert(tasks, vehicles,run_num)
from collections import deque

count =0
# 結果を表示（テスト用）
i=0
filename = os.path.join(directory_name, f"Step-0.txt") 
with open(filename, 'w') as f:
    for vehicle in vehicles:
        task_ids = [task.id for task in vehicle.tasks]
        # ファイル名を生成
        f.write(f"Vehicle {vehicle.id} has tasks {task_ids} with total weight {vehicle.current_weight}.\n")
        if len(task_ids) == 1:
            count += 1
print(count)
from queue import Queue
from collections import deque
#全車両から交渉の提案を受け付ける
Offer_list = deque()
for vehicle in vehicles:
    Offer_list.append(vehicle.offer_on_negotiation())


