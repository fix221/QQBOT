from fastapi import FastAPI, Request
from logger import setup_logging
import uvicorn

logging = setup_logging()
app = FastAPI()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)