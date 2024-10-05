
# QQBOT

SM腾讯的接口和各大AI接口对接

## 编辑守则

- 高度可控
- 写明对称
- 写明注释
- 使用LLOnebot接口，请查阅官方文档
- 可提供的传入数据： {text} {group_id} {user_id} {message_id} {raw_message} {message_type}

## 温馨提示

- bot发送文件的路径必须为全局路径，请通过OS库构建flie路径

## 对称表

| 文件名               | 用途               |
|---------------------|-------------------|
| ai_handler.py       | AI主逻辑          |
| api_router.py       | 主逻辑            |
| image_handler.py    | 图片处理          |
| logger.py           | 日志输出          |
| onebot_handler.py   | 发送群消息        |

# 接口适配

- [x] send_private_msg
- [] delete_msg
- [] send_like
- [] set_friend_add_request
- [] set_group_ban
- [] set_group_whole_ban
- [] get_image
- [] get_record
- [] upload_group_file
- [] send_group_forward_msg
- [] send_private_forward_msg

推荐查阅
[Go CQHTTP 文档](https://docs.go-cqhttp.org/api/)
[QQBOT函数引用](https://github.com/YuanXiaCN/QQBOT/blob/main/doc/README.md)
