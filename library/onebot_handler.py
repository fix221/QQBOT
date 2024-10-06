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

async def send_image_to_onebot(group_id: str, image_path: str):
    async with httpx.AsyncClient() as client:
        try:
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
            logging.info(f"{payload}")
            logging.info(f"发送图片到群组 {group_id}")
            response = await client.post(config['bot_url'] + "/send_group_msg", json=payload)
            response.raise_for_status()
            logging.info(f"OneBot图片发送成功: {response.status_code}")
            logging.info(f"返回结果: {response.json()}")  # 打印返回结果
        except Exception as e:
            logging.error(f"OneBot图片发送期间发生错误: {e}")

async def send_get_request(group_id: str, message: str):
    async with httpx.AsyncClient() as client:
        try:
            query_params = {
                "action": "send_group_msg",
                "group_id": group_id,
                "message": message
            }
            encoded_url = f"{config['bot_url']}/send_group_msg?{urllib.parse.urlencode(query_params)}"
            response = await client.get(encoded_url)
            response.raise_for_status()
            logging.info(f"GET请求成功: {response.status_code}")
            logging.info(f"返回结果: {response.json()}")  # 打印返回结果
            return response
        except httpx.HTTPStatusError as exc:
            logging.error(f"GET请求失败，状态码：{exc.response.status_code}")
            return None
        except Exception as e:
            logging.error(f"GET请求错误: {e}")
            return None
        
async def send_message_to_onebot(group_id: str, message: str):
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "group_id": group_id,
                "message": message
            }
            logging.info(f"{payload}")
            logging.info(f"发送消息到群组 {group_id}")
            response = await client.post(config['bot_url'] + "/send_group_msg", json=payload)
            response.raise_for_status()
            logging.info(f"OneBot消息发送成功: {response.status_code}")
            logging.info(f"返回结果: {response.json()}")  # 打印返回结果
        except Exception as e:
            logging.error(f"OneBot消息发送期间发生错误: {e}")