# main.py

from fastapi import FastAPI
import json
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Formi backend!"}

@app.get("/info/{category}")
def get_info(category: str):
    try:
        with open(os.path.join("data", f"{category}.json")) as f:
            data = json.load(f)
            return {"success": True, "data": data}
    except FileNotFoundError:
        return {"success": False, "message": "Category not found"}
