## 吉林大学研究生每日打卡
负责定时体温&签到打卡+微信消息推送
## 使用说明
使用Python 3，使用前确保第三方包requests、selenium已经安装  
脚本提供显式&隐式打卡，**`第一次使用务必显示运行，确保信息准确，之后可选择隐式运行。`**  
请参考主函数配置个人信息，**`因为没有正确配置造成的一切后果与程序作者无关。`**  
## 需要做的事情
* 配置chrome浏览器驱动（配置后可能需要重启）
  *  下载chrome driver, 将chrome diver放置在chrome浏览器安装文件夹下。参考[selenium 安装与 chromedriver安装](https://www.cnblogs.com/lfri/p/10542797.html)
  *  确定chrome 安装位置, 复制至代码主函数（例如：C:\Program Files (x86)\Google\Chrome\Application）
* 配置个人信息
  * 个人信息参考 config文件
* **（可选）** 微信消息提醒（请使用个人微信绑定的SCKEY）
  * server网址http://sc.ftqq.com/3.version
