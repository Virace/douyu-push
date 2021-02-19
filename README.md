# douyu-push
斗鱼直播间直播推送, 专治随缘主播(狗头)

腾讯云函数部署:

环境变量:

- LEANCLOUD_APP_ID leancloud应用ID
- LEANCLOUD_APP_KEY leancloud应用KEY

- LEANCLOUD_OID 新建数据行ID
- PUSH_PLUS_TOKEN push+推送token 
- COOL_PUSH_TOKEN 酷推推送token

push+推送token, 访问: https://pushplus.hxtrip.com/后, 点击一对多或一对一推动微信扫码后获得.

酷推: https://cp.xuthus.cc/

触发器: 

触发器变量为json格式
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
key值为直播间ID, 后面具体含义详见index.py中notification_push函数注释


