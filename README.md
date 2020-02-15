# batch-healer
全称：Batch Health-Checker  
直译：批量治愈者（迫真）  
# Features 
+ 从`vmess://`链接或订阅链接中读取服务器列表
+ 自动检测是`vmess://`链接还是订阅链接
+ 支持多台服务器
+ 自动以周期的方式轮询检查
> 一个周期后延迟一段时间，进入下一个周期
+ 从TCP、HTTPS、DNS等方面进行判断节点可用性
+ 没写完