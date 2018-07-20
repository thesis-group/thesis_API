import time
import numpy as np
import tkinter as tk
from model import structs
from PIL import ImageTk, Image
import random

PhotoImage = ImageTk.PhotoImage

HEIGHT = 5  # grid height
WIDTH = 5  # grid width

Nx = 5  # 卸载率的粒度
M = 5  # 云+MEC个数
B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

e_time = 0  # 当前时间
currentTaskIndex = 0  # 当前做到的任务标号
taskList = []  # 任务集合
np.random.seed(1)


class Env(tk.Tk):
    def __init__(self):
        super(Env, self).__init__()
        # z修改动作空间# TODO

        self.action_size = Nx * (M + 1) + 1

        self.title('DeepSARSA')

        self.geometry('{0}x{1}'.format(HEIGHT * UNIT, HEIGHT * UNIT))
        self.task = self.load_task()
        self.canvas = self._build_canvas()
        self.counter = 0
        self.rewards = []
        self.bandwidth = []
        self.battery_cost = 0.0
        self.energy_harvest = 0.0

    def load_task(self):
        filename = '.../train/data.txt'
        pos = []
        Efield = []
        with open(filename, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline()
                if not lines:
                    break
                p_tmp, E_tmp = [float(i) for i in lines.split()]  # 分割为空格
                pos.append(p_tmp)  # 添加新读取的数据
                Efield.append(E_tmp)

    def reset_reward(self):

        for reward in self.rewards:
            self.canvas.delete(reward['figure'])

        self.rewards.clear()
        self.goal.clear()

    def set_reward(self, state, reward):
        state = [int(state[0]), int(state[1])]
        x = int(state[0])
        y = int(state[1])
        temp = {}
        if reward < 0:
            temp['direction'] = -1
            temp['reward'] = reward

        temp['coords'] = self.canvas.coords(temp['figure'])
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
        self.update()
        time.sleep(0.5)
        x, y = self.canvas.coords(self.rectangle)
        self.canvas.move(self.rectangle, UNIT / 2 - x, UNIT / 2 - y)
        # return observation
        self.reset_reward()
        return self.get_state()

    def step(self, action, state, task):
        self.e_time += 1  # TODO
        self.render()

        self.battery_cost = self.energy_cost()
        self.energy_harvest = self.energy_get()

        s_ = structs.State()
        s_.bandwidth = self.bandwidth
        s_.battery = state.battery - self.battery_cost + self.energy_harvest
        s_.energy_estimate = self.predict()
        s_.task_len, s_.rest = self.Qlenth(state)

        self.excution(task)

        reward = self.get_reward(state, action)

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

    def excution(self, task):
        for i in range(len(self.bandwidth)):
            self.bandwidth[i] = random.randint(1, 9)  # 目前的带宽范围是1-9
        self.e_time += self.calculateTimeCost(task)
        pass  # 更新带宽等 TODO

    # 计算任务的花费时间
    def calculateTimeCost(self, task):
        tt = 0.1
        tu = x_off * task.cd / self.bandwidth[m]
        te = x_off * task.cd / excu_v[m]
        td = x_off * task.rd / self.bandwidth[m]
        tm = tu + te + td + tt
        tl = 0
        return max(tm, tl)

    def predict(self):
        pass  # 预测下一阶段能量收集多少 TODO
        energy = 0.0
        return energy

    def Qlenth(self, state):
        currentqlength = state.task_len
        nextTask = taskList[currentTaskIndex + 1]
        while i in range(currentTaskIndex, len(taskList)):
            if taskList[i].arrivalTime <= e_time:
                currentqlength = currentqlength + 1
            pass  # 队列长度和当前任务lifespan TODO
        return currentqlength, nextTask.arrivalTime + nextTask.rest - e_time

    def get_reward(self, state, action):
        r_ = sa * failcost() + beta * (self.E_Local + Em) + gama * max(T1, T2)
        # 计算当前的即使回报 TODO
        return r_

    def energy_cost(self):
        self.E_Local = power * x_off * task.cd / state.bandwidth[m]
        self.E_MEC = fai * f ^ 2
        return E_Local + E_MEC

    def energy_get(self):
        return 0, 0

    def render(self):
        time.sleep(0.07)
        self.update()
