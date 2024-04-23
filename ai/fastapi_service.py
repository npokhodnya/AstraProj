from fastapi import FastAPI
from ai.ai import predict
import uvicorn
import os
import signal


app = FastAPI()


@app.post("/")
def neuralink_processing(data) -> list:
    print(data)
    return predict(data)


@app.post("/stop_server")
def stop_server():
    os.kill(os.getpid(), signal.SIGTERM)


def start():
    uvicorn.run(app, host="127.0.0.1", port=6900)


if __name__ == "__main__":
    start()
