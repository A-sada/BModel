class Task:
    def __init__(self, id, x_coordinate, y_coordinate, weight, ready_time, due_date, service_time):
        self.id = id  # タスク（顧客）のID
        self.x_coordinate = x_coordinate  # 配送先のx座標
        self.y_coordinate = y_coordinate  # 配送先のy座標
        self.weight = weight  # 荷物の重量またはサイズ
        self.ready_time = ready_time  # 配送可能な最早時間
        self.due_date = due_date  # 配送締切時間
        self.service_time = service_time  # サービスにかかる時間
# 車両（エージェント）クラス
from negmas import AspirationNegotiator, ResponseType
from negmas import SAOMechanism, AspirationNegotiator, Issue, ResponseType
from typing import Optional, List
from VRPTW_functions import euclidean_distance

class Vehicle(AspirationNegotiator):
    def __init__(self, id, max_weight):
        self.id = id  # 車両のID
        #self.x_coordinate = x_coordinate  # 現在地のx座標
        #self.y_coordinate = y_coordinate  # 現在地のy座標
        self.max_weight = max_weight  # 最大積載量
        self.current_weight = 0  # 現在の積載量
        self.tasks = []  # 割り当てられたタスクのリスト
        self.offer_nego_list=[] #自分の交渉リスト・自分が提案側ならここにスタート時の交渉内容を保存する
        self.next_nego={} #交渉IDと自分の交渉リストインデックスと対応
        self.offer_flag = 0
        super().__init__()

    def propose(self, state) -> Optional["Outcome"]:
        # タスク交換の提案を行うロジック
        return {"taskA": self.tasks[0], "taskB": self.tasks[1]}  # 例として、タスクリストの最初の2つのタスクを提案

    def respond(self, state, offer: "Outcome") -> "ResponseType":
        # 提案されたタスク交換を評価するロジック
        if offer["taskA"] in self.tasks and offer["taskB"] in self.tasks:  # タスクが自分のリストにある場合
            return ResponseType.ACCEPT_OFFER
        return ResponseType.REJECT_OFFER
    
    #タスクの挿入が可能かチェック
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
    

    def offer_on_negotiation(self):
        #list_return = copy.deepcopy(self.offer_nego_list)
        list_return =[]
        list_return.append(self.tasks[0].id)
        return list_return
    
    def check_offer(self,task):
        if check_task(task) == True:
            return True
        return False
    
    def now_negotiation():
    #行われる交渉IDを受け取る，この値から自分が提案者側かどうかを判断する，
        return
    
    

