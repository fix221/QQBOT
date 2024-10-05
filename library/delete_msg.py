import httpx
import logging
import yaml
import os

# 获取当前工作目录
file = os.getcwd()

# 加载配置文件
def load_config():
    with open("config/main.yml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

async def delete_msg(message_id: int):
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "message_id": message_id
            }
            logging.info(f"尝试撤回消息: {payload}")
            response = await client.post(config['bot_url'] + "/delete_msg", json=payload)
            response.raise_for_status()
            logging.info(f"撤回消息成功: {response.status_code}")
            logging.info(f"返回结果: {response.json()}")  # 打印返回结果
            return response.json()
        except Exception as e:
            logging.error(f"撤回消息时发生错误: {e}")
            return None