#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################
# Author : cndaqiang             #
# Update : 2024-08-18            #
# Build  : 2024-08-18            #
# What   : 更新登录体验服         #
##################################
import sys
import os
import traceback

try:
    from airtest_mobileauto.control import *
except ImportError:
    traceback.print_exc()
    print("模块[airtest_mobileauto]导入不存在, 请安装airtest_mobileauto")
    print("python -m pip install airtest_mobileauto --upgrade")
    from airtest_mobileauto.control import *


class tiyanfu():
    def __init__(self):
        # device
        self.mynode = Settings.mynode
        self.totalnode = Settings.totalnode
        self.LINK = Settings.LINK_dict[Settings.mynode]
        self.移动端 = deviceOB(mynode=self.mynode, totalnode=self.totalnode, LINK=self.LINK)
        self.Tool = DQWheel(var_dict_file=f"{self.移动端.设备类型}.var_dict_{self.mynode}.ce.txt",
                            mynode=self.mynode, totalnode=self.totalnode)
        #
        self.组队模式 = self.totalnode > 1
        self.房主 = self.mynode == 0 or self.totalnode == 1
        # prefix, 还用于创建读取一些特定的控制文件/代码
        # prefix, 用于区分不同进程的字典文件中的图片位置，因为不同账户的位置可能又差异
        self.prefix = f"体验服.{self.mynode}"
        #
        self.设备类型 = self.移动端.设备类型
        self.APPID = "com.tencent.tmgp.sgamece"
        self.APPOB = appOB(APPID=self.APPID, big=True, device=self.移动端)
        #
        self.体验服初始化FILE = f"WZRY.ce.{self.mynode}.临时初始化.txt"
        self.只战一天FILE = f"WZRY.ce.oneday.txt"  # 今天执行完之后，直接结束程序。适用采用crontab等模式周期性运行脚本，而不采用本脚本自带的循环。
        #
        self.timelimit = 60*60*2.0
        # 更新时间
        self.对战时间 = [3.0, 4.0]

    def end(self):
        self.APPOB.关闭APP()
        self.移动端.关闭设备()

    def run(self, times=0):
        if not connect_status():
            self.移动端.连接设备()
        if times == 0:
            self.Tool.timelimit(timekey="登录体验服", limit=self.timelimit, init=True)
        if self.Tool.timelimit(timekey="登录体验服", limit=self.timelimit, init=False):
            TimeECHO("登录体验服超时")
            return
        times = times + 1
        TimeECHO(f"体验服更新中{times}")
        # 模拟器有时候会卡掉，重启设备才能好
        if times > 10 and times % 5 == 4:
            self.移动端.重启设备()
        if times > 10 and times % 5 == 0:
            self.APPOB.重启APP()
        self.APPOB.前台APP(2)
        self.APPOB.打开APP()
        #
        waittime = 10
        # ------------------------------------------------------------------------------
        run_class_command(self=self, command=self.Tool.readfile(self.体验服初始化FILE))
        # ------------------------------------------------------------------------------
        #
        极简下载 = Template(r"tpl1723551085244.png", record_pos=(-0.008, -0.096), resolution=(960, 540), target_pos=6)
        确定按钮 = Template(r"tpl1723551187946.png", record_pos=(-0.003, 0.122), resolution=(960, 540))
        if self.Tool.existsTHENtouch(极简下载, "极简下载", savepos=False):
            self.Tool.existsTHENtouch(确定按钮, "确定按钮", savepos=False)
            sleep(waittime)
        if self.Tool.existsTHENtouch(确定按钮, "确定按钮", savepos=False):
            sleep(waittime)
        #
        退出更新图标 = Template(r"tpl1723551006031.png", record_pos=(-0.036, 0.196), resolution=(960, 540))
        更新图标 = Template(r"tpl1723551024328.png", record_pos=(0.059, 0.199), resolution=(960, 540))
        if exists(退出更新图标):
            TimeECHO("检测到更新图标")
            self.Tool.existsTHENtouch(更新图标, "更新图标", savepos=True)
            sleep(waittime)
        self.Tool.existsTHENtouch(更新图标, "更新图标", savepos=False)
        # 更新中
        更新中 = Template(r"tpl1723959879694.png", record_pos=(-0.358, 0.244), resolution=(960, 540))
        if exists(更新中):
            TimeECHO("正在更新中....")
            sleep(waittime)
        #
        确定重启 = Template(r"tpl1723960034528.png", record_pos=(-0.001, 0.116), resolution=(960, 540), threshold=0.9)
        if self.Tool.existsTHENtouch(确定重启, "体验服.确定重启", savepos=False):
            TimeECHO("确定重启")
            sleep(waittime)
        # MuMu模拟器的安装元素
        MuMu安装 = Template(r"tpl1724563572426.png", record_pos=(-0.013, -0.005), resolution=(960, 540), target_pos=7)
        self.安装元素 = []
        self.安装元素.append(Template(r"tpl1723551109493.png", record_pos=(-0.349, -0.202), resolution=(960, 540)))
        self.安装元素.append(Template(r"tpl1723551120394.png", record_pos=(0.415, 0.243), resolution=(960, 540)))
        self.安装元素.append(Template(r"tpl1723551138518.png", record_pos=(-0.001, -0.033), resolution=(960, 540)))
        self.安装元素.append(Template(r"tpl1723973068687.png", record_pos=(-0.017, -0.175), resolution=(960, 540)))
        self.安装元素.append(Template(r"tpl1724466523208.png", record_pos=(-0.005, -0.161), resolution=(960, 540)))
        self.安装元素.append(MuMu安装)
        self.安装元素.append(Template(r"tpl1724936641621.png", record_pos=(-0.142, -0.033), resolution=(960, 540)))
        self.安装按钮 = []
        self.安装按钮.append(Template(r"tpl1723551120394.png", record_pos=(0.415, 0.243), resolution=(960, 540), target_pos=6))
        self.安装按钮.append(Template(r"tpl1723993720207.png", record_pos=(-0.001, 0.18), resolution=(960, 540)))
        self.安装按钮.append(Template(r"tpl1724466528191.png", record_pos=(0.075, 0.237), resolution=(960, 540)))
        self.安装按钮.append(MuMu安装)
        self.安装按钮.append(Template(r"tpl1724936646196.png", record_pos=(0.209, 0.051), resolution=(960, 540)))

        安装界面, self.安装元素 = self.Tool.存在任一张图(self.安装元素, "体验服.安装元素")
        if 安装界面:
            for i in self.安装按钮:
                self.Tool.existsTHENtouch(i, f"安装按钮{i}", savepos=False)
            sleep(waittime)
            self.APPOB.重启APP()
        #
        #
        关闭界面 = Template(r"tpl1723551215061.png", record_pos=(0.323, -0.202), resolution=(960, 540))
        关闭按钮 = Template(r"tpl1723551244924.png", record_pos=(0.425, -0.205), resolution=(960, 540))
        if exists(关闭界面):
            self.Tool.existsTHENtouch(关闭按钮, "关闭按钮", savepos=True)
        self.Tool.existsTHENtouch(关闭按钮, "其他关闭按钮", savepos=False)
        #
        self.登录元素 = []
        self.登录元素.append(Template(r"tpl1723551454028.png", record_pos=(0.0, -0.005), resolution=(960, 540)))
        self.登录元素.append(Template(r"tpl1723960220809.png", record_pos=(-0.002, 0.128), resolution=(960, 540)))
        self.登录元素.append(Template(r"tpl1723960588665.png", record_pos=(-0.107, 0.159), resolution=(960, 540)))
        登录协议, self.登录元素 = self.Tool.存在任一张图(self.登录元素, "体验服.登录元素")
        if 登录协议:
            TimeECHO("检测到登录协议")
            self.Tool.touchfile(f"WZRY.ce.{self.mynode}.重新登录.txt")
            # 5 分钟后不行就退出
            self.Tool.timedict["登录体验服"] = min(self.Tool.timedict["登录体验服"], time.time()-self.timelimit+60*5)
        确定协议 = Template(r"tpl1723961775100.png", record_pos=(-0.002, 0.115), resolution=(960, 540))
        同意协议 = Template(r"tpl1723968991405.png", record_pos=(0.061, 0.097), resolution=(960, 540))
        self.Tool.existsTHENtouch(确定协议, "确定协议", savepos=False)
        self.Tool.existsTHENtouch(同意协议, "同意协议", savepos=False)
        #
        开始游戏 = Template(r"tpl1723551226168.png", record_pos=(-0.003, 0.155), resolution=(960, 540))
        if self.Tool.existsTHENtouch(开始游戏, "开始游戏", savepos=False):
            sleep(waittime)
        if self.Tool.existsTHENtouch(开始游戏, "开始游戏", savepos=False):
            TimeECHO("还存在开始游戏，有可能体验服正在更新")
            return False
        #
        self.Tool.LoopTouch(关闭按钮, "关闭按钮", loop=5, savepos=False)
        #
        self.大厅元素 = []
        self.大厅元素.append(Template(r"tpl1723551269026.png", record_pos=(0.455, 0.203), resolution=(960, 540)))
        self.大厅元素.append(Template(r"tpl1723551278162.png", record_pos=(-0.003, 0.142), resolution=(960, 540)))
        self.大厅元素.append(Template(r"tpl1723551299495.png", record_pos=(-0.461, -0.249), resolution=(960, 540)))
        self.大厅元素.append(Template(r"tpl1723551309461.png", record_pos=(0.354, -0.252), resolution=(960, 540)))
        大厅中, self.大厅元素 = self.Tool.存在任一张图(self.大厅元素, "体验服.大厅元素")
        if 大厅中:
            return True
        else:
            return self.run(times)

    def looprun(self, times=0):
        times = times + 1
        startclock = self.对战时间[0]
        endclock = self.对战时间[1]
        while True:
            leftmin = self.Tool.hour_in_span(startclock, endclock)*60.0
            if leftmin > 0:
                TimeECHO("剩余%d分钟进入新的一天" % (leftmin))
                self.APPOB.关闭APP()
                self.移动端.重启重连设备(leftmin*60)
                continue
            times = times+1
            TimeECHO("="*10)
            self.run()


if __name__ == "__main__":
    config_file = ""
    if len(sys.argv) > 1:
        config_file = str(sys.argv[1])
    Settings.Config(config_file)
    ce = tiyanfu()
    ce.run()
    if os.path.exists(ce.只战一天FILE):
        ce.end()
        exit()
    ce.looprun()
    exit()
