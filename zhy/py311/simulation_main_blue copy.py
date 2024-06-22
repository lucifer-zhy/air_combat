# from CommunicationTool import *
import CommunicationTool

# 生成控制指令（参考案例）
jidong_time = [500, 2500, 3000, 4000, 4500, 5500]


def create_action_cmd(info, step_num):
    if (step_num <= jidong_time[0]):
        output_cmd = CommunicationTool.SendData()
        output_cmd.sPlaneControl.CmdIndex = 1
        output_cmd.sPlaneControl.CmdID = 1
        if (step_num == jidong_time[0]):
            output_cmd.sPlaneControl.isApplyNow = False
        output_cmd.sPlaneControl.isApplyNow = True
        output_cmd.sPlaneControl.CmdHeadingDeg = 180

        output_cmd.sPlaneControl.CmdAlt = 10000
        output_cmd.sPlaneControl.CmdSpd = 0.9
        output_cmd.sPlaneControl.TurnDirection = 1
        if len(info.AttackEnemyList) != 0:
            if info.AttackEnemyList[0].TargetDis / 1000 <= \
                            info.AttackEnemyList[0].MissilePowerfulDis and info.MissileNowNum > 0:
                # 判断武器是否发射
                output_cmd.sOtherControl.isLaunch = 1
            else:
                # 攻击列表内不存在敌方战机 没有发射导弹
                output_cmd.sOtherControl.isLaunch = 0

                output_cmd.sSOCtrl.NTSEntityIdAssigned = info.AttackEnemyList[0].EnemyID

            if info.AttackEnemyList[0].NTSstate == 0:
                output_cmd.sSOCtrl.isNTSAssigned = 1

    # elif (step_num <= jidong_time[1]):
    #     output_cmd = SendData()
    #     output_cmd.sPlaneControl.CmdIndex = 1
    #     output_cmd.sPlaneControl.CmdID = 1
    #     if (step_num == jidong_time[1]):
    #         output_cmd.sPlaneControl.isApplyNow = False
    #     output_cmd.sPlaneControl.isApplyNow = True
    #     output_cmd.sPlaneControl.CmdHeadingDeg = 180
    #     output_cmd.sPlaneControl.CmdAlt = 10000
    #     output_cmd.sPlaneControl.CmdSpd = 0.9
    #     output_cmd.sPlaneControl.TurnDirection = 1
    #     # output_tosend = SedTotalCom(output_cmd)
    #     # init_action_bytes = string_at(addressof(output_tosend), sizeof(output_tosend))
    #     # sock.send(init_action_bytes)
    # elif (step_num <= jidong_time[2]):
    #     output_cmd = SendData()
    #     output_cmd.sPlaneControl.CmdIndex = 3
    #     output_cmd.sPlaneControl.CmdID = 1
    #     output_cmd.sPlaneControl.VelType = 0
    #     output_cmd.sPlaneControl.CmdSpd = 0.9
    #     if (step_num == jidong_time[2]):
    #         output_cmd.sPlaneControl.isApplyNow = False
    #     output_cmd.sPlaneControl.isApplyNow = True
    #     output_cmd.sPlaneControl.CmdHeadingDeg = 180
    #     output_cmd.sPlaneControl.CmdAlt = 10000
    #     # output_tosend = SedTotalCom(output_cmd)
    #     # init_action_bytes = string_at(addressof(output_tosend), sizeof(output_tosend))
    #     # sock.send(init_action_bytes)
    # elif (step_num <= jidong_time[3]):
    #     output_cmd = SendData()
    #     output_cmd.sPlaneControl.CmdIndex = 4
    #     output_cmd.sPlaneControl.CmdID = 7
    #     output_cmd.sPlaneControl.VelType = 0
    #     output_cmd.sPlaneControl.CmdSpd = 0.8
    #     if (step_num == jidong_time[3]):
    #         output_cmd.sPlaneControl.isApplyNow = False
    #     output_cmd.sPlaneControl.isApplyNow = True
    #     output_cmd.sPlaneControl.CmdPitchDeg = -20
    #     output_cmd.sPlaneControl.CmdHeadingDeg = 180
    #     output_cmd.sPlaneControl.CmdAlt = 4000
    #     # output_tosend = SedTotalCom(output_cmd)
    #     # init_action_bytes = string_at(addressof(output_tosend), sizeof(output_tosend))
    #     # sock.send(init_action_bytes)
    # elif (step_num <= jidong_time[4]):
    #     output_cmd = SendData()
    #     output_cmd.sPlaneControl.CmdIndex = 5
    #     output_cmd.sPlaneControl.CmdID = 1
    #     output_cmd.sPlaneControl.VelType = 0
    #     output_cmd.sPlaneControl.CmdSpd = 0.9
    #     if (step_num == jidong_time[4]):
    #         output_cmd.sPlaneControl.isApplyNow = False
    #     output_cmd.sPlaneControl.isApplyNow = True
    #     output_cmd.sPlaneControl.CmdHeadingDeg = 180
    #     output_cmd.sPlaneControl.CmdAlt = 5000
    #     # output_tosend = SedTotalCom(output_cmd)
    #     # init_action_bytes = string_at(addressof(output_tosend), sizeof(output_tosend))
    #     # sock.send(init_action_bytes)
    # elif (step_num <= jidong_time[5]):
    #     output_cmd = SendData()
    #     output_cmd.sPlaneControl.CmdIndex = 6
    #     output_cmd.sPlaneControl.CmdID = 3
    #     output_cmd.sPlaneControl.VelType = 0
    #     output_cmd.sPlaneControl.CmdSpd = 0.9
    #     if (step_num == jidong_time[5]):
    #         output_cmd.sPlaneControl.isApplyNow = False
    #     output_cmd.sPlaneControl.isApplyNow = True
    #     output_cmd.sPlaneControl.CmdHeadingDeg = 180
    #     # output_tosend = SedTotalCom(output_cmd)
    #     # init_action_bytes = string_at(addressof(output_tosend), sizeof(output_tosend))
    #     # sock.send(init_action_bytes)
    else:
        output_cmd = CommunicationTool.SendData()
        output_cmd.sPlaneControl.CmdIndex = 7
        output_cmd.sPlaneControl.CmdID = 1
        output_cmd.sPlaneControl.VelType = 0
        output_cmd.sPlaneControl.CmdSpd = 0.9
        # if (step_num == jidong_time[4]):
        #     output_cmd.sPlaneControl.isApplyNow = False
        output_cmd.sPlaneControl.isApplyNow = True
        output_cmd.sPlaneControl.CmdHeadingDeg = 180
        output_cmd.sPlaneControl.CmdAlt = 5000

    return output_cmd


