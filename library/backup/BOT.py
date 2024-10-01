import uvicorn
import logging
import httpx
import os
import urllib.parse
import requests
import re
import time
import textwrap
from io import BytesIO
from fastapi import FastAPI, Request
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

# 初始化日志和FastAPI应用
logging.basicConfig(level=logging.INFO)
app = FastAPI()

# 初始化666666
client = OpenAI(
    api_key="sk-8882a4f31dc04aafac5779735cb946d6",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def get_temp_image_path():
    # 获取临时图片路径
    temp_dir = os.path.join(os.path.dirname(__file__), "tmp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return os.path.join(temp_dir, "temp_image.jpg")

def get_random_image():
    url = "https://t.mwm.moe/mp" 
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        return image
    else:
        raise Exception("Failed to fetch random image")

def resize_image_proportionally(image, base_width):
    width_ratio = base_width / image.width
    new_height = int(image.height * width_ratio)
    return image.resize((base_width, new_height), Image.Resampling.LANCZOS)

def create_image(text, background_url=None):
    font_path = 'G:\\桌面\\BOT\\library\\font\\Fort_1.ttf'
    font_size = 20
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        logging.error(f"Font file not found or cannot be opened. Please check the font path: {font_path}")
        return
    image_width = 600
    padding = 50
    line_spacing = 10
    processed_text = re.sub(r'(\d+)\.', r'\1.\n', text)
    wrapped_lines = textwrap.wrap(processed_text, width=25)
    text_height = len(wrapped_lines) * (font_size + line_spacing) - line_spacing + 2 * padding
    if background_url:
        background_image = Image.open(background_url)
        if background_image.mode != 'RGBA':
            background_image = background_image.convert('RGBA')
    else:
        background_image = get_random_image()
        background_image = resize_image_proportionally(background_image, image_width)
        if background_image.mode != 'RGBA':
            background_image = background_image.convert('RGBA')
    text_image = Image.new("RGBA", background_image.size, (255, 255, 255, 98))
    draw = ImageDraw.Draw(text_image)
    current_height = padding
    for line in wrapped_lines:
        draw.text((padding, current_height), line, font=font, fill=(0, 0, 0))
        current_height += font_size + line_spacing
    combined_image = Image.alpha_composite(background_image, text_image)
    timestamp = time.strftime("%Y-%m-%d-%H.%M.%S")
    filename = f"G:\\桌面\\BOT\\tmp\\{timestamp}.png"
    combined_image.save(filename)
    print(f"Image saved to {filename}")
    return filename

# 图片返回函数
async def send_image_to_onebot(group_id: str, image_path: str):
    # 发送图片到指定群组（遵循OneBot v11协议）
    async with httpx.AsyncClient() as client:
        try:
            # 构造请求数据
            payload = {
                "group_id": group_id,
                "message": [
                    {
                        "type": "image",
                        "data": {
                            "file": image_path.replace("\\", "/")  # 替换路径格式
                        }
                    }
                ]
            }
            logging.info(f"发送图片到群组 {group_id}")
            response = await client.post("http://localhost:3000/send_group_msg", json=payload)
            response.raise_for_status()
            logging.info(f"OneBot图片发送成功: {response.status_code}")
            logging.info(f"返回结果: {response.json()}")  # 打印返回结果
        except Exception as e:
            logging.error(f"OneBot图片发送期间发生错误: {e}")

# 文本返回函数
async def send_get_request(group_id: str, message: str):
    async with httpx.AsyncClient() as client:
        try:
            query_params = {
                "action": "send_group_msg",
                "group_id": group_id,
                "message": message
            }
            encoded_url = f"http://localhost:3000/send_group_msg?{urllib.parse.urlencode(query_params)}"
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

# AI调用函数
async def call_ai_api(input_text: str):
    try:
        completion = client.chat.completions.create(model="qwen-plus", messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': input_text}])
        return {"code": "Success", "AI_OUT": {"text": completion.choices[0].message.content}}
    except Exception as e:
        logging.error(f"AI API调用错误: {e}")
        return {"code": "Error", "message": str(e)}

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
        
        group_id = data.get("group_id", "NO_GROUP_ID")
        user_is_root = data.get("user_id") == 1925019494
        data["root"] = user_is_root

        target_qq = '3565439736'
        message = data.get('message', [])
        ai_called = False
        
        for msg in message:
            if msg.get('type') == 'at' and msg.get('data', {}).get('qq') == target_qq:
                if not ai_called:
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
                        ai_called = True
                else:
                    logging.info("成功")
                break
        
        if not ai_called:
            logging.info("AI:false")
            data["AI"] = False
            
        return data
    except Exception as e:
        logging.exception("发生错误: %s", str(e))
        return {"error": f"Error: {str(e)}"}
# FastAPI,启动!
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

