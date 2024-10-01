from fastapi import FastAPI, Request
from logger import setup_logging
from ai_handler import call_ai_api
from onebot_handler import send_image_to_onebot, send_get_request
from image_handler import create_image
import uvicorn

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
