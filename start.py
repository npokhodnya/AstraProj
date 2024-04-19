from ai import fastapi_service
from app import main
import multiprocessing


def start():
    app_process = multiprocessing.Process(target=main.start)
    ai_process = multiprocessing.Process(target=fastapi_service.start)
    app_process.start()
    ai_process.start()
    app_process.join()
    ai_process.join()


if __name__ == "__main__":
    start()
