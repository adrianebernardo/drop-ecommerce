from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products
from routes import orders
from database import create_tables

app = FastAPI(title="DRØP API")

# Cria as tabelas do banco automaticamente ao iniciar a API
create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    products.router,
    prefix="/products",
    tags=["products"]
)

app.include_router(
    orders.router,
    prefix="/orders",
    tags=["orders"]
)


@app.get("/")
async def root():
    return {"message": "DRØP API rodando!"}