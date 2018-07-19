import time
import numpy as np
import tkinter as tk
from model import structs
from PIL import ImageTk, Image

PhotoImage = ImageTk.PhotoImage

HEIGHT = 5  # grid height
WIDTH = 5  # grid width

Nx = 5  # 卸载率的粒度
M = 5  # 云+MEC个数
B = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

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

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=HEIGHT * UNIT,
                           width=WIDTH * UNIT)
        # create grids
        for c in range(0, WIDTH * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
            canvas.create_line(x0, y0, x1, y1)
        for r in range(0, HEIGHT * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = 0, r, HEIGHT * UNIT, r
            canvas.create_line(x0, y0, x1, y1)

        self.rewards = []
        self.goal = []
        # add image to canvas
        x, y = UNIT/2, UNIT/2
        self.rectangle = canvas.create_image(x, y, image=self.shapes[0])

        # pack all`
        canvas.pack()

        return canvas

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
        if reward > 0:
            temp['reward'] = reward
            temp['figure'] = self.canvas.create_image((UNIT * x) + UNIT / 2,
                                                       (UNIT * y) + UNIT / 2,
                                                       image=self.shapes[2])

            self.goal.append(temp['figure'])


        elif reward < 0:
            temp['direction'] = -1
            temp['reward'] = reward
            temp['figure'] = self.canvas.create_image((UNIT * x) + UNIT / 2,
                                                      (UNIT * y) + UNIT / 2,
                                                      image=self.shapes[1])

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
                #if reward['reward'] == 1:
                    #check_list['if_goal'] = True
        check_list['rewards'] = rewards

        return check_list

    def coords_to_state(self, coords):
        x = int((coords[0] - UNIT / 2) / UNIT)
        y = int((coords[1] - UNIT / 2) / UNIT)
        return [x, y]

    def reset(self):
        self.update()
        time.sleep(0.5)
        x, y = self.canvas.coords(self.rectangle)
        self.canvas.move(self.rectangle, UNIT / 2 - x, UNIT / 2 - y)
        # return observation
        self.reset_reward()
        return self.get_state()

    def step(self, action, state):
        self.e_time += 1  # TODO
        self.render()

        s_ = structs.state()
        s_.bandwidth = self.bandwidth
        s_.battery = state.battery - self.battery_cost + self.energy_harvest
        s_.energy_estimate = self.predict()
        s_.task_len, s_.rest = self.Qlenth()

        self.excution()

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

    def excution(self):
        pass  # 更新带宽等 TODO

    def predict(self):
        pass  # 预测下一阶段能量收集多少 TODO
        energy = 0.0
        return energy

    def Qlenth(self):
        pass  # 队列长度和当前任务lifespan TODO
        return 0, 0.0

    def get_reward(self, state, action):
        r_ = sa * failcost() + beta * (E0 + Em) + gama * max(T1, T2)
        # 计算当前的即使回报 TODO
        return r_
    
    def render(self):
        time.sleep(0.07)
        self.update()
