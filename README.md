## 介绍
1. 一款基于Python-Flask框架,开发的Hyper-V网页端管理程序.
## 功能
1. 具有管理和用户两大页面.
2. 管理可查看基本状况,修改登录密码,管理虚拟机,用户,网站.
3. 用户可修改登录密码,管理虚拟机.
## 需求
1. 环境: Python3.
2. 包: 见requirement.txt文件.
3. 管理员权限运行.
## 配置(data/core.json)
port的值代表端口号.
## 管理
1. 目前只有一个管理,用户名只能填写admin,登录默认密码为12345678.
2. 可在仪表盘中查看基本状况,修改密码.
3. 对虚拟机进行开机,重启,关机,强制关机,应用检查点,备注,分配给指定用户,设置到期日期.
4. 可查看用户列表,添加用户,修改密码,删除.
5. 对网站设置标题,关键词,描述,公告.
## 用户
1. 可在仪表盘中查看基本状况,修改密码.
2. 对虚拟机进行开机,重启,关机,强制关机,应用检查点,备注.