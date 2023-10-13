
from VRPTW_BASE import assign_tasks_to_vehicles_with_insert,read_task
from Vehicle import Vehicle
from Task import Task,Offer,Nego
import random
from negmas import SAOMechanism, AspirationNegotiator, Issue, ResponseType
from typing import Optional, List
from datetime import datetime
from Negotiator import Nego1

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

#車両とIDの紐付け＿辞書
cars_id = {}
for vehicle in vehicles:
    cars_id[vehicle.id] = vehicle

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

from collections import deque
#全車両から交渉の提案を受け付ける
Offer_list = deque()
offer_id=0
for vehicle in vehicles:
    lst=vehicle.offer_on_negotiation(vehicles,offer_id)
    Offer_list.append(lst)
    offer_id += len(lst)

# 交渉リストを初期化
negotiation_list = []
negotiation_id = 0
# Offer_list内の各リストをループで処理
for lst in Offer_list:
    
    # 各リスト内のオファーをループで処理
    for offer in lst:
        
        # オファーに含まれる車両IDをキーとして、対応する車両オブジェクトを取得
        cars_A = cars_id[offer.vehicleA]
        cars_B = cars_id[offer.vehicleB]
        
        # 車両Bがオファーのタスクを受け入れられるかどうかをチェック
        if cars_B.check_offer(offer.task) == True:
            
            # 車両Bがオファーを受け入れることができる場合、オファーを交渉リストに追加
            negotiation_list.append(Nego(negotiation_id,cars_A,cars_B))
            
            # 車両Aにオファーの受け入れを通知
            cars_A.accept_offer(offer,negotiation_id)
            negotiation_id += 1


result=[]
for neg in negotiation_list:
    neg.vehicleA.start_negotiation(neg.id)
    result.append(Nego1(neg.vehicleA,neg.vehicleB))
    neg.vehicleA.end_negotiation()
print(result)




        

