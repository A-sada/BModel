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
 
import random
class Vehicle(Vehicle_BASE):
#TypeA
    def __init__(self, id, max_weight, dep_x, dep_y):
        super().__init__(id, max_weight, dep_x, dep_y)

    def check_offer(self, task):
        if self.bulletin_board.n_steps / self.bulletin_board.max_steps < 0.5:

            return True
        return self.is_task_assignable_with_or_tools(task,self.dep_x,self.dep_y)
        
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
        other_cluster_tasks = []    
        for task in self.tasks:
            if random.randint(1,100)<51:
                other_cluster_tasks.append(task)
        
        if self.current_weight >= self.max_weight:
            wei = self.max_weight/len(self.tasks)

            for task in self.tasks:
                if task.weight >= wei:
                    if task not in other_cluster_tasks:
                        other_cluster_tasks.append(task)


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

        for agreements in list:
            task = agreements.taskA if agreements.taskA in self.tasks else None
            if task == None:
                task = agreements.taskB if agreements.taskB in self.tasks else None
            if task != None:
                if task not in min_cost:
                    min_cost[task] = [100000]
                    min_cost_agreement[task] = []

            #各タスクについて，もっともコストの低い合意結果とコストを対応させて記録する
                cost = self.calculate_cost_saving(agreements)
                if cost != None:
                    # if cost < 0:
                    #     if agreements not in signed:
                    #         signed.append(agreements)
                    #min_costにtaskがない場合，min_costに追加
                    if task not in min_cost:
                        min_cost[task].insert(0,cost)
                        min_cost_agreement[task].insert(0,agreements)  
                    #min_costにtaskがある場合，コストが小さい方をmin_costに追加
                    elif min_cost[task][0] > cost:
                        min_cost[task].insert(0,cost)
                        min_cost_agreement[task].insert(0,agreements)
            #計算したコストが閾値以下であれば合意する
        for task in min_cost:
            if self.current_weight + task.weight < self.max_weight + 0 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps:
                #閾値は時間帯によって変化する
                #閾値は変数
                cost_border = 0
                if self.bulletin_board.n_steps / self.bulletin_board.max_steps < 0.5:
                    cost_border = 10 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps
                else:
                    cost_border = 10 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps +10
                #print(f"車両{self.id}のコスト閾値は{cost_border}")
                #print(min_cost[task][0])
                # if min_cost[task][0] < cost_border:
                #     if min_cost_agreement[task][0] not in signed:
                #         signed.append(min_cost_agreement[task][0])
                for i in range(len(min_cost[task])):
                    if min_cost[task][i] < cost_border:
                        if min_cost_agreement[task][i] not in signed:
                            #print(min_cost[task][i])
                            signed.append(min_cost_agreement[task][i])
        #print(f"車両ごとの署名リストの長さ：{len(signed)}")
        # print(signed)
        return signed
    


    # この関数は特定の合意結果のコスト削減を計算します。
    def calculate_cost_saving(self,agreements: Agree):
        cost_saving = 0
        remove_task = agreements.taskA if agreements.taskA in self.tasks else None
        remove_task = agreements.taskB if agreements.taskB in self.tasks else None

        give_task = agreements.taskA if agreements.taskA not in self.tasks else None
        give_task = agreements.taskB if agreements.taskB not in self.tasks else None

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
        #print(f"車両{self.id}のコスト削減は{cost_saving}")
        return cost_saving

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
        earliest_start_time_list(changed_list,self.dep_x,self.dep_y)
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
        earliest_start_time_list(changed_list,self.dep_x,self.dep_y)
        latest_start_time_list(changed_list)
        after_over_window = self.calculate_over_window(changed_list)
        return after_over_window - before_over_window
        #over_windowが減れば負の値を返す
    
    def calculate_differ_distance(self,taskA,taskB):
        route = self.tasks
        distance = 0
        if taskA != None:
            #削除するタスクの前後の移動時間
            index = route.index(taskA)
            if index > 0:
                distance -= euclidean_distance(route[index-1],route[index])
            if index < len(route)-1:
                distance -= euclidean_distance(route[index],route[index+1])
        #タスク追加の前後の移動時間
        if taskB != None:

            index = self.least_cost_time_insertion_index(taskB)
            if index == None:
                return distance
            if index > 0:
                distance += euclidean_distance(route[index-1],taskB)
            if index < len(route):
                distance += euclidean_distance(route[index],taskB)
        return distance
        #距離が短くなれば負の値を返す

    
    def least_cost_time_insertion_index(self , new_task):
        if not isinstance(new_task, Task):  # 仮定として Task というクラスが存在するとします。
            ##print("エラー: 'new_task' が Task オブジェクトではありません。")
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
        self.arrival_time_list=[]
        for task in self.tasks:
            self.arrival_time_list.append(pac_task(task))
        earliest_start_time_list(self.arrival_time_list,self.dep_x,self.dep_y)
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
        if new_task in self.tasks:
            return False
        route = self.tasks
        index = self.least_cost_time_insertion_index(new_task)
        if index  == None :
            for i in range(len(route)):
                if route[i].due_date > new_task.due_date:
                    index = i
                    break
        if index != None and self.current_weight + new_task.weight < self.max_weight + 10 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps:
            self.current_weight += new_task.weight
            route.insert(index,new_task)
            self.arrival_time_list.insert(index,pac_task(new_task))
        if new_task in self.tasks:
            return True
        else:
            # print(index)
            # print(self.tasks)
            # print(self.current_weight)
            # print(self.max_weight + 100 * (self.bulletin_board.max_steps - self.bulletin_board.n_steps) / self.bulletin_board.max_steps)
            # print(new_task.weight)
            return False
    
    def remove(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            #self.arrival_time_listからリスト内のクラスにtaskがある場合，そのクラスを削除する
            for i in range(len(self.arrival_time_list)):
                if self.arrival_time_list[i].task == task:
                    self.current_weight -= task.weight
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
    
    def insert_cost(self,pac_list,route):
        slack_cost = self.calculate_slacktime(pac_list)
        over_cost = self.calculate_over_window(pac_list)
        distance_cost = self.calculate_distance(route)
        return slack_cost + over_cost + distance_cost



        
    def is_task_assignable_with_or_tools(vehicle, new_task,dep_x,dep_y):
        max_weight = vehicle.max_weight
        # タスクがまだ割り当てられていない場合や、車両にまだタスクが割り当てられていない場合
        if len(vehicle.tasks) > 4:
            return False
        if vehicle.current_weight + new_task.weight > max_weight:
            return False
        current_time = 0
        # 車両の開始位置から新しいタスクまでの距離を計算
        start_task = Task(0, dep_x, dep_y, 0, 0, 0, 0)  # 仮の開始位置
        travel_time_from_start = max(euclidean_distance(start_task, new_task),new_task.ready_time)
        #if travel_time_from_start <= new_task.due_date :
        if travel_time_from_start + new_task.service_time + euclidean_distance(new_task, vehicle.tasks[0]) <= vehicle.tasks[0].due_date: 
            return True
        current_task = vehicle.tasks[0]
        next_task = None
        pre_task = None
        # 各タスク間での新しいタスクの挿入を試みる
        for i in range(len(vehicle.tasks) - 1):
            current_task = vehicle.tasks[i]
            next_task = vehicle.tasks[i + 1]
            if i == 0:
                current_time = max(euclidean_distance(start_task, current_task),current_task.ready_time)
                current_time += current_task.service_time
                # 現在のタスクの終了時間を計算
            else:
                current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
                #current_timeをカレントタスクの開始時間に更新
                current_time += current_task.service_time
            
            # 新しいタスクへの移動に必要な時間を計算
            travel_time_to_new_task = euclidean_distance(current_task, new_task)

            # 新しいタスクのサービス終了時間を計算
            new_task_end_time = current_time + travel_time_to_new_task + new_task.service_time

            # 次のタスクへの移動に必要な時間を計算
            travel_time_to_next_task = euclidean_distance(new_task, next_task)

            # 次のタスクの開始時間を計算
            next_task_start_time = new_task_end_time + travel_time_to_next_task
            
            pre_task = current_task
            # 新しいタスクがdue_date前に終了し、次のタスクが時間内に開始できるかどうかを確認
            if current_time + travel_time_to_new_task <= new_task.due_date and next_task_start_time <= next_task.due_date:
                return True
        #current_timeは最後から二番目のタスクの終了時間
        if next_task != None:
            current_task = next_task
            current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
            current_time += current_task.service_time
            next_task = new_task
            current_time = max(current_time + euclidean_distance(current_task, next_task),next_task.ready_time)
            if current_time <= next_task.due_date:
                return True
        else:
            current_task = vehicle.tasks[-1]
            pre_task = current_task
            current_time = max(current_time + euclidean_distance(pre_task,current_task),current_task.ready_time)
            current_time += current_task.service_time
            next_task = new_task
            current_time = max(current_time + euclidean_distance(current_task, next_task),next_task.ready_time)
            if current_time <= next_task.due_date:
                return True
        return False