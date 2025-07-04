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
# Build  : 2024-07-28            #
# What   : WZYD的礼包         #
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


class wzyd_libao:
    def __init__(self):
        info = """
        营地的领额外战令经验功能也被官方下线了, 
        现在营地的唯一有价值的功能就是用体验币换皮肤碎片了，
        后续营地增加皮肤碎片的礼包，再考虑继续维护wzyd.py
        """
        TimeECHO(info)
        #
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
        dictfile = f"{self.移动端.设备类型}.var_dict_{self.mynode}.wzyd.yaml"
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
        self.prefix = "WZYD"+f".{Settings.mynode}"
        #
        self.设备类型 = self.移动端.设备类型
        self.IOS = "ios" in self.设备类型
        self.APPID = "com.tencent.smoba" if "ios" in self.设备类型 else "com.tencent.gamehelper.smoba"
        self.APPOB = appOB(APPID=self.APPID, big=False, device=self.移动端)
        #
        self.营地初始化FILE = f"{self.prefix}.初始化.txt"
        self.内置循环 = False  # 是否每日循环执行此脚本
        self.营地需要登录FILE = self.prefix+f".需要登录.txt"
        #
        self.timelimit = 60*60*0.5
        # 更新时间
        self.对战时间 = [0.1, 23.9]
        #
        # 默认只创建对象, 开启初始化检查才会检查
        self.体验币成功 = False
        self.营地活动 = True
        #
        # 这两个图标会根据活动变化,可以用下面的注入替换
        self.个人界面图标 = Template(r"tpl1699872206513.png", record_pos=(0.376, 0.724), resolution=(540, 960))
        self.游戏界面图标 = Template(r"tpl1704381547456.png", record_pos=(0.187, 0.726), resolution=(540, 960))
        self.社区界面图标 = Template(r"tpl1717046076553.png", record_pos=(-0.007, 0.759), resolution=(540, 960))
        self.每日福利图标 = Template(r"tpl1699872219891.png", record_pos=(-0.198, -0.026), resolution=(540, 960))
        self.一键领取按钮 = Template(r"tpl1706338731419.png", record_pos=(0.328, -0.365), resolution=(540, 960))
        self.赛事入口 = Template(r"tpl1717046009399.png", record_pos=(-0.269, -0.804), resolution=(540, 960), threshold=0.9, target_pos=6)
        self.资讯入口 = Template(r"tpl1717046009399.png", record_pos=(-0.269, -0.804), resolution=(540, 960), threshold=0.9)
        if self.IOS:
            self.每日福利图标 = Template(r"tpl1700272452555.png", record_pos=(-0.198, -0.002), resolution=(640, 1136))
        self.营地大厅元素 = []
        # 不用添加底部所有的图标, 活动时肯定全部改变, 多添加一些特色的图标
        self.营地大厅元素.append(self.社区界面图标)
        self.营地大厅元素.append(self.赛事入口)

        #
        self.营地登录元素 = []
        self.营地登录元素.append(Template(r"tpl1708393355383.png", record_pos=(-0.004, 0.524), resolution=(540, 960)))
        self.营地登录元素.append(Template(r"tpl1708393749272.png", record_pos=(-0.002, 0.519), resolution=(540, 960)))
        #
        # 测试是否支持pico, 目前仅针对安卓设备开发
        self.pocosupport = False
        if not self.IOS:
            try:
                from poco.drivers.android.uiautomation import AndroidUiautomationPoco
                self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
                """
                # https://developer.aliyun.com/article/1446075
                use_airtest_input=True是指，使用Airtest去执行点击操作，好处是，会在日志里面记录一条log记录，这样生成报告时，就能在报告上显示这个点击记录。
                如果初始化Android poco时，不传入这个参数，默认use_airtest_input=False，则不使用Airtest去执行点击操作，而是调用Android接口去点击，这时候不会在日志里面记录一条点击的log，所以会导致报告里面丢失这个点击步骤。
                所以，如果同学们不在意log内容，或者无需生成测试报告，这个参数可以不传。
                但如果同学们需要生成测试报告，在初始化Android poco时，还是需要把use_airtest_input=True这个参数传上去
                """
                self.pocosupport = True
                TimeECHO("⚠⚠⚠本次运行,将优先采用poco进行识别")
                TimeECHO("若poco模式遇到问题, 请关闭 self.pocosupport = False")
            except ImportError:
                traceback.print_exc()
                self.pocosupport = False
                TimeECHO("若希望开启poco,推荐安装python 3.7环境")
                TimeECHO("运行以下命令安装：")
                TimeECHO("conda create -n air37 python=3.7")
                TimeECHO("conda activate air37")
                TimeECHO("python -m pip install pocoui")
                TimeECHO("python -m pip install airtest_mobileauto")
                TimeECHO("python .\wzyd.py .\config.win.yaml")

        #
        self.初始化成功 = False

    #
    def end(self):
        self.APPOB.关闭APP()
        self.移动端.关闭设备()
    #

    def run(self):
        return self.RUN()
    #
    # poco 相关
    def poco_exit_text(self,strlist):
        # 如果是字符串，转换为单元素列表
        if isinstance(strlist, str):
            strlist = [strlist]
        for istr in strlist:
            if self.poco(text=istr).exists():
                TimeECHO(f"poco: 找到text == {istr}")
                return True
        return False

    def poco_exit_id(self,strlist):
        # 如果是字符串，转换为单元素列表
        if isinstance(strlist, str):
            strlist = [strlist]
        for istr in strlist:
            if self.poco(istr).exists():
                TimeECHO(f"poco: 找到id == {istr}")
                return True
        return False        
    
    def poco_exit_text_then_touch(self,strlist):
        # 如果是字符串，转换为单元素列表
        if isinstance(strlist, str):
            strlist = [strlist]
        for istr in strlist:
            if self.poco(text=istr).exists():
                self.poco(text=istr).click()
                TimeECHO(f"poco: touch(text == {istr})")
                sleep(0.1)
                return True
        return False
    
    def poco_exit_id_then_touch(self,strlist):
        # 如果是字符串，转换为单元素列表
        if isinstance(strlist, str):
            strlist = [strlist]
        for istr in strlist:
            if self.poco(istr).exists():
                self.poco(istr).click()
                TimeECHO(f"poco: touch({istr})")
                sleep(0.1)
                return True
        return False
    
    def 判断营地大厅中(self):
        #
        if self.pocosupport:
            return self.poco_exit_text(["首页"])
        #
        # 不用添加底部所有的图标, 活动时肯定全部改变
        self.营地大厅元素.append(self.社区界面图标)
        self.营地大厅元素.append(self.赛事入口)
        存在, self.营地大厅元素 = self.Tool.存在任一张图(self.营地大厅元素, "营地大厅元素")
        return 存在
    #

    def 判断营地登录中(self):
        #
        if self.pocosupport:
            return self.poco_exit_text(["com.tencent.gamehelper.smoba:id/sv_license","com.tencent.gamehelper.smoba:id/tv_reject","com.tencent.gamehelper.smoba:id/tv_agree","获取验证码"])
        #
        存在, self.营地登录元素 = self.Tool.存在任一张图(self.营地登录元素, "营地登录元素")
        return 存在
    #
    #
    # 用于更新上层调用参数,是不是领取礼包

    def 营地初始化(self, 初始化检查=False):
        #
        if not self.APPOB.HaveAPP:
            TimeECHO(f":不存在APP{self.APPOB.APPID}")
            return False
        #
        self.礼包功能_营地币换碎片 = True
        self.礼包功能_体验币换碎片 = False
        run_class_command(self=self, command=self.Tool.readfile(self.营地初始化FILE))
        #
        # 判断网络情况
        if not connect_status():
            TimeECHO(":营地暂时无法触摸,返回")
            if 初始化检查:
                return True
            return False
        #
        # 打开APP
        if not self.APPOB.前台APP(2):
            TimeECHO(":营地无法打开,返回")
            self.APPOB.关闭APP()
            if 初始化检查:
                return True
            return False
        sleep(20)  # 等待营地打开
        #
        # 这里很容易出问题，主页的图标变来变去
        # MuMu 模拟器营地居然也闪退
        if not self.判断营地大厅中():
            TimeECHO(":营地未知原因没能进入大厅,再次尝试")
            self.APPOB.关闭APP()
            if not self.APPOB.前台APP(2):
                TimeECHO(":营地无法打开,返回")
                self.APPOB.关闭APP()
                if 初始化检查:
                    return True
                return False
            #
            # 说明可以启动, 此时没有登录元素就算是成功了吧
            if self.判断营地登录中():
                TimeECHO(":检测到营地登录界面,不领取礼包")
                self.Tool.touchfile(self.营地需要登录FILE)
                self.APPOB.关闭APP()
                return False

        # 前面的都通过了,判断成功
        if 初始化检查:
            self.Tool.removefile(self.营地需要登录FILE)
            self.Tool.removefile("重新登录营地战令.txt")
            self.初始化成功 = True
        #
        return True

    def STOP(self):
        self.APPOB.关闭APP()
        sleep(5)

    def RUN(self):
        #
        # 修正分辨率, 避免某些模拟器返回的分辨率不对
        if self.移动端.resolution[0] > self.移动端.resolution[1]:
            TimeECHO("=>"*20)
            TimeECHO(f"⚠️ 警告: 分辨率 ({ self.移动端.resolution}) 不符合 (宽, 高) 格式，正在修正...")
            self.移动端.resolution = (min(self.移动端.resolution), max(self.移动端.resolution))
            TimeECHO("<="*20)
        #
        if not self.APPOB.HaveAPP:
            TimeECHO(f":不存在APP{self.APPOB.APPID}")
            return False
        #
        if not self.初始化成功:
            self.初始化成功 = self.营地初始化(初始化检查=True)
            if not self.初始化成功:
                TimeECHO("营地初始化失败")
                self.APPOB.关闭APP()
                return False

        self.Tool.removefile(self.Tool.独立同步文件)
        #
        if os.path.exists(self.营地需要登录FILE):
            if self.Tool.timelimit(timekey="检测营地登录", limit=60*60*8, init=False):
                TimeECHO(f"存在[{self.营地需要登录FILE}],重新检测登录状态")
                self.Tool.removefile(self.营地需要登录FILE)
                self.初始化成功 = self.营地初始化(初始化检查=True)
        #
        if os.path.exists(self.营地需要登录FILE):
            TimeECHO(f"检测到{self.营地需要登录FILE}, 不领取礼包")
            return False
        #
        self.营地任务_浏览资讯()
        self.营地任务_观看赛事()
        self.营地任务_圈子签到()
        #
        # 体验服只有安卓客户端可以领取
        if not self.IOS and self.礼包功能_体验币换碎片:
            self.体验服礼物()
        self.每日签到任务()
        if self.礼包功能_营地币换碎片:
            self.营地币兑换碎片()
        self.营地战令经验()
        self.APPOB.关闭APP()
        return True

    def 营地任务_观看赛事(self, times=1):
        #
        if self.Tool.存在同步文件():
            return True
        #
        keystr = "营地任务_观看赛事"
        if times == 1:
            self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=True)
        else:
            if self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=False):
                TimeECHO(f"{keystr}{times}超时退出")
                return False
        #
        TimeECHO(f"{keystr}{times}")
        self.APPOB.重启APP(10)
        sleep(10)
        times = times+1
        if times % 4 == 3:
            if not connect_status():
                self.Tool.touch同步文件(self.Tool.独立同步文件)
                return False
        if times > 10:
            return False
        #
        if not self.APPOB.前台APP(2):
            return self.营地任务_观看赛事(times)
        #
        # 都保存位置,最后进不去再return
        self.Tool.existsTHENtouch(self.赛事入口, "赛事入口", savepos=True)
        去直播间 = Template(r"tpl1717046024359.png", record_pos=(0.033, 0.119), resolution=(540, 960))
        for i in range(5):
            if self.Tool.existsTHENtouch(去直播间, "去直播间图标"):
                sleep(120)
                return True
            if self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=False):
                TimeECHO(f"{keystr}{times}超时退出")
                return False
        TimeECHO(f"没进入直播间")
        return self.营地任务_观看赛事(times)

    def 营地任务_圈子签到(self, times=1):
        #
        if self.Tool.存在同步文件():
            return True
        #
        keystr = "营地任务_圈子签到"
        if times == 1:
            self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=True)
        else:
            if self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=False):
                TimeECHO(f"{keystr}{times}超时退出")
                return False
        #
        TimeECHO(f"{keystr}{times}")
        self.APPOB.重启APP(10)
        sleep(10)
        times = times+1
        if times % 4 == 3:
            if not connect_status():
                self.Tool.touch同步文件(self.Tool.独立同步文件)
                return False
        if times > 10:
            return False
        #
        if not self.APPOB.前台APP(2):
            return self.营地任务_圈子签到(times)
        #
        # 都保存位置,最后进不去再return
        self.Tool.existsTHENtouch(self.社区界面图标, "社区界面图标", savepos=True)
        sleep(10)
        #
        圈子图标 = Template(r"tpl1717047527808.png", record_pos=(-0.254, -0.809), resolution=(540, 960))
        if not self.Tool.existsTHENtouch(圈子图标, "圈子图标", savepos=True):
            TimeECHO(f"找不到圈子图标")
            return self.营地任务_圈子签到(times)
        #
        # 需要提前自己加入一些圈子
        营地圈子 = []
        营地圈子.append(Template(r"tpl1717046264179.png", record_pos=(-0.178, -0.511), resolution=(540, 960)))
        营地圈子.append(Template(r"tpl1724585182506.png", record_pos=(0.02, -0.474), resolution=(540, 960)))
        营地圈子.append(Template(r"tpl1724585186597.png", record_pos=(0.22, -0.476), resolution=(540, 960)))
        进入小组 = False
        for i in range(5):
            进入小组 = self.Tool.existsTHENtouch(营地圈子[0], "营地.营地圈子", savepos=False)
            if not 进入小组:
                存在, 营地圈子 = self.Tool.存在任一张图(营地圈子, "营地.营地圈子", savepos=True)
                if 存在:
                    进入小组 = self.Tool.existsTHENtouch(营地圈子[0], "营地.营地圈子", savepos=True)
            #
            sleep(6)
            if 进入小组:
                break
        #
        if not 进入小组:
            TimeECHO(f"请加入以下圈子之一: 王者问答圈|皮肤交流圈|峡谷互助小组")
            TimeECHO(f"如果仍无法找到圈子，可能是营地版本不同，需要修改: 营地圈子.append()")
            return self.营地任务_圈子签到(times)
        圈子签到图标 = Template(r"tpl1717046286604.png", record_pos=(0.393, -0.3), resolution=(540, 960))
        签到成功图标 = Template(r"tpl1717047898461.png", record_pos=(-0.004, 0.237), resolution=(540, 960))
        if self.Tool.existsTHENtouch(圈子签到图标, "圈子签到图标"):
            if self.Tool.existsTHENtouch(签到成功图标, "签到成功图标"):
                TimeECHO(f"签到成功")
        else:
            TimeECHO(f"可能签到过了")
        return True

    def 营地任务_浏览资讯(self, times=1):
        #
        if self.Tool.存在同步文件():
            return True
        #
        keystr = "营地任务_浏览资讯"
        if times == 1:
            self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=True)
        else:
            if self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=False):
                TimeECHO(f"{keystr}{times}超时退出")
                return False
        #
        if not self.APPOB.前台APP(2):
            return self.营地任务_浏览资讯(times)
        #
        TimeECHO(f"{keystr}{times}")
        self.APPOB.重启APP(10)
        sleep(10)
        times = times+1
        if times % 4 == 3:
            if not connect_status():
                self.Tool.touch同步文件(self.Tool.独立同步文件)
                return False
        if times > 10:
            return False
        #
        if self.pocosupport:
            if not self.poco_exit_text_then_touch(["首页"]):
                return self.营地任务_浏览资讯(times)
            #
            if not self.poco_exit_text_then_touch(["推荐"]):
                return self.营地任务_浏览资讯(times)
        else:
            self.Tool.existsTHENtouch(self.资讯入口, "资讯入口.推荐", savepos=True)
        #
        # 
        if self.pocosupport:
            pass
            # 暂时没找到从poco进行咨询页面的功能，强制点击特定位置是可以行的
            # 暂时保留下面的图片识别，或者固定位置点击
        资讯入口图标 = []
        资讯入口图标.append(Template(r"tpl1724584561119.png", record_pos=(-0.419, -0.433), resolution=(540, 960)))
        资讯入口图标.append(Template(r"tpl1724681918901.png", record_pos=(-0.115, -0.213), resolution=(540, 960)))
        if "资讯入口图标" not in self.Tool.var_dict.keys():
            # savepos 如果找到会自动替换上一次的字典
            存在, 资讯入口图标 = self.Tool.存在任一张图(资讯入口图标, "资讯入口图标", savepos=True)
            if not 存在:
                TimeECHO(f"WZYD: 资讯入口图标")
                TimeECHO(f"按照960x540的分辨率强制设定坐标")
                # 这里是绝对坐标，不适用于其他分辨率的情况
                self.Tool.var_dict["资讯入口图标"] = (250, 650)
        #
        self.Tool.existsTHENtouch(资讯入口图标[0], "资讯入口图标", savepos=True)
        #
        #
        if self.pocosupport:
            self.poco_exit_id_then_touch(['com.tencent.gamehelper.smoba:id/img_like'])
            # 转发到动态
            if self.poco_exit_id_then_touch(["com.tencent.gamehelper.smoba:id/img_share"]):
                self.poco_exit_text_then_touch(["转发到动态"])
                self.poco_exit_id_then_touch(['com.tencent.gamehelper.smoba:id/publish'])
        # 下面是评论区的点赞
        点赞图标 = []
        点赞图标.append(Template(r"tpl1717046512030.png", record_pos=(0.424, 0.02), resolution=(540, 960)))
        点赞图标.append(Template(r"tpl1724681888775.png", record_pos=(0.417, -0.243), resolution=(540, 960)))
        评论区 = Template(r"tpl1723599264627.png", record_pos=(0.115, 0.717), resolution=(540, 960))
        资讯页面元素 = [评论区]
        for i in 点赞图标:
            资讯页面元素.append(i)
        存在, 资讯页面元素 = self.Tool.存在任一张图(资讯页面元素, "营地.资讯页面元素")
        if not 存在:
            if times % 4 == 3 and "资讯入口图标" in self.Tool.var_dict.keys():
                del self.Tool.var_dict["资讯入口图标"]
            return self.营地任务_浏览资讯(times)
        # 开始滑动点赞
        pos = self.Tool.var_dict["资讯入口图标"]
        for i in range(180):
            sleep(1)
            存在, 点赞图标 = self.Tool.存在任一张图(点赞图标, "营地.点赞图标", savepos=True)
            if 存在:
                self.Tool.existsTHENtouch(点赞图标[0], "营地.点赞图标", savepos=True)
                sleep(0.5)
                if i % 15 == 0:
                    swipe(pos, vector=[0.0, 0.5])
                    self.Tool.existsTHENtouch(评论区, "评论区图标", savepos=False)
            else:
                sleep(1)
                if i % 15 == 0:
                    self.Tool.existsTHENtouch(评论区, "评论区图标", savepos=False)
            TimeECHO(f"浏览资讯中{i}")
            swipe(pos, vector=[0.0, -0.5])
            if self.Tool.timelimit(timekey=f"{keystr}", limit=60*5, init=False):
                TimeECHO(f"浏览资讯时间到")
                return
        return

    def 营地战令经验(self, times=0):
        #
        TimeECHO(f"营地战令经验/营地战令任务于2025-04-01被官方下架, return")
        return True
        #
        # 第一次，需要手动点击一下，开启战令
        if self.Tool.存在同步文件():
            return True
        #
        if times == 0:
            self.Tool.timelimit(timekey="营地战令经验", limit=60*5, init=True)
        else:
            if self.Tool.timelimit(timekey="营地战令经验", limit=60*5, init=False):
                TimeECHO(f"营地战令经验{times}超时退出")
                return False
        #
        times = times+1
        TimeECHO(f"营地战令经验{times}")
        self.APPOB.重启APP(10)
        sleep(10)
        if times % 4 == 3:
            if not connect_status():
                self.Tool.touch同步文件(self.Tool.独立同步文件)
                return False
        if times > 10:
            return False
        #
        if not self.APPOB.前台APP(2):
            return self.营地战令经验(times)
        #
        #
        if self.pocosupport:
            if not self.poco_exit_text_then_touch(["游戏"]):
                return self.营地战令经验(times)
        else:
            # 都保存位置,最后进不去再return
            self.Tool.existsTHENtouch(self.游戏界面图标, "游戏界面图标", savepos=True)
        sleep(5)
        # 
        if self.pocosupport:
            pass
            # 暂时没找到从poco进入营地和点击
        #
        正式服判断图标 = Template(r"tpl1715609808723.png", record_pos=(-0.217, -0.044), resolution=(540, 960))
        正式服大头图标 = Template(r"tpl1715610763289.png", record_pos=(-0.281, -0.8), resolution=(540, 960))
        正式服入口 = False
        for i in range(5):
            if exists(正式服判断图标):
                正式服入口 = True
                break
            # 不同的账号，显示的数目不一样多，没办法savepos
            self.Tool.existsTHENtouch(正式服大头图标, "正式服大头图标", savepos=False)
        if not 正式服入口:
            TimeECHO(f"没有找到正式服入口,有可能营地有更新")
            return self.营地战令经验(times)
        # 点开工具箱
        self.Tool.existsTHENtouch(正式服判断图标, "正式服工具图标", savepos=True)
        sleep(10)
        战令入口 = Template(r"tpl1715609828196.png", record_pos=(0.209, -0.004), resolution=(540, 960))
        self.Tool.existsTHENtouch(战令入口, "战令入口", savepos=True)
        sleep(10)
        重新登录 = Template(r"tpl1724463208462.png", record_pos=(0.0, -0.035), resolution=(540, 960))
        if self.Tool.existsTHENtouch(重新登录, "重新登录"):
            self.Tool.touchfile("重新登录营地战令.txt")
            return
        # 
        战令任务 = []
        战令任务.append(Template(r"tpl1715609874404.png", record_pos=(-0.25, -0.706), resolution=(540, 960)))
        战令任务.append(Template(r"tpl1724905564530.png", record_pos=(-0.23, -0.694), resolution=(540, 960)))
        战令页面元素 = []
        战令页面元素.append(Template(r"tpl1715609862801.png", record_pos=(0.131, 0.743), resolution=(540, 960)))
        战令页面元素.append(Template(r"tpl1716804327622.png", record_pos=(0.0, 0.156), resolution=(540, 960)))
        战令页面元素.append(Template(r"tpl1716804333697.png", record_pos=(0.352, 0.739), resolution=(540, 960)))
        for i in 战令任务:
            战令页面元素.append(i)
        #
        存在, 战令页面元素 = self.Tool.存在任一张图(战令页面元素, "营地.战令页面元素")
        # 如果3次都没找到，就不管了，强制点下去
        if not 存在 and times < 4:
            sleep(20)
            存在, 战令页面元素 = self.Tool.存在任一张图(战令页面元素, "营地.战令页面元素")
            if not 存在:
                TimeECHO(f"没找到战令页面")
                return self.营地战令经验(times)

        if "营地.战令任务" not in self.Tool.var_dict.keys():
            存在, 战令任务 = self.Tool.存在任一张图(战令任务, "营地.战令任务", savepos=True)
            if not 存在:
                TimeECHO(f"没找到战令任务页面,按照960x540的分辨率强制点击战令任务")
                # 这里是绝对坐标，不适用于其他分辨率的情况
                self.Tool.var_dict["营地.战令任务"] = (148, 108)
        self.Tool.existsTHENtouch(战令任务[0], "营地.战令任务", savepos=True)
        sleep(10)
        一键领取 = Template(r"tpl1715610610922.png", record_pos=(0.337, -0.18), resolution=(540, 960))
        self.Tool.existsTHENtouch(一键领取, "一键领取战令经验", savepos=True)
        sleep(5)
        pos = exists(一键领取)
        if pos:
            TimeECHO("仍检测到一键领取战令经验，更新坐标中")
            self.Tool.var_dict["一键领取战令经验"] = pos
            self.Tool.existsTHENtouch(一键领取, "一键领取战令经验", savepos=True)
            sleep(10)

    def 体验服礼物(self, times=1):
        #
        """
        停更
        """
        if self.Tool.存在同步文件():
            return True
        #
        if times == 1:
            self.Tool.timelimit(timekey="体验服礼物", limit=60*5, init=True)
        else:
            if self.Tool.timelimit(timekey="体验服礼物", limit=60*5, init=False):
                TimeECHO(f"体验服礼物{times}超时退出")
                return False
        #
        TimeECHO(f"体验币{times}")
        self.APPOB.重启APP(10)
        sleep(10)
        times = times+1
        if times % 4 == 3:
            if not connect_status():
                self.Tool.touch同步文件(self.Tool.独立同步文件)
                return False
        if times > 10:
            return False
        #
        if not self.APPOB.前台APP(2):
            return self.体验服礼物(times)
        #
        #
        if self.pocosupport:
            if not self.poco_exit_text_then_touch(["游戏"]):
                return self.营地战令经验(times)
        else:
            # 都保存位置,最后进不去再return
            self.Tool.existsTHENtouch(self.游戏界面图标, "游戏界面图标", savepos=True)
        sleep(5)
        # 判断是否在体验服框架
        # 这里需要提前手动把体验服加到选择界面
        体验服判断图标 = Template(r"tpl1704381586249.png", record_pos=(-0.293, -0.026), resolution=(540, 960))
        体验服大头图标 = Template(r"tpl1704381887267.png", record_pos=(-0.42, -0.787), resolution=(540, 960))
        体验服入口 = False
        for i in range(5):
            if exists(体验服判断图标):
                体验服入口 = True
                break
            # 不同的账号，显示的数目不一样多，没办法savepos
            self.Tool.existsTHENtouch(体验服大头图标, "体验服大头图标", savepos=False)
        if not 体验服入口:
            TimeECHO(f"没有找到体验服入口,有可能营地有更新")
            return self.体验服礼物(times)
        #
        奖励兑换图标 = Template(r"tpl1704381904053.png", record_pos=(-0.209, -0.026), resolution=(540, 960))
        self.Tool.existsTHENtouch(奖励兑换图标, "体验服奖励兑换图标", savepos=True)
        sleep(5)
        正在进入 = Template(r"tpl1725004412475.png", record_pos=(-0.004, -0.776), resolution=(540, 960))
        奖励兑换网页图标 = Template(r"tpl1704381965060.png", rgb=True, target_pos=7, record_pos=(0.243, -0.496), resolution=(540, 960))
        for i in range(10):
            if exists(正在进入):
                TimeECHO("正在进入体验服中....")
                sleep(6*1.5)  # 1.5分钟
            else:
                sleep(5)
            #
            if self.pocosupport:
                if self.poco_exit_text(["奖励兑换"]):
                    break
            elif exists(奖励兑换网页图标):
                break
        if self.pocosupport:
            if not self.poco_exit_text_then_touch(["奖励兑换"]):
                sleep(20)
                if not self.poco_exit_text_then_touch(["奖励兑换"]):
                    return self.体验服礼物(times)
        elif not self.Tool.existsTHENtouch(奖励兑换网页图标, "奖励兑换网页图标", savepos=False):
            sleep(20)
            if not self.Tool.existsTHENtouch(奖励兑换网页图标, "奖励兑换网页图标", savepos=False):
                return self.体验服礼物(times)
        #
        # 
        if self.pocosupport:
            pass
            # 下面的不好弄
        
        # 有时候会让重新登录
        重新登录 = Template(r"tpl1702610976931.png", record_pos=(0.0, 0.033), resolution=(540, 960))
        if self.Tool.existsTHENtouch(重新登录, "重新登录"):
            self.Tool.touchfile("重新登录体验服.txt")
            return
        奖励页面 = Template(r"tpl1704522893096.png", record_pos=(0.239, 0.317), resolution=(540, 960))
        pos = False
        # 这里是等待刷新的过程,不用sleep那么久
        for i in range(10):
            sleep(5)
            pos = exists(奖励页面)
            if pos:
                break
            else:
                TimeECHO(f"寻找奖励兑换页面中{i}")

        if not pos:
            TimeECHO(":没进入奖励兑换页面")
            return self.体验服礼物(times)
        #
        swipe(pos, vector=[0.0, -0.5])
        碎片奖励 = Template(r"tpl1699874679212.png", record_pos=(-0.233, 0.172), resolution=(540, 960), threshold=0.9)
        奖励位置 = False
        for i in range(20):
            sleep(1)
            奖励位置 = exists(碎片奖励)
            if 奖励位置:
                break
            else:
                TimeECHO(f"寻找碎片奖励中{i}")
            swipe(pos, vector=[0.0, -0.5])
        if not 奖励位置:
            TimeECHO("没找到体验币")
            return self.体验服礼物(times)
        #
        touch(奖励位置)
        成功领取 = Template(r"tpl1699874950410.png", record_pos=(-0.002, -0.006), resolution=(540, 960))
        if exists(成功领取):
            TimeECHO(":成功领取")
        else:
            TimeECHO(":领取过了/体验币不够")
        return
        #

    def 每日签到任务(self, times=1):
        TimeECHO(f"营地每日签到{times}")
        #
        if self.Tool.存在同步文件():
            return True
        #
        if times == 1:
            self.Tool.timelimit(timekey="营地每日签到", limit=60*5, init=True)
        else:
            if self.Tool.timelimit(timekey="营地每日签到", limit=60*5, init=False):
                TimeECHO(f"营地每日签到{times}超时退出")
                return False
        #
        times = times+1
        if times % 4 == 3:
            if not connect_status():
                self.Tool.touch同步文件(self.Tool.独立同步文件)
                return False
        if times > 5:
            return False
        #
        if not self.APPOB.前台APP(2):
            return self.每日签到任务(times)
        #
        # 每日签到
        self.APPOB.重启APP(10)
        #
        if self.pocosupport:
            self.poco_exit_text_then_touch(["我"])
        else:
            self.Tool.existsTHENtouch(self.个人界面图标, "WZYD个人界面", savepos=True)
        sleep(10)
        #
        if self.pocosupport:
            if not self.poco_exit_text_then_touch(["每日福利"]):
                return self.每日签到任务(times)
        elif not self.Tool.existsTHENtouch(self.每日福利图标, "WZYD每日福利", savepos=False):
            return self.每日签到任务(times)
        #
        #
        if self.pocosupport:
            pass        
        sleep(5)
        self.Tool.existsTHENtouch(self.一键领取按钮, "一键领取按钮")
        # 新款签到入口
        #
        签到入口 = Template(r"tpl1706339365291.png", target_pos=6, record_pos=(-0.011, -0.185), resolution=(540, 960))
        签到按钮 = Template(r"tpl1706339420536.png", record_pos=(0.106, -0.128), resolution=(540, 960))
        if self.Tool.existsTHENtouch(签到入口, "营地签到入口"):
            sleep(10)
            if self.Tool.existsTHENtouch(签到按钮, "营地签到按钮"):
                return self.每日签到任务(times)
            # 签到后也有礼物,在后面的营地币兑换碎片可以领到
        #
        return True

    def 营地币兑换碎片(self, times=1):
        """
        20250627 停止维护
        """
        TimeECHO(f"营地币兑换碎片{times}")
        TimeECHO(f"20250627 停止维护")
        #
        if self.Tool.存在同步文件():
            return True
        #
        if times == 1:
            self.Tool.timelimit(timekey="营地币兑换碎片", limit=60*5, init=True)
        else:
            if self.Tool.timelimit(timekey="营地币兑换碎片", limit=60*5, init=False):
                TimeECHO(f"营地币兑换碎片{times}超时退出")
                return False
        #
        times = times+1
        if times % 4 == 3:
            if not connect_status():
                self.Tool.touch同步文件(self.Tool.独立同步文件)
                return False
        if times > 10:
            return False
        self.APPOB.重启APP(10)
        #
        if not self.APPOB.前台APP(2):
            return self.营地币兑换碎片(times)
        #
        #
        if self.pocosupport:
            if not self.poco_exit_text_then_touch(["每日福利"]):
                return self.每日签到任务(times)
        elif not self.Tool.existsTHENtouch(self.每日福利图标, "WZYD每日福利", savepos=False):
            return self.每日签到任务(times)
        sleep(5)
        #
        #
        if self.pocosupport:
            pass
        self.Tool.existsTHENtouch(self.一键领取按钮, "一键领取按钮")
        # 老款营地币兑换
        if not self.Tool.existsTHENtouch(Template(r"tpl1706338003287.png", record_pos=(0.389, 0.524), resolution=(540, 960)), "营地币兑换"):
            return self.营地币兑换碎片(times)
        兑换页面 = Template(r"tpl1699873075417.png", record_pos=(0.437, 0.167), resolution=(540, 960))
        pos = False
        for i in range(10):
            sleep(5)
            pos = exists(兑换页面)
            if pos:
                break
            else:
                TimeECHO(f":寻找兑换页面中{i}")
        if not pos:
            TimeECHO(":没进入营地币兑换页面")
            return self.营地币兑换碎片(times)
        swipe(pos, vector=[0.0, -0.5])
        碎片奖励 = Template(r"tpl1699873407201.png", record_pos=(0.009, 0.667), resolution=(540, 960))
        奖励位置 = False
        for i in range(5):
            sleep(1)
            奖励位置 = exists(碎片奖励)
            if 奖励位置:
                break
            else:
                TimeECHO(f"寻找营地币换碎片中{i}")
            swipe(pos, vector=[0.0, -0.5])
        if not 奖励位置:
            TimeECHO(":没找到营地币")
            return self.营地币兑换碎片(times)
        touch(奖励位置)
        #
        确定兑换 = Template(r"tpl1699873472386.png", record_pos=(0.163, 0.107), resolution=(540, 960))
        if not self.Tool.existsTHENtouch(确定兑换):
            self.Tool.touch_record_pos(确定兑换.record_pos, self.移动端.resolution, f"确定兑换")
        #
        再次确定兑换 = Template(r"tpl1733194097335.png", record_pos=(0.007, 0.748), resolution=(540, 960))
        if not self.Tool.existsTHENtouch(再次确定兑换):
            self.Tool.touch_record_pos(再次确定兑换.record_pos, self.移动端.resolution, f"再次确定兑换")
        #
        self.Tool.existsTHENtouch(Template(r"tpl1699873480797.png", record_pos=(0.163, 0.104), resolution=(540, 960)))

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
    ce = wzyd_libao()
    ce.run()
    if ce.内置循环:
        ce.looprun()
    else:
        ce.end()
    exit()


if __name__ == "__main__":
    main()
