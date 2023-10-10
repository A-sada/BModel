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

    def propose(self, state) -> Optional["Outcome"]:
        # タスク交換の提案を行うロジック
        return {"taskA": self.tasks[0], "taskB": self.tasks[1]}  # 例として、タスクリストの最初の2つのタスクを提案

    def respond(self, state, offer: "Outcome") -> "ResponseType":
        # 提案されたタスク交換を評価するロジック
        if offer["taskA"] in self.tasks and offer["taskB"] in self.tasks:  # タスクが自分のリストにある場合
            return ResponseType.ACCEPT_OFFER
        return ResponseType.REJECT_OFFER
    
    def offer_on_negotiatin():
        return
    
    def now_negotiation():
    #行われる交渉IDを受け取る，この値から自分が提案者側かどうかを判断する，
        return
    
    

