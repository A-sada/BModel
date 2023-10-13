import math
# タスク間または車両とタスク間のユークリッド距離を計算する関数
def euclidean_distance(task1, task2):
    return math.sqrt((task1.x_coordinate - task2.x_coordinate)**2 + (task1.y_coordinate - task2.y_coordinate)**2)