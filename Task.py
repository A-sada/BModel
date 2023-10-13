class Task:
    def __init__(self, id, x_coordinate, y_coordinate, weight, ready_time, due_date, service_time):
        self.id = id  # タスク（顧客）のID
        self.x_coordinate = x_coordinate  # 配送先のx座標
        self.y_coordinate = y_coordinate  # 配送先のy座標
        self.weight = weight  # 荷物の重量またはサイズ
        self.ready_time = ready_time  # 配送可能な最早時間
        self.due_date = due_date  # 配送締切時間
        self.service_time = service_time  # サービスにかかる時間

class Offer:
    def __init__(self, id, vehicleA,vehicleB,task):
        self.id = id  # タスク（顧客）のID
        self.vehicleA = vehicleA
        self.vehicleB = vehicleB
        self.task = task

class Nego:
    def __init__(self, id, vehicleA, vehicleB):
        self.id = id  # タスク（顧客）のID
        self.vehicleA = vehicleA
        self.vehicleB = vehicleB     