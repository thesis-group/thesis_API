# coding=utf-8
from model import structs
from param import reward_param
from reward.reward import reward_back_val

"""
对应原Java项目中的类：
Strategy

类目标：
选择相应策略的计算过程
"""


def calculate_reward(location, task, reward_param):
    """
    计算策略回报值
    对应方法：Strategy.calculateReward
    :param location: 调度位置(0 - 本地; 1 - MEC; 2 - 云服务器)
    :param task: 任务
    :param reward_param: 回报参数
    :type location: int
    :type task: structs.task
    :type reward_param: reward_param
    :return: 策略回报值
    :rtype: reward_back_val
    """
    pass
