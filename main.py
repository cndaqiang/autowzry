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
#
#
# 源代码可以从[开源仓库的dev分支](https://github.com/cndaqiang/autowzry/tree/dev)下载.
#
#

INFO="""
# **Python 环境安装方法**

* 若你不了解Python, 请使用独立包运行.
* 作为开发者，你应该可以访问[**视频教程**](https://youtu.be/Uj2NE6XjYSc)
* **项目的持续发展需要你为 [autowzry 项目点个 star⭐](https://github.com/cndaqiang/autowzry)**


## 安装模拟器和登陆游戏

## 配置环境
* 安装 Python, **推荐使用python 3.7 ~ 3.12 版本**
* 安装依赖`airtest_mobileauto`

```
python -m pip install airtest_mobileauto --upgrade
```

## 运行源码

下载

* 源代码可以从[开源仓库的dev分支](https://github.com/cndaqiang/autowzry/tree/dev)下载.
* **为防止他人删除版权信息后倒卖软件，开源仓库的更新将滞后一个赛季以上**。
* 公开源代码仅供研究与学习用途，具备 Python 经验的开发者可基于开源版本自行适配。

运行

* 当模拟器的ADB地址是`127.0.0.1:5555`时(比如雷电模拟器、新版MuMu等), 可以直接执行脚本`python -u wzry.py`
* **若运行脚本后无法连接模拟器，或有组队需求，请参考[配置文件](config.md)修改自动生成的配置文件`config.example.yaml`**
* 然后采用配置文件运行`python -u wzry.py config.example.yaml`
"""


print(INFO)