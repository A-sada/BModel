
from VRPTW_BASE import assign_tasks_to_vehicles_with_insert,read_task
from Vehicle_Task import Task,Vehicle
import random
from negmas import SAOMechanism, AspirationNegotiator, Issue, ResponseType
from typing import Optional, List
run_num = 0
tasks = []  # タスクを保存するためのリスト
vehicles = []
no_runs=[]
# taskのリスト化


read_task("C1_10_1.txt",tasks)
random.shuffle(tasks)
# タスクを車両に割り当て（時間制約を含む）
assign_tasks_to_vehicles_with_insert(tasks, vehicles,run_num)

count =0
# 結果を表示（テスト用）
for vehicle in vehicles:
    task_ids = [task.id for task in vehicle.tasks]
    print(f"Vehicle {vehicle.id} has tasks {task_ids} with total weight {vehicle.current_weight}.")
    if len(task_ids) == 1:
        count += 1
print(count)
#初期解のテキストファイル化
#全車両から交渉の提案を受け付ける
