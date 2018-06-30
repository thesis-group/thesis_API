# coding=utf-8
from model import structs
from reward import strategy


"""
对应原Java项目中的类：
Learning2、Learning2Service、Learning2Para

类目标：
实现训练过程
"""


def train_state(location, map, state):
    """
    不同调度位置的训练方法
    :param location: 调度位置(0 - 本地; 1 - MEC; 2 - 云服务器)
    :param map: 状态值-<策略，回报值>映射
    :param state: 状态
    :type location: int
    :type map: 待定 # TODO
    :type state: structs.state
    :return: 调度策略
    :rtype: strategy
    """
    pass
