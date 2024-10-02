from fastapi import FastAPI
from logger import setup_logging
from api_router import root_handler

logging = setup_logging()
app = FastAPI()

app.include_router(root_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)