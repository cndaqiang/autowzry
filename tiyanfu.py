#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# autowzry · 自动化农活演示
# Copyright (C) 2025 cndaqiang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

##################################
# Author : cndaqiang             #
# Update : 2024-12-08            #
# Build  : 2024-08-18            #
# What   : 更新登录体验服         #
##################################
import sys
import os
import traceback

try:
    from airtest_mobileauto import *
except ImportError:
    traceback.print_exc()
    print("模块 [airtest_mobileauto] 导入不存在，请安装 airtest_mobileauto")
    print("运行以下命令安装：")
    print("python -m pip install airtest_mobileauto --upgrade")
    raise ImportError("模块 [airtest_mobileauto] 导入失败")


class tiyanfu():
    def __init__(self):
        # 静态资源
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, 'assets')
        Settings.figdirs.append(assets_dir)
        seen = set()
        Settings.figdirs = [x for x in Settings.figdirs if not (x in seen or seen.add(x))]
        #
        # device
        self.mynode = Settings.mynode
        self.totalnode = Settings.totalnode
        self.LINK = Settings.LINK_dict[Settings.mynode]
        self.移动端 = deviceOB(mynode=self.mynode, totalnode=self.totalnode, LINK=self.LINK)
        # Tool
        dictfile = f"{self.移动端.设备类型}.var_dict_{self.mynode}.ce.yaml"
        # 预设的分辨率对应的触点文件
        dictreso = os.path.join(assets_dir, f"{max(self.移动端.resolution)}.{min(self.移动端.resolution)}.dict.yaml")
        loaddict = not os.path.exists(dictfile) and os.path.exists(dictreso)
        self.Tool = DQWheel(var_dict_file=dictfile, mynode=self.mynode, totalnode=self.totalnode)
        if loaddict:
            try:
                TimeECHO(f"检测到本程序第一次运行，且分辨率为{self.移动端.resolution}, 加载预设字典中....")
                self.Tool.var_dict = self.Tool.read_dict(dictreso)
                self.Tool.save_dict(self.Tool.var_dict, dictfile)
            except:
                traceback.print_exc()
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
        self.内置循环 = False  # 是否每日循环执行此脚本
        #
        self.timelimit = 60*60*0.5
        # 更新时间
        self.对战时间 = [0.1, 23.9]

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
        # 修正分辨率, 避免某些模拟器返回的分辨率不对
        if self.移动端.resolution[0] < self.移动端.resolution[1]:
            TimeECHO("=>"*20)
            TimeECHO(f"⚠️ 警告: 分辨率 ({ self.移动端.resolution}) 不符合 (宽, 高) 格式，正在修正...")
            self.移动端.resolution = (max(self.移动端.resolution), min(self.移动端.resolution))
            TimeECHO("<="*20)
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
        # 不同版本的安卓、不同模拟器的安装界面区别较大，仅对MuMu进行适配
        # MuMu模拟器的安装元素
        王者图标 = Template(r"tpl1730462743001.png", record_pos=(-0.218, -0.049), resolution=(960, 540))
        更新按钮 = Template(r"tpl1724936646196.png", record_pos=(0.209, 0.051), resolution=(960, 540))
        self.安装元素 = [王者图标, 更新按钮]

        安装界面, self.安装元素 = self.Tool.存在任一张图(self.安装元素, "体验服.安装元素")
        if 安装界面:
            if self.Tool.existsTHENtouch(更新按钮, f"体验服.更新按钮", savepos=False):
                sleep(waittime)
                self.APPOB.重启APP()
        # 体验服随便点无所谓 不用追求太逻辑和完美，就直接点以前的更新坐标
        self.Tool.touch_record_pos(更新按钮.record_pos, self.移动端.resolution, keystr=f"体验服.更新按钮")
        #
        # 更新界面的关闭按钮
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
        # 现在打开可能会放一段视频，这个随意点击也为了让界面换一下
        self.Tool.touch_record_pos(record_pos=(1, 1), resolution=self.移动端.resolution, keystr=f"{fun_name(1)}.屏幕中心")
        sleep(10)
        #
        登录界面开始游戏图标 = Template(r"tpl1692947242096.png", record_pos=(-0.004, 0.158), resolution=(960, 540), threshold=0.9)
        if self.Tool.existsTHENtouch(登录界面开始游戏图标, "登录界面开始游戏图标", savepos=False):
            sleep(waittime)
        if self.Tool.existsTHENtouch(登录界面开始游戏图标, "登录界面开始游戏图标", savepos=False):
            TimeECHO("还存在开始游戏，有可能体验服正在更新")
            return self.run(times)
        #
        # 适合王者活动更改登录界面图标时
        登录界面年龄提示 = Template(r"tpl1729676388436.png", record_pos=(0.382, 0.198), resolution=(960, 540))
        if exists(登录界面年龄提示):
            self.Tool.touch_record_pos(record_pos=登录界面开始游戏图标.record_pos,
                                       resolution=self.移动端.resolution, keystr=f"登录界面开始游戏图标")
            sleep(10)
        #
        # 进入游戏大厅偶尔会有关闭按钮
        self.Tool.LoopTouch(关闭按钮, "关闭按钮", loop=5, savepos=False)
        # 避免点多了, 如果有返回就返回一下
        返回图标 = Template(r"tpl1692949580380.png", record_pos=(-0.458, -0.25), resolution=(960, 540), threshold=0.9)
        self.Tool.LoopTouch(返回图标, "返回图标", loop=3, savepos=False)
        #
        self.大厅元素 = []
        self.大厅元素.append(Template(r"tpl1723551269026.png", record_pos=(0.455, 0.203), resolution=(960, 540)))
        self.大厅元素.append(Template(r"tpl1723551299495.png", record_pos=(-0.461, -0.249), resolution=(960, 540)))
        self.大厅元素.append(Template(r"tpl1723551309461.png", record_pos=(0.354, -0.252), resolution=(960, 540)))
        大厅中, self.大厅元素 = self.Tool.存在任一张图(self.大厅元素, "体验服.大厅元素")
        大厅对战图标 = Template(r"tpl1723219359665.png", record_pos=(-0.122, 0.133), resolution=(960, 540))
        进入5v5匹配 = Template(r"tpl1689666019941.png", record_pos=(0.331, 0.049), resolution=(960, 540))
        if 大厅中:
            return True
        else:
            # 万一大厅更新, 点击进人机界面看看
            if self.Tool.existsTHENtouch(大厅对战图标, "大厅对战", savepos=True):
                if exists(进入5v5匹配):
                    return True
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


def main():
    # 如果使用vscode等IDE运行此脚本
    # 在此处指定config_file=config文件
    config_file = ""
    if len(sys.argv) > 1:
        config_file = str(sys.argv[1])
        if not os.path.exists(config_file):
            TimeECHO(f"不存在{config_file},请检查文件是否存在、文件名是否正确以及yaml.txt等错误拓展名")
            exit()
    Settings.Config(config_file)
    ce = tiyanfu()
    ce.run()
    if ce.内置循环:
        ce.looprun()
    else:
        ce.end()
    exit()


if __name__ == "__main__":
    main()
