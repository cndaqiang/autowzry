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


try:
    from setuptools import setup, find_packages
except:
    print("注意本脚本是用于打包autowzry项目, 发布到pypi")
    print("若是运行演示代码, 请根据手册运行wzry.py")

setup(
    name='autowzry',
    version='2.4.1.1',
    # 版本号后缀说明：
    # - a1：早期测试版（Alpha 版本）
    # - b1：功能较完整但可能有问题的测试版（Beta 版本）
    # - rc1：接近最终稳定版的发布候选版本（Release Candidate）
    # - dev1：开发中版本（未完成，内部测试）
    # - post1：正式版发布后的补丁版本
    # 示例：'2.3.0a1' 表示 2.3.0 的第 1 个 Alpha 测试版
    author='cndaqiang',
    author_email='who@cndaqiang.ac.cn',
    description='自动化农活演示',
    long_description=open('README.md', encoding='utf-8').read(),  # 从 autowzry/README.md 读取 long description
    long_description_content_type='text/markdown',
    packages=find_packages(),  # 自动查找所有子包
    # 需要在autowzry下面创建__init__.[y]
    package_data={             # 指定需要包含的额外文件
        'autowzry': [
            'assets/*',         # 包括 autowzry/assets 下的所有文件
        ],
    },
    include_package_data=True,  # 自动包含 package_data 中指定的文件
    url='https://github.com/cndaqiang/autowzry',
    install_requires=[
        'airtest-mobileauto>=2.1.8.1',
        # 'autoansign>=1.2',
    ],
    entry_points={
        'console_scripts': [
            'autowzyd=autowzry.wzyd:main',  # 直接引用脚本文件
            'autowzry=autowzry.wzry:main',  # 直接引用脚本文件
            'autotiyanfu=autowzry.tiyanfu:main',  # 直接引用脚本文件
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
