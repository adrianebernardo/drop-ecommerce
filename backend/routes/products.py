from fastapi import APIRouter, HTTPException
from models.schemas import Product, ProductUpdate
from firebase_config import db

router = APIRouter()

@router.get("/")
async def get_products():
    products = db.collection("products").stream()
    return [{"id": p.id, **p.to_dict()} for p in products]

@router.get("/{product_id}")
async def get_product(product_id: str):
    doc = db.collection("products").document(product_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"id": doc.id, **doc.to_dict()}

@router.post("/")
async def create_product(product: Product):
    doc_ref = db.collection("products").document()
    doc_ref.set(product.model_dump())
    return {"id": doc_ref.id, **product.model_dump()}

@router.put("/{product_id}")
async def update_product(product_id: str, product: ProductUpdate):
    doc_ref = db.collection("products").document(product_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    doc_ref.update({k: v for k, v in product.model_dump().items() if v is not None})
    return {"message": "Produto atualizado com sucesso"}

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    doc_ref = db.collection("products").document(product_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    doc_ref.delete()
    return {"message": "Produto deletado com sucesso"}