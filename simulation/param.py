# coding=utf-8
"""
对应原Java项目中的类：
Parameter、OperatingTimes

文件目标：
定义过程参数
"""

# 列出了可供参考的参数，请根据实际情况修改，将来可删 # TODO
"""
   public static  double fl = 0.1;
   public static  double fup = 0.15;
   public static  double fdown = 0.12;
   public static  double ft = 0.12;
   public static  double fad = 0.05;
   public static  double ps = 0.5;
   public static  double lamdan = 25;
   public static  double lamdaq =0.25;
   public static  double lamdac = 0.1;
   public static  double a = 1;
   public static  double p = 0.5;  //Z转移概率
   public static  Strategy str;
   
   public static double beita = 0.6;    //fsch判断阈值
   public static  int x = 0; //greedy算法选择 0在线 or 1离线
   public static final int n = 1;	//greedy算法选择 0reward or 1fsch
"""
local_fail_rate = 0.0  # 本地调度故障率

cloud_up_fail_r = 0.0  # 云服务器上传故障率
cloud_down_fail_r = 0.0  # 云服务器下载故障率

p = 0.5  # Z转移概率
beta = 0.6  # fsch判断阈值
