import socket
import threading
from ctypes import *
import ClassName
import AiScenarioDef
import time
import CommunicationTool

# 生成蓝方的控制指令
def create_blue_action_cmd(info, step_num):
    output_cmd = CommunicationTool.SendData()
    if info.isNTS:
        if info.TargetDis < 10000:  # 距离小于10km时发射导弹
            output_cmd.sOtherControl.isLaunch = 1
            output_cmd.sOtherControl.TargetID = info.EnemyID
        else:
            output_cmd.sOtherControl.isLaunch = 0
    else:
        output_cmd.sOtherControl.isLaunch = 0
    
    # 控制指令参数设定
    output_cmd.sPlaneControl.CmdIndex = step_num
    output_cmd.sPlaneControl.CmdID = 1
    output_cmd.sPlaneControl.VelType = 0
    output_cmd.sPlaneControl.CmdSpd = 0.9
    output_cmd.sPlaneControl.CmdHeadingDeg = info.TargetYaw * 180 / 3.14159
    output_cmd.sPlaneControl.CmdAlt = 10000  # 可以根据需要调整
    output_cmd.sPlaneControl.isApplyNow = True
    
    return output_cmd

# 规整上升沿
def check_cmd(cmd, last_cmd):
    if last_cmd is None:
        cmd.sPlaneControl.isApplyNow = False
        cmd.sOtherControl.isLaunch = 0
        cmd.sSOCtrl.isNTSAssigned = 0
    else:
        if cmd.sPlaneControl == last_cmd.sPlaneControl:
            cmd.sPlaneControl.isApplyNow = False
        if cmd.sSOCtrl == last_cmd.sSOCtrl:
            cmd.sSOCtrl.isNTSAssigned = 0
    return cmd

# 获取传输数据，生成对应无人机command指令，并传输指令逻辑
def solve(platform, plane):
    global save_last_cmd

    if platform.step > save_last_cmd[plane][1]:
        if platform.recv_info.AlarmList[0].MisAzi != 0:
            print(platform.recv_info.DroneID, ": vars(AlarmList[0])", vars(platform.recv_info.AlarmList[0]))
        cmd_created = create_blue_action_cmd(platform.recv_info, platform.step)  # 生成控制指令
        # 保存上一个发送的指令
        save_last_cmd[plane][0] = cmd_created  # 更新保存指令

        cmd_created = check_cmd(cmd_created, save_last_cmd[plane][0])  # 比较得到上升沿
        platform.cmd_struct_queue.put(cmd_created)  # 发送数据
        save_last_cmd[plane][1] = save_last_cmd[plane][1] + 1

def main(IP, Port, drone_num):
    # data_serv = DataService(IP, Port, drone_num)  # 本机IP与设置的端口，使用config文件
    data_serv = CommunicationTool.DataService(IP, Port, drone_num)
    data_serv.run()  # 启动仿真环境
    print("data_serv.run()")

    global save_last_cmd  # 用于比较指令变化的字典全局变量
    save_last_cmd = {}

    for plane in data_serv.platforms:  # 初始化全局变量为None
        save_last_cmd[plane] = [None, 0]

    while True:  # 交互循环
        try:
            for plane in data_serv.platforms:
                solve(data_serv.platforms[plane], plane)  # 处理信息
                print(plane, "'s step is  ", data_serv.platforms[plane].step)
        except Exception as e:
            print("Error break", e)
            break
        
    data_serv.close()

if __name__ == "__main__":
    IP = "192.168.0.104"
    Port = 60001
    drone_num = 4
    main(IP, Port, drone_num)
