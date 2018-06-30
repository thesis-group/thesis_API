# coding=utf-8
from model import structs
from reward.reward import reward_back_val
"""
对应原Java项目中的类：
FSCH

类目标：
任务卸载过程
"""


def calculate_offloading(location, task, reward_param):
    """
    按位置卸载
    对应方法：FSCH.calculateFschX
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


def calculate_time(location, task, reward_param):
    """
    计算时间，待定  # TODO
    对应方法：FSCH.calculateTime
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
