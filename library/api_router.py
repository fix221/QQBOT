from fastapi import FastAPI, Request
from logger import setup_logging
from ai_handler import call_ai_api
from onebot_handler import send_image_to_onebot, send_get_request, send_message_to_onebot
from image_handler import create_image
import uvicorn
import yaml
import requests
import os

# 加载配置文件 123
def load_config():
    with open("config/main.yml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

logging = setup_logging()
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.warning_sent = False

@app.on_event("shutdown")
async def shutdown_event():
    logging.info('滚！')
    app.warning_sent = False

@app.get("/")
async def get_root(request: Request):
    group_id = request.query_params.get("group_id") 
    if group_id:
        return {"message": "初始化成功"}
    else:
        return {"Error": "需要组 ID"}

# 主逻辑路由
@app.post("/")
async def root_handler(request: Request):
    try:
        data = await request.json()
        logging.info(f"请求: {data}")
        if "group_id" in data: # 群消息
            group_id = data.get("group_id", "NO_GROUP_ID")
            user_is_root = data.get("user_id") == config['root']
            data["root"] = user_is_root

            target_qq = '227278359'
            message = data.get('message', [])
            logging.info(f"收到消息: {message}")
            command_called = False  # 添加一个标志，用于指示是否调用了命令
            use_ai = False 
            for msg in message:
                #如果没@
                if msg.get('type') == 'text':
                    text_msg = next((m for m in message if m.get('type') == 'text'), None)
                    text = text_msg.get("data", {}).get("text", "")
                    if "抱抱" in text:
                            await send_message_to_onebot(group_id, "抱抱")
                            return {"message": "抱抱已发送"}
                    if "喵喵" in text:
                        await send_message_to_onebot(group_id, "喵喵")
                        return {"message": "喵喵已发送"}
                #如果@了机器人，则执行命令
                if msg.get('type') == 'at' and msg.get('data', {}).get('qq') == target_qq:
                    text_msg = next((m for m in message if m.get('type') == 'text'), None)
                    # logging.info(f"发送内容：{text_msg}")
                    if text_msg:
                        text = text_msg.get("data", {}).get("text", "")
                        # logging.info(f"收到文本: {text}")
                        # if text.startswith(' /'):
                            # 执行命令
                        # command = "随机图片"
                        # logging.info("发送内容："+text)
                        if "随机图片" in text:
                            # 下载图片
                            response = requests.get('https://www.dmoe.cc/random.php')
                            if response.status_code == 200:
                                image_path = 'tmp/' + os.path.basename(response.url)
                                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                                with open(image_path, 'wb') as f:
                                    f.write(response.content)
                                logging.info(f"图片保存路径: {image_path}")
                                await send_image_to_onebot(group_id, image_path)
                                command_called = True  # 标记命令已被调用
                                return {"message": "图片已发送"}
                            else:
                                return {"error": "无法下载图片"}
                        elif "抱抱" in text:
                            command_called = True  # 标记命令已被调用
                            await send_message_to_onebot(group_id, "抱抱")
                            return {"message": "抱抱已发送"}
                        elif "喵喵" in text:
                            command_called = True  # 标记命令已被调用
                            # break  # 跳出循环，不再处理其他消息
                            await send_message_to_onebot(group_id, "喵喵")
                            return {"message": "喵喵已发送"}
                        else:
                            #获得谁@我
                            at_user = data.get('sender', {}).get('card', "")
                            logging.info(f"收到@: {at_user}")
                            await send_message_to_onebot(group_id, f"{at_user} 欸欸欸？不许瞎@我，会生气的！")
                            command_called = True  # 标记命令已被调用
                            # break  # 跳出循环，不再处理其他消息
                            return {"message": "反@已发送"}
                            
            if not command_called and use_ai:
                target_qq = '227278359'
                # 只有在命令未被调用时才调用AI
                #添加调用ai条件
                
                
                        
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
        else: # 私聊消息
            # return {"message": "私聊消息"}
            logging.info("私聊消息")
            logging.info(data)
    except Exception as e:
        logging.exception("发生错误: %s", str(e))
        return {"error": f"Error: {str(e)}"}

# FastAPI,启动!
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)