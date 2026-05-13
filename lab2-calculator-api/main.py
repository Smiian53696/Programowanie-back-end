
from fastapi import FastAPI, HTTPException
# tworzenie aplikacji
app = FastAPI(
    title="Calculator API",
    version="1.0"
)


#------------------------------------------główny endpoint--------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Calculator API is working"
    }


#------------------------------------------dodawanie dwóch liczb------------------------------------------
@app.get("/add")
def add(a: float, b: float):
    result = a + b

    return {
        "a": a,
        "b": b,
        "operation": "add",
        "result": result
    }


#------------------------------------------odejmowanie dwóch liczb------------------------------------------
@app.get("/subtract")
def subtract(a: float, b: float):
    result = a - b

    return {
        "a": a,
        "b": b,
        "operation": "subtract",
        "result": result
    }


# ------------------------------------------mnożenie dwóch liczb------------------------------------------
@app.get("/multiply")
def multiply(a: float, b: float):
    result = a * b

    return {
        "a": a,
        "b": b,
        "operation": "multiply",
        "result": result
    }


# ------------------------------------------dzielenie dwóch liczb------------------------------------------
@app.get("/divide")
def divide(a: float, b: float):

    # sprawdzenie dzielenia przez zero
    if b == 0:
        raise HTTPException(
            status_code=400,
            detail="Nie można dzielić przez zero"
        )

    result = a / b

    return {
        "a": a,
        "b": b,
        "operation": "divide",
        "result": result
    }