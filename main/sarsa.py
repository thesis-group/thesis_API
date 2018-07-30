# coding=utf-8
import copy
import random
import numpy as np
from main.environment import Env
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential
from model.structs import State
import json

EPISODES = 1000
Nx = 5  # 卸载率的粒度
M = 5  # 云+MEC个数

Q_table = {}
learning_rate = 0.1  # TODO 这里加了一下参数
discount_factor = 0.1
train = True  # True -- 训练; False -- 测试
group_size = 1000  # 一组任务集的任务数量


# this is DeepSARSA Agent for the GridWorld
# Utilize Neural Network as q function approximator
class DeepSARSAgent:
    def __init__(self):
        self.load_model = False

        self.action_size = Nx * (M + 1) + 1

        self.state_size = 15
        self.discount_factor = 0.99
        self.learning_rate = 0.001

        self.epsilon = 1.  # exploration
        self.epsilon_decay = .9999
        self.epsilon_min = 0.01
        self.model = self.build_model()

        if self.load_model:
            self.epsilon = 0.05
            self.model.load_weights('./save_model/deep_sarsa_trained.h5')

    #
    #     # approximate Q function using Neural Network
    #     # state is input and Q Value of each action is output of network
    #     # 网络模型使用Sequential模型利用add或list添加，决定网络结构 # TODO
    def build_model(self):
        model = Sequential()
        model.add(Dense(30, input_dim=self.state_size, activation='relu'))
        model.add(Dense(30, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        # 打印模型结构,可删# TODO
        model.summary()
        # 损失函数与优化算法以及指标列表的选择# TODO
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    # get action from model using epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            # The agent acts randomly
            return random.randrange(self.action_size)
        else:
            # Predict the reward value based on the given state
            return np.argmax(Q_table[state])  # TODO 这里改动了，通过查表获得下一个Action

    def train_model(self, state, action, reward, next_state, next_action, done):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        state = np.float32(state)
        next_state = np.float32(next_state)
        target = self.model.predict(state)[0]
        # like Q Learning, get maximum Q value at s'
        # But from target model
        if done:
            target[action] = reward
        else:
            target[action] = (reward + self.discount_factor *
                              self.model.predict(next_state)[0][next_action])

        target = np.reshape(target, [1, 5])
        # make minibatch which includes target q value and predicted q value
        # and do the model fit!
        self.model.fit(state, target, epochs=1, verbose=0)


#
def dic2Q_table(dic):
    result = {}
    all_state_dic = dic.keys()
    for state_dic in all_state_dic:
        state = State(state_dic['bandwidth'], state_dic['energy_estimate'], state_dic['battery'], state_dic['task_len'],
                      state_dic['rest'])
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
    current_q = Q_table[state][action]
    next_state_q = Q_table[next_state][next_action]
    new_q = (current_q + learning_rate *
             (reward + discount_factor * next_state_q - current_q))
    Q_table[state][action] = new_q


def format_state(old_state):
    bandwidth_list = old_state.bandwidth
    for i in len(bandwidth_list):
        format_bandwidth = bandwidth_list[i]
        format_bandwidth = (format_bandwidth + 1) / 2 * 2 - 1
        bandwidth_list[i] = format_bandwidth
    old_state.energy_estimate = old_state.energy_estimate / 1
    old_state.battery = old_state.battery / 10
    if old_state.rest < 0:
        old_state.rest = 0
    else:
        old_state.rest = old_state.rest / 5
        if old_state.rest > 20:
            old_state.rest = 20


if __name__ == "__main__":
    env = Env()
    agent = DeepSARSAgent()

    task_index = 0
    succ = 0

    data = []
    D = []
    DeepSARSAgent.init_q_table(train)

    for e in range(EPISODES):
        done = False
        score = 0
        state = env.reset()
        shaped_state = state.reshape()
        action = agent.get_action(shaped_state)

        extend_state = state  # 上一次循环的完整状态
        while not done:
            # fresh env
            task_index += 1

            state = extend_state  # 上一次的完整next_state状态

            # get action for the current state and go one step in environment
            next_state, reward = env.step(action, state, task_index)

            # 经验池
            data = [state, action, reward, next_state]
            D.append(data)

            extend_state = next_state  # 保存next_state
            # TODO 缺少取出操作

            format_state(state)  # 缩小State
            format_state(next_state)  # 缩小State

            next_action = agent.get_action(next_state)
            learn(state, action, reward, next_state, next_action)  # TODO 这里做了改动

            state = next_state
            action = next_action
            # every time step we do training

            state = copy.deepcopy(next_state)

    if e % 100 == 0:
        with open("sarsa_model.json", "a+")as f:
            f.write(json.dump(Q_table, default=lambda obj: obj.__dict__))
