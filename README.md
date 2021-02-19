# DouYu-Push

<p align="center">
<img src="https://img.shields.io/badge/python-3.x-blue">
<img src="https://img.shields.io/github/license/Virace/douyu-push?color=%234c1&style=flat-square">
</p>



斗鱼直播间直播推送, 专治随缘主播(🐶)


- [介绍](#介绍)
- [目录](#目录)
- [安装](#安装)
- [部署](#部署)
- [维护者](#维护者)
- [感谢](#感谢)
- [许可证](#许可证)


### 介绍
- 已完成的功能
  - 查询直播间直播状态
  - Push+ 微信推送
  - 酷推 QQ机器人推送

    
- 待解决的问题
    - 推送可靠性问题

### 目录
```
├  index.py
│  database.py
│  push.py
│  requirements.txt
```

### 安装

**要求:**
- 直接克隆本库
- leancloud创建应用, 并获取appid、appkey和数据行id
  ![](https://tva1.sinaimg.cn/large/008aYkguly1gnt4j0xp6dj31n315vn4o.jpg)
  ![](https://tva1.sinaimg.cn/large/008aYkguly1gnt4j0wu5sj323s0ysgr1.jpg)
  
- Push+ 获取推送token https://pushplus.hxtrip.com/
- 酷推 获取推送token https://cp.xuthus.cc/

**注意:**
- 所需参数均以环境变量方式提供, 本地测试已pycharm为例, 可以在右上角编辑配置将环境变量加入, 也可以自行新建一个test.py, 然后模拟云函数调用.

### 部署
- 环境变量
  - LEANCLOUD_APP_ID leancloud应用ID
  - LEANCLOUD_APP_KEY leancloud应用KEY
  
  - LEANCLOUD_OID 新建数据行ID
  - PUSH_PLUS_TOKEN push+推送token 
  - COOL_PUSH_TOKEN 酷推推送token
  
- 触发器
触发器变量为json格式, key值为直播间ID, 后面具体含义详见index.py中notification_push函数注释
```json
{
  "71415":{
            "push_plus_topic": "",
            "push_plus_template": "",
            "cool_push_type": "",
            "cool_push_specific": ""
           }
}
```
### 维护者
**Virace**
- blog: [孤独的未知数](https://x-item.com)

### 感谢
- [@pcstx1](http://pushplus.hxtrip.com/), **Push+** 服务提供方
- [@xuthus](https://cp.xuthus.cc/), **CoolPush** 服务提供方
- 以及**JetBrains**提供开发环境支持
  
  <a href="https://www.jetbrains.com/?from=kratos-pe" target="_blank"><img src="https://cdn.jsdelivr.net/gh/virace/kratos-pe@main/jetbrains.svg"></a>

### 许可证

[The MIT License](LICENSE)