# batch-healer
> 全称：Batch Health-Checker  
> 直译：批量治愈者（迫真） 
 
对您的鸡厂进行直观的健康检查
## 说明
> 众所周知的原因（网课啊啊啊），我的时间变少了，开发将会有大幅度滞后
## Features 
目前暂只支持`vmess`协议，兼容`shadowsocks`这个大家族要大改动  
+ 从`vmess://`链接或`订阅链接`中读取服务器列表
+ 支持`vmess://`与`订阅链接`混用
+ 自动以周期的方式轮询检查
+ 从TCP、HTTPS、DNS等方面进行判断节点可用性（ICMP被否定了
+ 在周期等待时间按下`Ctrl+C`可直观反馈结果
## Usage
1. `$ git clone https://github.com/ctuin/batch-healer`，也可以下载后解压
2. 在程序的同级目录下新建`v2ray-urls.txt`，并在其中写入URL，例如
    ```text
    vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIui/meWPquaYr+ekuuS+i+iAjOW3siIsDQogICJhZGQiOiAibG9jYWxob3N0IiwNCiAgInBvcnQiOiAiNDQzIiwNCiAgImlkIjogIjI2MmVhNDdlLWRkNzEtNDgyNC04NGU3LTMwM2U1YTllZWI0YSIsDQogICJhaWQiOiAiNjQiLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogImxvY2FsaG9zdCIsDQogICJwYXRoIjogIi8iLA0KICAidGxzIjogInRscyINCn0=
    https://example.com/path/
    ```
3. 根据情况修改`settings.py`中的内容
4. `$ python3 main.py`愉快地运行吧！（screen中运行体验更佳
> Docker版将会择机发布，取决于学习压力
## Demo
什么？
`D`
`E`
`M`
`O`是什么玩意？我不是我没有我不会
> 不存在的，真的没有
## Copyright
此代码仅用于学习&交流使用，不得作他用！
此仓库基于`GNU General Public License v3.0`
随意修改或不正当使用，产生的后果作者不负责任！