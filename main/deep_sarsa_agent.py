# coding=utf-8
import copy
import random
import numpy as np
from main.environment import Env
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from keras.models import Sequential

EPISODES = 100
Nx = 5  # 卸载率的粒度
M = 3  # MEC个数
fault_tolerance = True


# this is DeepSARSA Agent for the GridWorld
# Utilize Neural Network as q function approximator
class DeepSARSAgent:
    def __init__(self):
        self.load_model = False

        self.action_size = Nx * (M + 1) + 1

        self.state_size = M + 5
        self.discount_factor = 0.99
        self.learning_rate = 0.01

        self.epsilon = 1.  # exploration
        self.epsilon_decay = .9999
        self.epsilon_min = 0.001
        self.model = self.build_model()

        if self.load_model:
            self.epsilon = 0.05
            self.model.load_weights('./save_model/deep_sarsa_trained.h5')

    # approximate Q function using Neural Network
    # state is input and Q Value of each action is output of network
    # 网络模型使用Sequential模型利用add或list添加，决定网络结构 # TODO
    def build_model(self):
        model = Sequential()
        model.add(Dense(13, input_dim=self.state_size, activation='relu'))
        model.add(Dense(17, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        # 打印模型结构,可删# TODO
        model.summary()
        # 损失函数与优化算法以及指标列表的选择# TODO
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate), metrics=['accuracy'])
        return model

    # get action from model using epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            # The agent acts randomly
            return random.randrange(self.action_size)
        else:
            # Predict the reward value based on the given state
            state = np.float32(state)
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])

    def train_model(self, state, action, reward, next_state, next_action):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        print('e = ', self.epsilon)
        state = np.float32(state)
        next_state = np.float32(next_state)
        target = self.model.predict(state)[0]
        # like Q Learning, get maximum Q value at s'
        # But from target model
        if done:
            target[action] = reward
        else:
            target[action] = reward + self.discount_factor * self.model.predict(next_state)[0][next_action]
            print('target = ', reward + self.discount_factor * self.model.predict(next_state)[0][next_action])

        target = np.reshape(target, [1, self.action_size])
        # make minibatch which includes target q value and predicted q value
        # and do the model fit!
        self.model.fit(state, target, batch_size=1, epochs=1, verbose=2, shuffle=True)


def wrong_execution():
    number = random.randint(1, 100)
    if number >= 5:
        return True
    return False


if __name__ == "__main__":
    env = Env()
    agent = DeepSARSAgent()

    times = 0

    data = []
    D = []

    for e in range(EPISODES):
        done = False

        task_index = -1
        succ = 0
        last_task = False
        state = env.reset()
        shaped_state = np.reshape(state.reshape(), [1, -1])
        action = agent.get_action(shaped_state)

        while not done:
            # fresh env
            task_index += 1

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

            shaped_next_state = np.reshape(next_state.reshape(), [1, -1])

            # 经验池
            data = [state, action, reward, next_state]
            D.append(data)

            # TODO 缺少取出操作

            next_action = agent.get_action(shaped_next_state)
            agent.train_model(shaped_state, action, reward, shaped_next_state, next_action)

            shaped_state = copy.deepcopy(shaped_next_state)
            action = next_action
            # every time step we do training
            state = copy.deepcopy(next_state)

        agent.model.save_weights("./train/deep_sarsa.h5")
        times += 1

        if e % 100 == 0:
            agent.model.save_weights("./train/deep_sarsa.h5")

    print(times)

    with open('statistics.txt') as f:
        total_time_cost, total_battery_cost, total_failure = env.get_statistics()
        f.write(total_failure / 1000 + "," + total_battery_cost / 1000 + "," + total_time_cost / 1000)
