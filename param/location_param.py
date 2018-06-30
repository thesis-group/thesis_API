# coding=utf-8
"""
对应原Java项目中的类：
LocalParam、CloudletParam

文件目标：
定义与卸载位置相关的参数
"""

# 列出了可供参考的参数，请根据实际情况修改，将来可删 # TODO
"""
    Local:
    public static double fl; //本地故障率 .
    public static double eCpu; //单位处理能耗 .
    public static double cPen; //单位数百乘法 .
    public static double cl; //单位处理花销
    
    
    Cloud:
    public static double fUp;      //数据上传的故障率 .
    public static double fDown;    //数据下载的故障率 .
    public static double cCloudlet;//单位处理花销 .
    public static double eUp;      //单位数据传输能耗（上传） .
    public static double eDown;    //单位数据传输能耗（下载） .
    public static double cPen;     //单位失败惩罚 .
    public static double sCloudlet;//薄云处理速度 .
    public static double rUp;      //数据传输率（上传） .
    public static double rDown;    //数据传输率（下载） .

    public static double delta;    //拥塞程度
"""
local_fail_rate = 0.0  # 本地调度故障率
local_e = 0.0  # 本地单位处理能耗
local_s = 0.0  # 本地单位处理速度
local_c = 0.0  # 本地单位处理开销

cloud_up_fail_r = 0.0  # 云服务器上传故障率
cloud_down_fail_r = 0.0  # 云服务器下载故障率
cloud_c = 0.0  # 云服务器单位处理开销
cloud_e_up = 0.0  # 云服务器单位上传能耗
cloud_e_down = 0.0  # 云服务器单位下载能耗
cloud_s = 0.0  # 云服务器单位处理速度
cloud_up_rate = 0.0  # 云服务器数据传输率(上传)
cloud_down_rate = 0.0  # 云服务器数据传输率(下载)

mec_up_fail_r = 0.0  # MEC上传故障率
mec_down_fail_r = 0.0  # MEC下载故障率
mec_c = 0.0  # MEC单位处理开销
mec_e_up = 0.0  # MEC单位上传能耗
mec_e_down = 0.0  # MEC单位下载能耗
mec_s = 0.0  # MEC单位处理速度
mec_up_rate = 0.0  # MEC数据传输率(上传)
mec_down_rate = 0.0  # MEC数据传输率(下载)
