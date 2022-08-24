from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
def home_page():
    return {"Hello" : "Hello"}


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()