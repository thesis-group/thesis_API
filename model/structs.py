# coding=utf-8
"""
对应原Java项目中的类：
State、Task

文件目标：
定义训练状态模型和任务模型
"""


class state(object):
    """
    状态模型
    """

    def __init__(self, args):
        self.bandwidth = [0, 0, 0, 0, 0]
        self.energy_estimate = 0.0
        self.battery = 0.0
        self.task_len = 0
        self.rest = 0.0

        """
        状态模型构造方法
        :param args: 暂时不知道有哪些参数  # TODO
        """
        self.args = args

    def equals(self):
        """
        判断两个状态是否是同一状态
        :return: 判断结果
        :rtype: bool
        """
        pass


class task(object):
    # 剩余生命周期
    rest = 0.0
    # 任务的到达时间
    arrivalTime = 0
    # 需计算数据量
    cd = 0.0
    # 传出数据量
    rd = 0.0

    """
    任务模型
    """

    def __init__(self, args):
        # 剩余生命周期
        self.rest = 0.0
        # 任务的到达时间
        self.arrivalTime = 0
        # 需计算数据量
        self.cd = 0.0
        # 传出数据量
        self.rd = 0.0

        """
        任务模型构造方法
        :param args: 暂时不知道有哪些参数  # TODO
        参数参考：
        private double rest; //剩余生命周期
        private int k;  //最大执行次数上限
        private double wl; //工作负载
        private double ip; //输入数据量
        private double op; //输出数据量
        private double wait;//任务在队列中的等待时间
        """
        self.args = args
