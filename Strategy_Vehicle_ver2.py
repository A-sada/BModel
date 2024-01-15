from typing import List
from Vehicle import Vehicle_BASE
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter
from balletin_are_search import calculate_dynamic_area
from VRPTW_functions import find_time_zone,find_vehicles_in_neighboring_areas,find_vehicle_by_id, earliest_start_time_list, latest_start_time_list, euclidean_distance
from classes import Offer,Agree,pac_task,Task
import copy

class Vehicle(Vehicle_BASE):
#TypeA
    def __init__(self, id, max_weight, dep_x, dep_y):
        super().__init__(id, max_weight, dep_x, dep_y)

    def check_offer(self, task):
        if self.bulletin_board.n_steps / self.bulletin_board.max_steps < 0.5:
            return True
        return self.check_task(task)
        
    def offer_on_negotiation(self, run_cars, offer_id,vehicles):
        if len(self.tasks) < 3:
            for task in self.tasks:
                vehicles_in_neighbors=[]
                task_area = calculate_dynamic_area(task.x_coordinate,task.y_coordinate,self.bulletin_board.X, self.bulletin_board.n)
                task_time_zone = find_time_zone(task.ready_time,self.bulletin_board.zones)
                vehicles_in_neighbors = find_vehicles_in_neighboring_areas(task_time_zone, task_area, self.bulletin_board.area_board) #車両IDが帰ってくる
                
                vehicles_in_neighbors.extend(self.find_available_vehicles(self.bulletin_board.time_board, task.ready_time,task.due_date,vehicles))
                if self.id in vehicles_in_neighbors:
                    vehicles_in_neighbors.remove(self.id)

                for vehicle in vehicles_in_neighbors:
                    car = find_vehicle_by_id(vehicle, run_cars)
                    if car != None:
                        ofe=Offer(offer_id,self.id,car.id,task)
                        offer_id += 1
                        self.offer_nego_list.append(ofe)
                        
                return self.offer_nego_list
        coordinates = np.array([[task.x_coordinate, task.y_coordinate] for task in self.tasks])
        scaler = MinMaxScaler()
        normalized_coordinates = scaler.fit_transform(coordinates)
        
        # 実際のK-meansクラスタリング
        def calculate_sse_changes(sse):
            sse_changes = []
            for i in range(1, len(sse)):
                if sse[i-1] ==0:
                    sse_changes.append(0)
                else:
                    sse_changes.append((sse[i-1] - sse[i]) / sse[i-1])
            return sse_changes

        # データポイント（タスク）の総数を取得
        num_samples = len(normalized_coordinates)

        # クラスタ数の最大値を設定（データポイントの数に基づく）
        max_clusters = int(num_samples / 2)

        # エルボー法によるクラスタ数の決定
        sse = []
        for k in range(1, max_clusters + 1):  # クラスタ数は1からmax_clustersまで
            kmeans = KMeans(n_clusters=k, n_init=10)
            kmeans.fit(normalized_coordinates)
            sse.append(kmeans.inertia_)

        # SSEの減少率の変化を計算
        sse_changes = calculate_sse_changes(sse)
        if not sse_changes:
            optimal_clusters = 1
        
        else:
        # 最も大きな変化を示すクラスタ数を選択
            optimal_clusters = sse_changes.index(max(sse_changes)) + 2  # +2 は、インデックス補正（1から始まるクラスタ数と合わせるため）
        if optimal_clusters <= len(self.tasks):
            optimal_clusters = 2
        # 実際のK-meansクラスタリング
        kmeans = KMeans(n_clusters=optimal_clusters,n_init=10)
        kmeans.fit(normalized_coordinates)
        task_clusters = kmeans.labels_

        # 各クラスタのタスク数を計算
        cluster_counts = Counter(task_clusters)

        # 最もタスクが多いクラスタを特定
        most_common_cluster = cluster_counts.most_common(1)[0][0]

        # 最もタスクが多いクラスタ以外に分類されたタスクのリスト
        other_cluster_tasks = [task for task, cluster in zip(self.tasks, task_clusters) if cluster != most_common_cluster]
        

        for task in other_cluster_tasks:
            vehicles_in_neighbors=[]
            task_area = calculate_dynamic_area(task.x_coordinate,task.y_coordinate,self.bulletin_board.X, self.bulletin_board.n)
            task_time_zone = find_time_zone(task.ready_time,self.bulletin_board.zones)
            vehicles_in_neighbors = find_vehicles_in_neighboring_areas(task_time_zone, task_area, self.bulletin_board.area_board) #車両IDが帰ってくる
            vehicles_in_neighbors.extend(self.find_available_vehicles(self.bulletin_board.time_board, task.ready_time,task.due_date,vehicles))
            if self.id in vehicles_in_neighbors:
                vehicles_in_neighbors.remove(self.id)

            for vehicle in vehicles_in_neighbors:
                car = find_vehicle_by_id(vehicle, run_cars)
                if car != None:
                    ofe=Offer(offer_id,self.id,car.id,task)
                    offer_id += 1
                    self.offer_nego_list.append(ofe)
                    
        #list_return = copy.deepcopy(self.offer_nego_list)
        return self.offer_nego_list

    def find_available_vehicles(self,b_board, task_ready_time, task_due_date,vehicles):
        #タスク時間が，車両の稼動時間前後の車両を探す
        available_vehicles = []
        for _, row in b_board.iterrows():
            if row['departure_time'] > task_due_date or row['return_time'] < task_ready_time:
                available_vehicles.append(row['id'])
        return [vehicle for vehicle in vehicles if vehicle.id in available_vehicles]
    
    
    def sign_contracts(self, list: List[Agree]):
        #実際に履行する契約のリストを返す
        #listはAgreeクラスのリスト
        #listの中身は交渉によって得られた合意結果
        #合意結果の中身は交換するタスクのペア
        min_cost ={}
        min_cost_agreement = {}
        signed = []
        cost_border = 0
        if self.bulletin_board.n_steps / self.bulletin_board.max_steps < 0.5:
            cost_border = 1000 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps
        else:
            cost_border = 1000 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps - 300
        for agreements in list:
            task = agreements.taskA if agreements.taskA in self.tasks else None
            if task == None:
                task = agreements.taskB if agreements.taskB in self.tasks else None
            else:

            #各タスクについて，もっともコストの低い合意結果とコストを対応させて記録する
                cost = -1

                if cost < cost_border:
                    if agreements not in signed:
                        signed.append(agreements)

        return list
    


    # この関数は特定の合意結果のコスト削減を計算します。
    def calculate_cost_saving(self,agreements: Agree):

        remove_task = agreements.taskA if agreements.taskA in self.tasks else agreements.taskB
        give_task = agreements.taskA if agreements.taskA not in self.tasks else agreements.taskB

        # 交換でのタスクの交換によるスラックタイムの差分・コストの変化を計算
        slack_cost = self.calculate_differ_slack(self.tasks,remove_task,give_task)
        # 交換でのタスクの交換によるover_windowの差分・コストの変化を計算
        over_cost = self.caluculate_differ_over_window(self.tasks,remove_task,give_task)
        # 交換でのタスクの交換による距離の差分・コストの変化を計算
        distans_cost = self.calculate_differ_distance(remove_task,give_task)

        slack_late = 0.5

        #over_lateは，時間が進むにつれて値を大きくする
        #現在の時間はself.bulletin_board.n_stepで取得できる
        #最大時間はself.bulletin_board.max_stepで取得できる
        #over_costは前半ではほぼ無視をして，後半では大きくする
        #最後の25％の時間ではover_costをかなり大きくする
        over_late = 10 * (self.bulletin_board.n_steps / self.bulletin_board.max_steps) ** 2
        distance_late = 0.5
        cost_saving = slack_late * slack_cost + over_late * over_cost + distance_late * distans_cost
        return cost_saving

    def sign_contract(self, partner, taskA, taskB):

        return super().sign_contract(partner, taskA, taskB)
     
    def calculate_slacktime(self,route):
        slack_time = 0
        for task in route:
            slack_time += max(task.late_start_time - task.earliest_start_time ,0)
        return slack_time
    
    def calculate_differ_slack(self,route,remove_task,add_task):
        #元のrouteのスラックタイムと，タスクの交換後のスラックタイムの差分を示す
        #routeはパッケージのリストに限る
        #remove_taskはrouteから削除するタスク
        #add_taskはrouteに追加するタスク
        before_slack_time = self.calculate_slacktime(self.arrival_time_list)
        changed_list = copy.deepcopy(self.arrival_time_list)
        changed_list = self.remove_task(remove_task,changed_list)
        changed_list = self.add_task(add_task,changed_list)
        earliest_start_time_list(changed_list)
        latest_start_time_list(changed_list)
        after_slack_time = self.calculate_slacktime(changed_list)
        #スラックタイムが増えれば負の値を返す   
        return before_slack_time - after_slack_time
        #スラックタイムが増えれば負の値を返す
    

    def calculate_over_window(self,route):
        over_window = 0
        for task in route:
            over_window += max(task.earliest_start_time - task.task.due_date, 0)
        #due_dateトの引き算デいいのか議論の余地あり，最遅サービス開始時間でも
        return over_window  
            
    def caluculate_differ_over_window(self,route,remove_task,add_task):
        #元のrouteのover_windowと，タスクの交換後のover_windowの差分を示す
        #routeはパッケージのリストに限る
        #remove_taskはrouteから削除するタスク
        #add_taskはrouteに追加するタスク
        before_over_window = self.calculate_over_window(self.arrival_time_list)
        changed_list = copy.deepcopy(self.arrival_time_list)
        changed_list = self.remove_task(remove_task,changed_list)
        changed_list = self.add_task(add_task,changed_list)
        earliest_start_time_list(changed_list)
        latest_start_time_list(changed_list)
        after_over_window = self.calculate_over_window(changed_list)
        return after_over_window - before_over_window
        #over_windowが減れば負の値を返す
    
    def calculate_differ_distance(self,taskA,taskB):
        route = copy.deepcopy(self.tasks)
        if taskA in route:
            index = route.index(taskA)
        elif taskB in route:
            index = route.index(taskB)
        else:
            return 0

        distance = 0
        #削除するタスクの前後の移動時間
        distance -= euclidean_distance(route[index-1],route[index])
        distance -= euclidean_distance(route[index],route[index+1])
        #タスク追加の前後の移動時間
        taskB = taskA if taskA not in route else taskB
        index = self.least_cost_time_insertion_index(taskB)
        if index == None:
            return 0
        distance += euclidean_distance(route[index-1],taskB)
        distance += euclidean_distance(route[index],taskB)
        return distance
        #距離が短くなれば負の値を返す

    
    def least_cost_time_insertion_index(self , new_task):
        if not isinstance(new_task, Task):  # 仮定として Task というクラスが存在するとします。
            print("エラー: 'new_task' が Task オブジェクトではありません。")
            return False
        min_cost = float('inf')
        best_position = None
        cost = 0
        if len(self.tasks) == 0:
            return False
        # 車両の開始位置から新しいタスクまでの距離を計算
        start_task = Task(0, self.dep_x, self.dep_y, 0, 0, 0, 0)  # 仮の開始位置
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
            return best_position
        return None
    
    def step(self):
        return super().step()
    
    def find_task(self, task_id):
        # IDに基づいてタスクを探す
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def remove_task(self,task,route):
        #ルートはパッケージのリストに限る
        #routeからtaskを一致するものをもつクラスを削除する
        if task == None:
            return route
        for i in range(len(route)):
            if route[i].task == task:
                del route[i]
                break
        return route

    def first_step(self):
        self.arrival_time_list
        for task in self.tasks:
            self.arrival_time_list.append(pac_task(task))
        earliest_start_time_list(self.arrival_time_list)
        latest_start_time_list(self.arrival_time_list)
    
    def add_task(self,task,route : List[pac_task]):
        #routeはパッケージのリストに限る
        #routeにtaskを追加する
        if task == None:
            return route
        index = self.least_cost_time_insertion_index(task)
        if index == None:
            for i in range(len(route)):
                if route[i].task.due_date > task.due_date:
                    index = i
                    break
        if index == None:
            return route
        route.insert(index,pac_task(task))
        return route
    
        #コストが最小となる場所に挿入する
    def add(self, new_task):
        index = None
        if self.current_weight + new_task.weight > self.max_weight + 0 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps:
            return False
        if new_task in self.tasks:
            return False
        route = self.tasks
        index = self.least_cost_time_insertion_index(new_task)
        if index  == None :
            for i in range(len(route)):
                if route[i].due_date > new_task.due_date:
                    index = i
                    break
        if index != None:
            route.insert(index,new_task)
            self.arrival_time_list.insert(index,pac_task(new_task))
            self.current_weight += new_task.weight
        if new_task in self.tasks:
            return True
        else:
            return False
    
    def remove(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.current_weight -= task.weight
            #self.arrival_time_listからリスト内のクラスにtaskがある場合，そのクラスを削除する
            for i in range(len(self.arrival_time_list)):
                if self.arrival_time_list[i].task == task:
                    del self.arrival_time_list[i]
                    break
            return True
        else:
            return False
    def before_negotiation(self):
        #self.tasksの中から期限までに到達できないタスクを選びリスト化する
        #リストの中身はタスクのリスト
        #タスクのリストの中身はタスクのクラス
        remove_list = []
        for task_pac in self.arrival_time_list:
            if task_pac.earliest_start_time > task_pac.task.due_date:
                remove_list.append(task_pac.task)
        pac_list = copy.deepcopy(self.arrival_time_list)
        #pac_listから要素を1つずつ削除して，コストの減少が大きい順に並べる
        #remove_listにあるタスクは前に来るようにする
        #pac_listからi番目のタスクを削除したときのコストの増減を計算する
        cost={}
        rt_list = []
        for pac in pac_list:
            cost[pac.task] = self.calculate_cost_saving(Agree(self,self,pac.task,None))
        sorted_cost = sorted(cost.items(), key=lambda x:x[1])
        for i in sorted_cost:
            if i[0] in remove_list:
                remove_list.remove(i[0])
                rt_list.append(i[0])
        for i in sorted_cost:
            if i[0] not in remove_list:
                rt_list.append(i[0])
        self.over_task = rt_list
        return 