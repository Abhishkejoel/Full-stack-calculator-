import threading
import time
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gradio as gr
import uvicorn


app = FastAPI()

class Numbers(BaseModel):
    x: float
    y: float

@app.post("/add")
def add_numbers_api(numbers: Numbers):
    return {"result": add_numbers(numbers.x, numbers.y)}

@app.post("/subtract")
def subtract_numbers_api(numbers: Numbers):
    return {"result": subtract_numbers(numbers.x, numbers.y)}

@app.post("/multiply")
def multiply_numbers_api(numbers: Numbers):
    return {"result": multiply_numbers(numbers.x, numbers.y)}

@app.post("/divide")
def divide_numbers_api(numbers: Numbers):
    if numbers.y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": divide_numbers(numbers.x, numbers.y)}

def add_numbers(x: float, y: float) -> float:
    return x + y

def subtract_numbers(x: float, y: float) -> float:
    return x - y

def multiply_numbers(x: float, y: float) -> float:
    return x * y

def divide_numbers(x: float, y: float) -> float:
    return x / y


def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)


thread = threading.Thread(target=run_fastapi, daemon=True)
thread.start()


BASE_URL = "http://127.0.0.1:8000"

def perform_operation(operation: str, x: float, y: float) -> str:
    try:
        url = f"{BASE_URL}/{operation}"
        response = requests.post(url, json={"x": x, "y": y})
        response.raise_for_status()
        result = response.json().get("result")
        return str(result)
    except requests.exceptions.HTTPError as err:
        return f"Error: {err.response.json().get('detail')}"


iface = gr.Interface(
    fn=perform_operation,
    inputs=[
        gr.Radio(choices=["add", "subtract", "multiply", "divide"], label="Operation"),
        gr.Number(label="X"),
        gr.Number(label="Y")
    ],
    outputs="text",
    live=False
)


time.sleep(1)
iface.launch()
