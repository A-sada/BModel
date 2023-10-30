from classes import Task,Offer,Nego
# 車両（エージェント）クラス
from negmas import AspirationNegotiator, ResponseType,SAONegotiator

from negmas import SAOMechanism, AspirationNegotiator, Issue, ResponseType
from typing import Optional, List
from VRPTW_functions import euclidean_distance
import copy
import math

import random
class Vehicle_Base():
    def __init__(self, id, max_weight):
        super().__init__()
        self.id = id  # 車両のID
        #self.x_coordinate = x_coordinate  # 現在地のx座標
        #self.y_coordinate = y_coordinate  # 現在地のy座標
        self.max_weight = max_weight  # 最大積載量
        self.current_weight = 0  # 現在の積載量
        self.propose_task : Task
        self.tasks = []  # 割り当てられたタスクのリスト
        self.offer_nego_list=[] #自分の交渉リスト・自分が提案側ならここにスタート時の交渉内容を保存する
        self.next_nego={} #交渉IDと自分の交渉リストインデックスと対応
        self.offer_flag = 0
        self.rout_pacs = []
        self.taskA = 0

    def step(self):
        self.offer_flag=0
        return
    
    def accept_or_reject(self,offer):

        #交渉の受け入れの是非を実装
        if self.check_offer(offer.get("taskB")) == True:
            return True
        else:
            return False
    
    def make_propose(self):
        return {"taskA": self.propose_task, "taskB": self.tasks[random.randint(0,len(self.tasks - 1))]}
  
    #タスクの挿入が可能かチェック->true or false
    def check_task(self,new_task):
        # 車両の開始位置から新しいタスクまでの距離を計算
        start_task = Task(0, 0, 0, 0, 0, 0, 0)  # 仮の開始位置
        travel_time_from_start = euclidean_distance(start_task, new_task)
        if travel_time_from_start <= new_task.due_date :
            if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, self.tasks[0]) <= self.tasks[0].due_date: 
                return True

        # 各タスク間での新しいタスクの挿入を試みる
        for i in range(len(self.tasks) - 1):
            current_task = self.tasks[i]
            next_task = self.tasks[i + 1]

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
        last_task = self.tasks[-1]
        last_task_end_time = last_task.ready_time + last_task.service_time
        travel_time_to_new_task = euclidean_distance(last_task, new_task)
        if last_task_end_time + travel_time_to_new_task <= new_task.due_date:
            return True
        return False
    
    #交渉の提案を行う-> 希望する交渉のリストを送信
    def offer_on_negotiation(self,run_cars,offer_id):
        #list_return = copy.deepcopy(self.offer_nego_list)
        #list_return =[]
        ofe=Offer(offer_id,self.id,run_cars[0].id,self.tasks[0])
        offer_id += 1
        self.offer_nego_list.append(ofe)
        #list_return = copy.deepcopy(self.offer_nego_list)
        return self.offer_nego_list
    
    #提案された交渉について応じるかどうかを判断　->応じるならTrue,応じないならFalse
    def check_offer(self,task):
        return self.check_task(task)
    
    #リストからIDの一致する要素のインデックスを返す
    def find_index(self,obj_list, target_id):
        index = 0
        for obj in obj_list:
            if obj.id == target_id:
                return index
            index += 1
        return None
    
    #提案した交渉が相手に受け入れられたら呼び出される．
    def accept_offer(self,offer,neg_id):
        if offer not in self.offer_nego_list:
            print("error- vehicleA have not task")
            return False
        #実施する交渉のリスト（自分が提案したタスクのみ）
        self.next_nego[neg_id]=offer
        return

    #行われる交渉IDを受け取る，この値から自分が提案者側かどうかを判断する，
    def start_negotiation(self,neg_id):
        neg_task = self.next_nego.get(neg_id)
        if neg_task != None:
            self.propose_task = neg_task
            #propse_taskはタスクリストのインデックス
            self.offer_flag = 1
            #自分が提案した交渉ならフラグがたつ
        return
    

    #交渉終了時に呼び出される
    def end_negotiation(self):
        self.offer_flag = 0
        return
    
    #署名戦略
    def sign_contract(self,partner,taskA,taskB):

        return True
    
    #ルートから該当するタスクを削除
    def pop(self,task):
        for i, obj in enumerate(self.tasks):
            if obj.id == task.id:
                del self.tasks[i]
                return True
        return False
    
    #とにかく挿入可能な場所に挿入する
    def add_old(self,new_task):
        # 車両の開始位置から新しいタスクまでの距離を計算
        start_task = Task(0, 0, 0, 0, 0, 0, 0)  # 仮の開始位置
        travel_time_from_start = euclidean_distance(start_task, new_task)
        if travel_time_from_start <= new_task.due_date :
            if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, self.tasks[0]) <= self.tasks[0].due_date: 
                self.tasks.insert(0,new_task)
                self.current_weight += new_task.weight
                return True

        # 各タスク間での新しいタスクの挿入を試みる
        for i in range(len(self.tasks) - 1):
            current_task = self.tasks[i]
            next_task = self.tasks[i + 1]

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
                self.tasks.insert(i+1,new_task)
                self.current_weight += new_task.weight
                return True

        # すべてのタスクの後に新しいタスクを追加する場合の判定
        last_task = self.tasks[-1]
        last_task_end_time = last_task.ready_time + last_task.service_time
        travel_time_to_new_task = euclidean_distance(last_task, new_task)
        if last_task_end_time + travel_time_to_new_task <= new_task.due_date:
            self.tasks.append(new_task)
            self.current_weight += new_task.weight
            return True
        return False
    
    #コストが最小となる場所に挿入する
    def add(self, new_task):
        return self.least_cost_time_sensitive_insertion(self.tasks, new_task, 1)
    
    #掲示板の更新
    def bulletin_update(self):
        return 
    
    #スラックタイムの計算
    def calculate_slack_time(self, route, position_to_insert, task_to_insert):
        total_time = 0  # total time spent so far in the route
        slack_time = 0
        
        for i in range(len(route)):
            task = route[i]
            
            if i == position_to_insert:
                # Assuming we insert the new task here
                total_time += euclidean_distance(route[i-1], task_to_insert)
                total_time += task_to_insert.service_time
                
                slack_time += max(0, task_to_insert.due_date - total_time)
                
                total_time += euclidean_distance(task_to_insert, task)
                total_time += task.service_time
                
            else:
                if i != 0:
                    total_time += euclidean_distance(route[i-1], task)
                    total_time += task.service_time
                else:
                    distance = euclidean_distance(Task(0,0,0,0,0,0,0), task)
                    if distance < task.ready_time:
                        distance = task.ready_time
                    total_time += distance
                    total_time += task.service_time

            slack_time += max(0, task.due_date - total_time)
            
        return slack_time

    def least_cost_time_sensitive_insertion(self ,route, new_task, alpha):
        min_cost = float('inf')
        best_position = None
        cost = 0
        # 車両の開始位置から新しいタスクまでの距離を計算
        start_task = Task(0, 0, 0, 0, 0, 0, 0)  # 仮の開始位置
        travel_time_from_start = euclidean_distance(start_task, new_task)
        if travel_time_from_start <= new_task.due_date :
            if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, self.tasks[0]) <= self.tasks[0].due_date: 
                cost = self.calculate_slack_time(self.tasks, 0, new_task)
                if min_cost > cost:
                    min_cost = cost
                    best_position = 0


        # 各タスク間での新しいタスクの挿入を試みる
        for i in range(len(self.tasks) - 1):
            current_task = self.tasks[i]
            next_task = self.tasks[i + 1]

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
                cost = self.calculate_slack_time(self.tasks,i+1,new_task)
                if min_cost > cost:
                    min_cost = cost
                    best_position = i+1
        if best_position != None:
            self.tasks.insert(best_position,new_task)
            return True
        return False

