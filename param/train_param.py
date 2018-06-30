# coding=utf-8
"""
对应原Java项目中的类：
TrainParam

文件目标：
定义与训练相关的参数
"""

# 列出了可供参考的参数，请根据实际情况修改，将来可删 # TODO
"""
    public static String savepath = "./test.txt"; //保存文件路径 原来的路径 + 文件名
    public static int iter ;  // 训练迭代次数
    public static double epsilon; //贪心算法选定的epsilon值
    public static double temp; //softmax算法需要的温度

    public static int rest; //剩余生命周期
    public static int k;  //最大执行次数上限
    public static double wl; //工作负载
    public static double ip; //输入数据量
    public static double op; //输出数据量
    public static double rtt; //训练任务指定rtt
    public static double lifespan; //训练指定任务的生命周期
"""

file_path = ''  # 文件路径
iter = 0  # 训练迭代次数
epsilon = 0.0  # epsilon值

rest = 0  # 剩余生命周期
work_load = 0.0  # 工作负载
input_data = 0.0  # 输入数据量
output_data = 0.0  # 输出数据量
rtt = 0.0  # 任务rtt
lifespan = 0.0  # 任务生命周期
