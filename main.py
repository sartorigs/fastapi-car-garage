import json
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from pydantic import BaseModel
from types import SimpleNamespace

class Car(BaseModel):
    id: int
    brand: str
    model: str
    plate: str

carList = []

app = FastAPI()


@app.post("/car/")
async def create_car(car: Car):
    if any(car.id == car.id for car in carList):
        return {"message": "Um carro com este mesmo id já foi cadastrado!"}
    carList.append(car)
    return car

def cars_dict(car):
    return car.__dict__

@app.get("/car/{car_id}")
async def get_car_by_id(car_id: int):
    for car in carList:
        if(car.id == car_id ):
            return car
    return {"message": "Não foi possível encontrar o carro por este ID!"}



@app.get("/all/")
async def get_all_cars():
    return json.dumps(carList, default=cars_dict)

@app.delete("/delete/{car_id}")
async def delete_car(car_id: int):
    for car in carList:
        if(car.id == car_id):
            carList.remove(car)
            break
    return True

@app.get("/car/{car_id}", response_class=HTMLResponse)
async def read_car(car_id: int):
    car = json.load(get_car_by_id(car_id),object_hook=lambda d: SimpleNamespace(**d))
    return f"""
    <html>
        <head>
            <title>{car.model} | {car.brand}</title>
        </head>
        <body>
            <h1>MODEL: {car.model}</h1>
            <h1>BRAND: {car.brand}</h1>
            <h1>PLATE: {car.plate}</h1>
        </body>
    </html>
    """


