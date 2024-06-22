import CommunicationTool

# 生成控制指令（参考案例）
jidong_time = [5000, 2500, 3000, 4000, 4500, 5500]

def create_action_cmd(info, step_num):
    if (step_num <= jidong_time[0]):
        output_cmd = CommunicationTool.SendData()
        output_cmd.sPlaneControl.CmdIndex = 1 # 动作序号 从1开始累加 参数变化而机动类型不变时可以不更新
        output_cmd.sPlaneControl.CmdID = 1 # 动作编号 1:等速平飞
        if (step_num == jidong_time[0]):
            output_cmd.sPlaneControl.isApplyNow = False # true:立即应用 false：完成前序命令后应用 目前默认为true
        output_cmd.sPlaneControl.isApplyNow = True
        output_cmd.sPlaneControl.CmdHeadingDeg = 180 # 目标航向 度 -180~+180

        output_cmd.sPlaneControl.CmdAlt = 10000 # safe 安全高度 目标高度 m 与飞行包线有关 <16000m
        output_cmd.sPlaneControl.CmdSpd = 0.9 # 目标速度或限制速度 m/s 或 mach
        output_cmd.sPlaneControl.TurnDirection = 1 # 转弯方向 1 右转 -1左转 0默认就近转

        # if len(info.AttackEnemyList) != 0: # 攻击列表内存在敌方战机
        #     # for enen in info.AttackEnemyList:
        #     #     print("enen", enen.EnemyID ,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #     #     # 如果enen的ID不在tar_ID中，就把他加入tar_ID
        #     #     if (enen.TargetDis <= enen.MissilePowerfulDis) and info.MissileNowNum > 0:
        #     #         output_cmd.sOtherControl.isLaunch = 1
        #     #     else:
        #     #         # 攻击列表内不存在敌方战机 没有发射导弹
        #     #         output_cmd.sOtherControl.isLaunch = 0
        #     #         output_cmd.sSOCtrl.NTSEntityIdAssigned = enen.EnemyID

        #         if info.AttackEnemyList[0].NTSstate == 0: # NTS状态 0: 未指令 1: 已指令
        #             output_cmd.sSOCtrl.isNTSAssigned = 1 # 是否指令 0: 未指令 1: 已指令
        #     # if (info.AttackEnemyList[0].TargetDis <= info.AttackEnemyList[0].MissilePowerfulDis) and info.MissileNowNum > 0:
        #     #     output_cmd.sOtherControl.isLaunch = 1
        #     # else:
        #     #     # 攻击列表内不存在敌方战机 没有发射导弹
        #     #     output_cmd.sOtherControl.isLaunch = 0
        #     #     output_cmd.sSOCtrl.NTSEntityIdAssigned = info.AttackEnemyList[0].EnemyID

        #     # if info.AttackEnemyList[0].NTSstate == 0: # NTS状态 0: 未指令 1: 已指令
        #     #     output_cmd.sSOCtrl.isNTSAssigned = 1 # 是否指令 0: 未指令 1: 已指令
        if len(info.AttackEnemyList) != 0:# 存放Attackinfo类
            min_dis_index = 0   
            Dis_list = []
            for i in range(4):
                Dis_list.append(info.AttackEnemyList[i].TargetDis)
                min_dis_index = Dis_list.index(min(Dis_list))
            for i in range(4):
                if i == min_dis_index:
                    info.FoundEnemyList[i].isNTS = True
                    info.AttackEnemyList[i].NTSstate=1
                else:
                    info.FoundEnemyList[i].isNTS = False
                    info.AttackEnemyList[i].NTSstate = 0
            if info.AttackEnemyList[min_dis_index].TargetDis - 10000 <= info.AttackEnemyList[min_dis_index].MissilePowerfulDis and info.MissileNowNum > 0:# 判断武器是否发射
            # if info.MissileNowNum > 0:# 判断武器是否发射
                output_cmd.sOtherControl.isLaunch = 1#导弹发射指令
            else:
            #攻击列表内不存在敌方战机没有发射导弹
                output_cmd.sOtherControl.isLaunch = 0
                output_cmd.sSOCtrl.NTSEntityIdAssigned = info.AttackEnemyList[min_dis_index].EnemyID
            if info.AttackEnemyList[min_dis_index].NTSstate != 0:# 是否被NTS标识
                output_cmd.sSOCtrl.isNTSAssigned = 1#对目标NTS指定
    else:
        output_cmd = CommunicationTool.SendData()
        output_cmd.sPlaneControl.CmdIndex = 7 # 动作序号 从1开始累加 参数变化而机动类型不变时可以不更新
        output_cmd.sPlaneControl.CmdID = 1 # 动作编号 1:等速平飞
        output_cmd.sPlaneControl.VelType = 0 # 动作序号 从1开始累加 参数变化而机动类型不变时可以不更新
        output_cmd.sPlaneControl.CmdSpd = 0.9
        if (step_num == jidong_time[4]):
            output_cmd.sPlaneControl.isApplyNow = False
        output_cmd.sPlaneControl.isApplyNow = True
        output_cmd.sPlaneControl.CmdHeadingDeg = 180
        output_cmd.sPlaneControl.CmdAlt = 5000

    return output_cmd


# 规整上升沿
def check_cmd(cmd, last_cmd):
    # cmd.sOtherControl.isLaunch = 0
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
        #     print(platform.recv_info.MissileTrackList[0].TargetID, "000000000000000000")
        cmd_created = create_action_cmd(platform.recv_info, platform.step)  # 生成控制指令

        # 保存上一个发送的指令
        cmd_created = check_cmd(cmd_created, save_last_cmd[plane][0])  # 比较得到上升沿
        save_last_cmd[plane][0] = cmd_created  # 更新保存指令
        platform.cmd_struct_queue.put(cmd_created)  # 发送数据
        # save_last_cmd[plane][1] = save_last_cmd[plane][1] + 1
        save_last_cmd[plane][1] = platform.step


def main(IP, Port, drone_num):
    data_serv = CommunicationTool.DataService(IP, Port, drone_num)
    data_serv.run()  # Start the simulation environment.
    
    global save_last_cmd 
    save_last_cmd = {}

    for plane in data_serv.platforms:
        save_last_cmd[plane] = [None, 0]

    while True:
        try:
            for plane in data_serv.platforms:
                solve(data_serv.platforms[plane], plane)
                print(plane, "'s step is  ", data_serv.platforms[plane].step)
        except Exception as e:
            print("Error break", e)
            break
        # tar_ID = [1]
    data_serv.close()


if __name__ == "__main__":
    IP = "192.168.0.112"
    Port = 60010
    drone_num = 4
    main(IP, Port, drone_num)

