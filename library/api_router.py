from fastapi import APIRouter, Request
from logger import setup_logging
from ai_handler import call_ai_api
from onebot_handler import send_image_to_onebot, send_get_request
from image_handler import create_image
import requests
import os
import yaml

router = APIRouter()

# 加载配置文件
def load_config():
    with open("config/main.yml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

logging = setup_logging()

@router.on_event("startup")
async def startup_event():
    logging.info('应用启动')

@router.on_event("shutdown")
async def shutdown_event():
    logging.info('应用关闭')

@router.get("/")
async def get_root(request: Request):
    group_id = request.query_params.get("group_id") 
    if group_id:
        return {"message": "初始化成功"}
    else:
        return {"Error": "需要组 ID"}

# 主逻辑路由
@router.post("/")
async def root_handler(request: Request):
    try:
        data = await request.json()
        logging.info(f"请求: {data}")
        
        group_id = data.get("group_id", "NO_GROUP_ID")
        user_is_root = data.get("user_id") == config['root']
        data["root"] = user_is_root

        target_qq = '3565439736'
        message = data.get('message', [])
        command_called = False  # 添加一个标志，用于指示是否调用了命令
        
        for msg in message:
            if msg.get('type') == 'at' and msg.get('data', {}).get('qq') == target_qq:
                text_msg = next((m for m in message if m.get('type') == 'text'), None)
                if text_msg:
                    text = text_msg.get("data", {}).get("text", "")
                    logging.info(f"收到文本: {text}")
                    if text.startswith(' /'):
                        # 执行命令
                        PIC = "随机图片"
                        if PIC in text:
                            # 下载图片
                            response = requests.get('https://t.mwm.moe/mp')
                            if response.status_code == 200:
                                image_path = 'tmp/' + os.path.basename(response.url)
                                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                                with open(image_path, 'wb') as f:
                                    f.write(response.content)
                                logging.info(f"图片保存路径: {image_path}")
                                await send_image_to_onebot(group_id, image_path)
                                return {"message": "图片已发送"}
                            else:
                                return {"error": "无法下载图片"}
                        command_called = True  # 标记命令已被调用
                        break  # 跳出循环，不再处理其他消息

        if not command_called:
            # 只有在命令未被调用时才调用AI
            logging.info("AI:true")
            data["AI"] = True
            user_id = data.get("user_id")
            text_msg = next((m for m in message if m.get('type') == 'text'), None)
            if text_msg:
                text = text_msg.get("data", {}).get("text", "")
                input_text = f"{user_id} {text}"
                logging.info(f"准备输入AI的文本: {input_text}")
                ai_response = await call_ai_api(input_text)
                data["AI_RESPONSE"] = ai_response
                if ai_response.get("code") == "Success":
                    response_text = ai_response.get("AI_OUT", {}).get("text", "")
                    if len(response_text) > 250:
                        image_path = create_image(response_text)
                        await send_image_to_onebot(group_id, image_path)
                    else:
                        await send_get_request(group_id, response_text) 
                else:
                    logging.error("失败")
            else:
                logging.info("AI:false")
                data["AI"] = False
        
        return data
    except Exception as e:
        logging.exception("发生错误: %s", str(e))
        return {"error": f"Error: {str(e)}"}