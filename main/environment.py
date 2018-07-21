# coding=utf-8
import time
import numpy as np

from model import structs
import random


HEIGHT = 5  # grid height
WIDTH = 5  # grid width

sa_ = 0.1
beta = 0.1
gamma = 0.1
fai = 0.1
frequency = 1

power = 1

Nx = 5  # 卸载率的粒度
M = 5  # MEC个数
B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
excu_v = [1, 1, 1, 1, 1, 1]

currentTaskIndex = -1  # 当前做到的任务标号

np.random.seed(1)


class Env(object):
    def __init__(self):
        super(Env, self).__init__()

        self.action_size = Nx * (M + 1) + 1

        self.x_off = 0
        self.m = 0

        self.title = 'DeepSARSA'

        self.taskList = self.load_task()
        self.counter = 0
        self.rewards = []
        self.bandwidth = [0, 0, 0, 0, 0, 0]
        self.e_time = 0
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
                pos.append(temp)  # 添加新读取的数据
        return pos

    def reset_reward(self):
        pass

    def set_reward(self, state, reward):
        state = [int(state[0]), int(state[1])]
        x = int(state[0])
        y = int(state[1])
        temp = {}
        if reward < 0:
            temp['direction'] = -1
            temp['reward'] = reward

        temp['state'] = state
        self.rewards.append(temp)

    # new methods

    def check_if_reward(self, state):
        check_list = dict()
        check_list['if_goal'] = False
        rewards = 0

        for reward in self.rewards:
            if reward['state'] == state:
                rewards += reward['reward']
        check_list['rewards'] = rewards

        return check_list

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
        initial_state.battery = 100
        initial_state.task_len = 1
        # e_time 的情况和episode TODO
        self.e_time = self.taskList[0].arrivalTime
        initial_state.rest = self.taskList[0].rest
        return initial_state

    def step(self, action, state, index):
        time.sleep(0.07)

        self.x_off = (action + 5) / 6 * 0.2
        self.m = (action + 5) % 6

        task = self.taskList[index]

        self.battery_cost = self.energy_cost(task)
        self.energy_harvest = self.energy_get()

        s_ = structs.State()
        s_.bandwidth = self.bandwidth
        s_.battery = state.battery - self.battery_cost + self.energy_harvest
        s_.energy_estimate = self.predict()
        s_.task_len, s_.rest = self.Qlenth(state)

        self.failure = self.fail(s_.battery, s_.rest)

        self.execution(task)

        reward = self.get_reward(state, action, task)

        return s_, reward

    def move_rewards(self):
        new_rewards = []
        for temp in self.rewards:
            if temp['reward'] == 1:
                new_rewards.append(temp)
                continue
            temp['coords'] = self.move_const(temp)
            temp['state'] = self.coords_to_state(temp['coords'])
            new_rewards.append(temp)
        return new_rewards

    def execution(self, task):
        # 失败判断
        if self.failure:
            return
        for i in range(len(self.bandwidth)):
            self.bandwidth[i] = random.randint(1, 9)  # 目前的带宽范围是1-9
        self.e_time += self.calculateTimeCost(task)

    # 计算任务的花费时间
    def calculateTimeCost(self, task):
        tt = 0.1
        tu = self.x_off * task.cd / self.bandwidth[self.m]
        te = self.x_off * task.cd / excu_v[self.m]
        td = self.x_off * task.rd / self.bandwidth[self.m]
        tm = tu + te + td + tt
        tl = 0
        return max(tm, tl)

    def predict(self):
        pass  # TODO 预测下一阶段能量收集多少，依赖于enery_get()
        energy = 0.0
        return energy

    def Qlenth(self, state):
        currentqlength = state.task_len
        nextTask = self.taskList[currentTaskIndex + 1]
        for i in range(currentTaskIndex, len(self.taskList)):
            if self.taskList[i].arrivalTime <= self.e_time:
                currentqlength = currentqlength + 1
            pass
        return currentqlength, nextTask.arrivalTime + nextTask.rest - self.e_time

    def get_reward(self, state, action, task):
        r_ = sa_ * self.failure + beta * (self.E_Local + self.E_MEC) + gamma * self.calculateTimeCost(task)
        return r_

    def fail(self, battery, rest):
        """
        判断任务执行情况
        :param battery: 电池电量
        :param rest: 剩余时间
        :type battery: int
        :type rest: int
        :return: 任务是否执行失败
        :rtype: bool
        """
        if battery < 0 or rest < 0:
            return True
        return False

    def energy_cost(self, task):
        self.E_MEC = power * self.x_off * task.cd / self.bandwidth[self.m]
        self.E_Local = fai * (frequency ** 2)  # TODO E_local算式不确定
        return self.E_Local + self.E_MEC

    def energy_get(self):
        # TODO 能量获取机制不确定
        return 0.0
