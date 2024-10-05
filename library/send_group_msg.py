import httpx
import logging
import urllib.parse
import yaml
import os

file = os.getcwd()

# 加载配置文件
def load_config():
    with open("config/main.yml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

async def send_group_msg(group_id: str, type: str, image_path: str = None, text: str = None):
    async with httpx.AsyncClient() as client:
        try:
            if type == 'image':
                if not group_id or not image_path:
                    logging.error("缺少必要的参数 group_id 或 image_path")
                    return None
                
                payload = {
                    "group_id": group_id,
                    "message": [
                        {
                            "type": "image",
                            "data": {
                                "file": file + "/" + image_path.replace("\\", "/")  # 替换路径格式
                            }
                        }
                    ]
                }
            elif type == 'message':
                if not group_id or not text:
                    logging.error("缺少必要的参数 group_id 或 text")
                    return None
                
                payload = {
                    "group_id": group_id,
                    "message": text
                }
            else:
                logging.error("不支持的类型")
                return None

            logging.info(f"发送到群组 {group_id} 的消息: {payload}")
            response = await client.post(config['bot_url'] + "/send_group_msg", json=payload)
            response.raise_for_status()
            logging.info(f"消息发送成功: {response.status_code}")
            logging.info(f"返回结果: {response.json()}")  # 打印返回结果
            return response.json()
        except Exception as e:
            logging.error(f"消息发送期间发生错误: {e}")
            return None