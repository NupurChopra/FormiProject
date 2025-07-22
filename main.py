# main.py

from fastapi import FastAPI
import json
import os
import tiktoken

app = FastAPI()

def limit_tokens(text: str, max_tokens=800):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return encoding.decode(tokens[:max_tokens])

@app.get("/")
def root():
    return {"message": "Hello from Formi backend!"}

@app.get("/info/{category}")
def get_info(category: str):
    try:
        with open(os.path.join("data", f"{category}.json")) as f:
            data = json.load(f)
            limited_text = limit_tokens(json.dumps(data))
            return {"success": True, "data": limited_text}
    except FileNotFoundError:
        return {"success": False, "message": "Category not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}
