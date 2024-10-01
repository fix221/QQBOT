import logging
from openai import OpenAI
import yaml

# 读取配置文件
with open("config/main.yml", "r") as file:
    config = yaml.safe_load(file)

client = OpenAI(
    api_key=config["AI_api_key"],
    base_url=config["AI_url"]
)

async def call_ai_api(input_text: str):
    try:
        completion = client.chat.completions.create(model="qwen-plus", messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': input_text}])
        return {"code": "Success", "AI_OUT": {"text": completion.choices[0].message.content}}
    except Exception as e:
        logging.error(f"AI API调用错误: {e}")
        return {"code": "Error", "message": str(e)}