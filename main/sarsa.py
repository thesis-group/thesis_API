# coding=utf-8
import copy
import random
import numpy as np
from main.environment import Env
from model.structs import State
import json

EPISODES = 1000
Nx = 5  # 卸载率的粒度
M = 3  # 云+MEC个数

Q_table = {}
learning_rate = 0.1  # TODO 这里加了一下参数
discount_factor = 0.1
fault_tolerance = True
train = True  # True -- 训练; False -- 测试
group_size = 1000  # 一组任务集的任务数量


# this is DeepSARSA Agent for the GridWorld
# Utilize Neural Network as q function approximator
class DeepSARSAgent:
    def __init__(self):
        self.load_model = False

        self.action_size = Nx * (M + 1) + 1

        self.state_size = M + 5
        self.discount_factor = 0.99
        self.learning_rate = 0.001

        self.epsilon = 1.  # exploration
        self.epsilon_decay = .9999
        self.epsilon_min = 0.01

        if not train:
            self.epsilon = self.epsilon_min
        if self.load_model:
            self.epsilon = 0.05

    # get action from model using epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            # The agent acts randomly
            return random.randrange(self.action_size)
        else:
            # Predict the reward value based on the given state
            return np.argmax(Q_table[state])  # TODO 这里改动了，通过查表获得下一个Action


#
def dic2Q_table(dic):
    result = {}
    all_state_dic = dic.keys()
    for state_dic in all_state_dic:
        state = State()
        state.bandwidth = state_dic['bandwidth']
        state.energy_estimate = state_dic['bandwidth']
        state.battery = state_dic['battery']
        state.task_len = state_dic['task_len']
        state.rest = state_dic['rest']
        result[state] = dic[state_dic]
    return result


def read_Q_table():
    with open('sarsa_model.json')as f:
        json_str = f.readline()
        saved_table = json.load(json_str, object_hook=dic2Q_table)
    Q_table = saved_table


# # TODO 初始化Q表
def init_q_table(train):
    if not train:
        read_Q_table()
        return
    for first_bandwidth in range(1, 10, 2):
        for second_bandwidth in range(1, 10, 2):
            for third_bandwidth in range(1, 10, 2):
                for fourth_bandwidth in range(1, 10, 2):
                    for energy_estimate in range(0, 6):
                        for battery in range(0, 11):
                            for task_len in range(0, 21):
                                for rest in range(0, 21):
                                    this_state = State()
                                    this_state.bandwidth = [first_bandwidth, second_bandwidth, third_bandwidth,
                                                            fourth_bandwidth]
                                    this_state.energy_estimate = energy_estimate
                                    this_state.battery = battery
                                    this_state.task_len = task_len
                                    this_state.rest = rest
                                    Q_table[this_state] = np.zeros(21)

# with sample <s, a, r, s', a'>, learns new q function
def learn(state, action, reward, next_state, next_action):
    print(state, ' ', action)
    current_q = Q_table[state][action]
    next_state_q = Q_table[next_state][next_action]
    new_q = (current_q + learning_rate *
             (reward + discount_factor * next_state_q - current_q))
    Q_table[state][action] = new_q

def format_state(old_state):
    bandwidth_list = old_state.bandwidth
    for i in range(len(bandwidth_list)):
        format_bandwidth = bandwidth_list[i]
        format_bandwidth = (format_bandwidth + 1) / 2 * 2 - 1
        bandwidth_list[i] = format_bandwidth
    old_state.energy_estimate = int(old_state.energy_estimate / 1)
    old_state.battery = int(old_state.battery / 10)
    if old_state.rest < 0:
        old_state.rest = 0
    else:
        old_state.rest = int(old_state.rest / 5)
        if old_state.rest > 20:
            old_state.rest = 20

def wrong_execution():
    number = random.randint(1, 100)
    if number <= 5:
        return True
    return False

if __name__ == "__main__":
    env = Env(train)
    agent = DeepSARSAgent()

    data = []
    D = []
    init_q_table(train)

    if not train:
        EPISODES = 20

    for e in range(EPISODES):
        done = False
        task_index = -1
        state = env.reset(True)  # 初始化任务文件偏移量
        extend_state = state  # 上一次循环的完整状态

        format_state(state)  # 缩小State
        action = agent.get_action(state)

        while not done:
            # fresh env
            task_index += 1
            state = extend_state  # 上一次的完整next_state状态

            if task_index != 0 and task_index % group_size == 0:
                state = env.reset()

            # get action for the current state and go one step in environment
            try:
                next_state, reward, current_task = env.step(action, state, task_index)
                x_off = (action + 3) / 4
                x_off *= 0.2
                if fault_tolerance and wrong_execution():
                    task_index -= 1
                    current_task.rd *= x_off
                    current_task.cd *= x_off
            except IndexError:
                last_task = True
                break

            extend_state = next_state  # 保存next_state

            format_state(state)  # 缩小State
            format_state(next_state)  # 缩小State

            next_action = agent.get_action(next_state)
            learn(state, action, reward, next_state, next_action)  # TODO 这里做了改动

            action = next_action
            # every time step we do training
    with open("sarsa_model.json", "a+")as f:
        f.write(json.dump(Q_table, default=lambda obj: obj.__dict__))
