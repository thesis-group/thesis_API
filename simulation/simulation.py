# coding=utf-8
"""
对应原Java项目中的类：
Simulation、SimulationsInput、SimulationOut

类目标：
实现模拟过程
"""


def simulation_start():
    """
    开始模拟
    对应方法：SimulationsInput.simulationStart
    """
    pass


def schedule(map, tasks, beta, n):
    """
    调度
    对应方法：Simulation.DiaoDu
    :param map: 状态值-<策略，回报值>映射
    :param tasks: 任务列表
    :param beta: fsch判断阈值
    :param n: 
    :type map: map<State,map<stategy,double>>
    :type tasks: tasks[]
    :type beta: double
    :type n: int
    """
    pass


def learning(map, state):
    """
    学习
    对应方法：Simulation.learningA
    :param map: 状态值-<策略，回报值>映射
    :param state: 状态
    :type map: map<State,map<stategy,double>>
    :type state: struts.state
    :return: 调度策略
    :rtype: strategy
    """
    pass


def environment_simulation(param):
    """
    模拟环境
    对应方法：Simulation.enviroSimulation
    :param param: 环境参数
    :type param: param
    :return: 环境
    :rtype: environment
    """
    pass


def calculate_reward(state, strategy, task, n):
    """
    选择动作
    对应方法：Simulation.SelectAction
    :param state: 状态
    :param strategy: 策略
    :param task: 任务
    :type state: struts.state
    :type task: task
    :type strategy: strategy
    :return: reword
    :rtype: reword
    """
    pass


def select_action(map, state, task):
    """
    选择Strategy
    对应方法：Simulation.SelectAction
    :param map: 状态值-<策略，回报值>映射
    :param state: 状态
    :param task: 任务
    :type map: map<state,map<strategy,double>>
    :type state: struts.state
    :type task: task
    :return: 策略
    :rtype: strategy
    """
    pass


def poisson_process(p_lamda):
    """
    模拟泊松过程
    对应方法：Simulation.RandExp
    :param p_lamda: 参数
    :type p_lamda: double
    :return: 随机密度
    :rtype: double
    """
    pass
