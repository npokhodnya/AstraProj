from fastapi import FastAPI
from ai.ai import predict

app = FastAPI()


@app.post("/")
def neuralink_processing(data: list):
    return predict(data)


def start():
    import uvicorn
    print("good")
    uvicorn.run(app, host="127.0.0.1", port=6900)


if __name__ == "__main__":
    start()
