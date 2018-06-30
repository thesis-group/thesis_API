# coding=utf-8
from model import structs
from reward import strategy

"""
对应原Java项目中的类：
Reward、RewardBackValue

方法目标：
根据策略获取相应回报值
"""


class reward_back_val(object):
    """
    回报返回值模型，对应RewardBackValue类
    """
    def __init__(self, fail_rate, rtt, cost):
        """
        回报返回值模型构造方法
        :param fail_rate: 任务失败率
        :param rtt: 任务最长执行时间
        :param cost: 任务执行代价
        """
        self.fail_rate = fail_rate
        self.rtt = rtt
        self.cost = cost


def get_reward(state, strategy, task):
    """
    计算回报值
    对应方法：Reward.getReward
    :param state: 状态
    :param strategy: 策略
    :param task: 任务
    :type state: structs.state
    :type task: structs.task
    :type task: strategy
    :return: 回报值
    :rtype: reward_back_val
    """
    pass
