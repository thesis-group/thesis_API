# coding=utf-8
"""
对应原Java项目中的类：
State、Task

文件目标：
定义训练状态模型和任务模型
"""


class State(object):
    """
    状态模型
    """

    def __init__(self):
        self.bandwidth = [0, 0, 0, 0]
        self.energy_estimate = 0.0
        self.battery = 0.0
        self.task_len = 0
        self.rest = 0.0

    """def __init__(self, bandwidth, energy_estimate, battery, task_len, rest):
        self.bandwidth = bandwidth
        self.energy_estimate = energy_estimate
        self.battery = battery
        self.task_len = task_len
        self.rest = rest
    """
    def reshape(self):
        new_shape = []
        for b in self.bandwidth:
            new_shape.append(b)
        new_shape.append(self.energy_estimate)
        new_shape.append(self.battery)
        new_shape.append(self.task_len)
        new_shape.append(self.rest)
        return new_shape

    def equals(self):
        """
        判断两个状态是否是同一状态
        :return: 判断结果
        :rtype: bool
        """
        pass


class Task(object):
    # 剩余生命周期
    rest = 0.0
    # 任务的到达时间
    arrivalTime = 0
    # 需计算数据量
    cd = 0.0
    # 传出数据量
    rd = 0.0

    """
    任务模型
    """

    def __init__(self):
        # 剩余生命周期
        self.rest = 0.0
        # 任务的到达时间
        self.arrivalTime = 0
        # 需计算数据量
        self.cd = 0.0
        # 传出数据量
        self.rd = 0.0
