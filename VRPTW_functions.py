import math
from classes import Task
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
