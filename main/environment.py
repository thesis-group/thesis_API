# coding=utf-8
import time
import numpy as np
import copy
from model import structs
import random


HEIGHT = 5  # grid height
WIDTH = 5  # grid width

sa_ = -0.1
beta = -0.1
gamma = -0.1
fai = 0.1
frequency = 1

power = 1
P_energy = 0.2

Nx = 5  # 卸载率的粒度
M = 5  # MEC个数
B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
excu_v = [15, 2, 3, 1, 2, 1]

currentTaskIndex = -1  # 当前做到的任务标号

np.random.seed(1)


class Env(object):
    def __init__(self):
        super(Env, self).__init__()

        self.action_size = Nx * (M + 1) + 1

        self.x_off = 0
        self.m = 0

        self.title = 'DeepSARSA'

        self.taskList = self.load_task().copy()
        self.counter = 0
        self.rewards = []
        self.bandwidth = [0, 0, 0, 0, 0, 0]
        self.e_time = 0
        self.this_time = 0
        self.failure = False

        self.E_MEC, self.E_Local = 0.0, 0.0
        self.battery_cost = 0.0
        self.energy_harvest = 0.0

    def load_task(self):
        filename = './train/data.txt'
        pos = []
        temp = structs.Task()
        with open(filename, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline()
                if not lines:
                    break
                temp.arrivalTime, temp.cd, temp.rd, temp.rest = [float(i) for i in lines.split(',')]  # 分割为逗号,（英文）
                pos.append(copy.deepcopy(temp))  # 添加新读取的数据
        return pos

    # new methods
    def reset(self):
        """
        初始化首状态
        :return: 首状态
        :rtype: structs.State
        """
        # 初始化 TODO
        initial_state = structs.State()
        initial_bandwidth = self.bandwidth
        for i in range(len(self.bandwidth)):
            initial_bandwidth[i] = random.randint(1, 9)
        initial_state.bandwidth = initial_bandwidth
        initial_state.energy_estimate = self.predict()
        initial_state.battery = 1000
        initial_state.task_len = 1
        # e_time 的情况和episode TODO
        self.e_time = self.taskList[0].arrivalTime
        initial_state.rest = self.taskList[0].rest
        return initial_state

    def step(self, action, state, index):
        time.sleep(0.005)

        self.x_off = (action + 5) / 6 * 0.2
        self.m = (action + 5) % 6

        task = self.taskList[index]

        self.this_time = 0

        s_ = copy.deepcopy(state)

        if not self.failure:
            s_.bandwidth = copy.deepcopy(self.bandwidth)
            for i in range(len(self.bandwidth)):
                self.bandwidth[i] = random.randint(1, 9)  # 目前的带宽范围是1-9

        self.battery_cost = self.energy_cost(task)
        self.energy_harvest = self.energy_get()
        self.failure = self.fail(state, state.rest)

        self.this_time = self.calculateTimeCost(task, s_)
        self.execution(task, s_)
        print(self.e_time)

        if not self.failure:
            s_.battery = state.battery - self.battery_cost + self.energy_harvest
        s_.energy_estimate = self.predict()
        s_.task_len, s_.rest = self.Qlenth(state, index)

        reward = self.get_reward(state, action, task, s_)

        return s_, reward

    def execution(self, task, s_):
        # 失败判断
        if self.failure:
            return

        self.e_time += self.this_time

    # 计算任务的花费时间
    def calculateTimeCost(self, task, s_):
        if self.failure:
            return 0
        tt = 0.1
        tu = self.x_off * task.cd / s_.bandwidth[self.m]
        te = self.x_off * task.cd / excu_v[self.m]
        td = self.x_off * task.rd / s_.bandwidth[self.m]
        tm = tu + te + td + tt
        tl = 0.5  # TODO DVFS
        return max(tm, tl)

    def Qlenth(self, state, index):
        currentqlength = state.task_len
        # nextTask未考虑容错
        nextTask = self.taskList[index + 1]
        for i in range(index + state.task_len, len(self.taskList)):
            if self.taskList[i].arrivalTime <= self.e_time:
                currentqlength = currentqlength + 1
            else:
                break
        return currentqlength - 1, nextTask.arrivalTime + nextTask.rest - self.e_time

    def get_reward(self, state, action, task, s_):
        r_ = sa_ * self.failure + beta * (self.E_Local + self.E_MEC) + gamma * self.this_time
        return round(r_, 3)

    def fail(self, state, rest):
        """
        判断任务执行情况
        :param battery: 电池电量
        :param rest: 剩余时间
        :type battery: int
        :type rest: int
        :return: 任务是否执行失败
        :rtype: bool
        """
        battery = state.battery - self.battery_cost + state.energy_estimate
        if battery < 0 or rest < 0:
            return True
        return False

    def energy_cost(self, task):
        self.E_MEC = power * self.x_off * task.cd / self.bandwidth[self.m]
        self.E_Local = fai * (frequency ** 2)  # TODO E_local算式不确定
        return self.E_Local + self.E_MEC

    def predict(self):
        pass  # TODO 预测下一阶段能量收集多少
        energy = 3
        return energy

    def energy_get(self):
        # TODO 真实能量获取
        energy = self.this_time * P_energy
        return energy
