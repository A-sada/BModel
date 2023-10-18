from Task import Task,Offer,Nego
# 車両（エージェント）クラス
from negmas import AspirationNegotiator, ResponseType,SAONegotiator

from negmas import SAOMechanism, AspirationNegotiator, Issue, ResponseType
from typing import Optional, List
from VRPTW_functions import euclidean_distance
import copy
import math

class Vehicle(SAONegotiator):
    def __init__(self, id, max_weight):
        super().__init__()
        self.id = id  # 車両のID
        #self.x_coordinate = x_coordinate  # 現在地のx座標
        #self.y_coordinate = y_coordinate  # 現在地のy座標
        self.max_weight = max_weight  # 最大積載量
        self.current_weight = 0  # 現在の積載量
        self.propose_task = 512
        self.tasks = []  # 割り当てられたタスクのリスト
        self.offer_nego_list=[] #自分の交渉リスト・自分が提案側ならここにスタート時の交渉内容を保存する
        self.next_nego={} #交渉IDと自分の交渉リストインデックスと対応
        self.offer_flag = 0
        

    def step(self):
        self.offer_flag=0
        return
    
    def propose(self, state) -> Optional["Outcome"]:
        # タスク交換の提案を行うロジック
        return {"taskA": self.tasks[0], "taskB": self.tasks[1]}  # 例として、タスクリストの最初の2つのタスクを提案

    def respond(self, state, offer: "Outcome") -> "ResponseType":
        # 提案されたタスク交換を評価するロジック
        if offer["taskA"] in self.tasks and offer["taskB"] in self.tasks:  # タスクが自分のリストにある場合
            return ResponseType.ACCEPT_OFFER
        return ResponseType.REJECT_OFFER
    
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
    

    def offer_on_negotiation(self,run_cars,offer_id):
        #list_return = copy.deepcopy(self.offer_nego_list)
        list_return =[]
        ofe=Offer(offer_id,self.id,run_cars[0].id,self.tasks[0])
        offer_id += 1
        self.offer_nego_list.append(ofe)
        list_return = copy.deepcopy(self.offer_nego_list)
        return self.offer_nego_list
    
    def check_offer(self,task):
        return self.check_task(task)
    
    def find_index(self,obj_list, target_id):
        index = 0
        for obj in obj_list:
            if obj.id == target_id:
                return index
            index += 1
        return None
    
    def accept_offer(self,offer,neg_id):
        if offer not in self.offer_nego_list:
            print("error- vehicleA have not task")
            return False
        self.next_nego[neg_id]=offer
        return

    #行われる交渉IDを受け取る，この値から自分が提案者側かどうかを判断する，
    def start_negotiation(self,neg_id):
        neg_task = self.next_nego.get(neg_id)
        if neg_task != None:
            self.propose_task = neg_task
            #propse_taskはタスクリストのインデックス
            self.offer_flag = 1
        return
    
    def end_negotiation(self):
        self.offer_flag = 0
        return
    
    def sign_contract(self,partner,taskA,taskB):

        return True

    def pop(self,task):
        for i, obj in enumerate(self.tasks):
            if obj.id == task.id:
                del self.tasks[i]
                return True
        return False
    
    def add(self,new_task):
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
    
    def bulletin_update(self):
        return 
    
    def calculate_total_cost(distance_cost, slack_time, late_penalty, alpha=1, beta=0):
        return distance_cost + alpha * slack_time + beta * late_penalty

    def least_cost_time_sensitive_insertion(self,route, task_to_insert, alpha=1, beta=1):
        min_cost = float('inf')
        best_position = None
        
        for i in range(1, len(route)):
            distance_cost = euclidean_distance(route[i-1], task_to_insert) + euclidean_distance(task_to_insert, route[i]) - euclidean_distance(route[i-1], route[i])

            # Calculate slack time and late penalty (for simplicity, set to 0 here; you should implement this part)
            slack_time = 0
            late_penalty = 0

            total_cost = self.calculate_total_cost(distance_cost, slack_time, late_penalty, alpha, beta)
            
            if total_cost < min_cost:
                min_cost = total_cost
                best_position = i
                
        if best_position is not None:
            route.insert(best_position, task_to_insert)
        