# 规整上升沿
def check_cmd(cmd, last_cmd):
    # if last_cmd is None:
    #     cmd.sPlaneControl.isApplyNow = False
    #     cmd.sOtherControl.isLaunch = 0
    #     cmd.sSOCtrl.isNTSAssigned = 0
    # else:
    #     if cmd.sPlaneControl == last_cmd.sPlaneControl:
    #         cmd.sPlaneControl.isApplyNow = False
    #     if cmd.sSOCtrl == last_cmd.sSOCtrl:
    #         cmd.sSOCtrl.isNTSAssigned = 0
    return cmd


# 获取传输数据，生成对应无人机command指令，并传输指令逻辑
def solve(platform, plane):
    global save_last_cmd

    if platform.step > save_last_cmd[plane][1]:
        # if platform.recv_info.MissileTrackList[0].WeaponID != 0:
        #     print(platform.recv_info.DroneID, ":  vars(MissileTrackList[0])", vars(platform.recv_info.MissileTrackList[0]))
        cmd_created = create_action_cmd(platform.recv_info, platform.step)  # 生成控制指令
        # 保存上一个发送的指令
        save_last_cmd[plane][0] = cmd_created  # 更新保存指令

        cmd_created = check_cmd(cmd_created, save_last_cmd[plane][0])  # 比较得到上升沿
        platform.cmd_struct_queue.put(cmd_created)  # 发送数据
        save_last_cmd[plane][1] = save_last_cmd[plane][1] + 1


def main(IP, Port, drone_num):
    data_serv = CommunicationTool.DataService(IP, Port, drone_num)  # 本机IP与设置的端口，使用config文件
    print("Ready!")
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
    Port = 60010
    drone_num = 4
    main(IP, Port, drone_num)

