### QQBOT
SM腾讯的接口和各大AI接口对接
***
## 编辑守则
- 高度可控
- 写明对称
- 使用LLOnebot接口，请查阅官方文档
- 写明注释
***
## 对称表
| 文件名               | 用途               |
|---------------------|-------------------|
| ai_handler.py       | AI主逻辑          |
| api_router.py       | 主逻辑            |
| image_handler.py    | 图片处理          |
| logger.py           | 日志输出          |
| onebot_handler.py   | 发送群消息        |
***
## 文件目录
OOBOT
│  README.md
│  requirements.txt
│  启动.bat
│  安装依赖.bat
│  
├─img
│      background.jpg
│      
├─library
│  │  ai_handler.py
│  │  api_router.py
│  │  image_handler.py
│  │  logger.py
│  │  onebot_handler.py
│  │  
│  ├─backup
│  │      BOT.py
│  │      
│  ├─font
│  │      Fort_1.ttf
│  │      
│  ├─web
│  └─__pycache__
│          ai_handler.cpython-312.pyc
│          image_handler.cpython-312.pyc
│          logger.cpython-312.pyc
│          onebot_handler.cpython-312.pyc
│          
├─tmp
│      2024-09-29-17.42.26.png
│      2024-09-29-18.08.49.png
│      2024-10-01-00.39.07.png
│      
└─web
        Index.html
''' 如何生成结构树
在文件夹中输入 tree /f > list.txt 即可
'''
