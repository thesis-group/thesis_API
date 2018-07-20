import copy
import random
import numpy as np
from environment import Env
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential

EPISODES = 1000
Nx = 5  # 卸载率的粒度
M = 5  # 云+MEC个数

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

    # approximate Q function using Neural Network
    # state is input and Q Value of each action is output of network
    # 网络模型使用Sequential模型利用add或list添加，决定网络结构 # TODO
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
            state = np.float32(state)
            q_values = self.model.predict(state)
            return np.argmax(q_values[0])

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


if __name__ == "__main__":
    env = Env()
    agent = DeepSARSAgent()

    global_step = 0
    scores, episodes = [], []

    for e in range(EPISODES):
        done = False
        score = 0
        state = env.reset()
        state = np.reshape(state, [1, 15])

        while not done:
            # fresh env
            global_step += 1

            # get action for the current state and go one step in environment
            action = agent.get_action(state)
            next_state, reward, done = env.step(action, state)
            next_state = np.reshape(next_state, [1, 15])
            next_action = agent.get_action(next_state)
            agent.train_model(state, action, reward, next_state, next_action,
                              done)
            state = next_state
            # every time step we do training
            score += reward

            state = copy.deepcopy(next_state)



        if e % 100 == 0:
            agent.model.save_weights("./save_model/deep_sarsa.h5")
