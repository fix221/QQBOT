import logging
import httpx
from openai import OpenAI

client = OpenAI(
    api_key="sk-8882a4f31dc04aafac5779735cb946d6",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

async def call_ai_api(input_text: str):
    try:
        completion = client.chat.completions.create(model="qwen-plus", messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': input_text}])
        return {"code": "Success", "AI_OUT": {"text": completion.choices[0].message.content}}
    except Exception as e:
        logging.error(f"AI API调用错误: {e}")
        return {"code": "Error", "message": str(e)}