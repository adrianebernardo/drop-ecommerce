from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products
from routes import orders                          # ← novo

app = FastAPI(title="Next--Cart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])   # ← novo

@app.get("/")
async def root():
    return {"message": "Next--Cart API rodando!"}