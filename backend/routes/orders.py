from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid

router = APIRouter()

# Firebase será importado do módulo de configuração do projeto
# Ajuste o import conforme seu firebase_config.py
try:
    from firebase_config import db
except ImportError:
    db = None  # fallback para testes sem Firebase


# ──────────────────────────────────────────────
# POST /orders/  — cria novo pedido
# ──────────────────────────────────────────────
@router.post("/", status_code=201)
async def create_order(order: dict):
    """
    Recebe o pedido do frontend e salva no Firestore.

    Payload esperado:
    {
        "customer": {
            "name": "Ana Lima",
            "email": "ana@email.com",
            "address": "Rua das Flores, 42 — SP"
        },
        "payment_method": "pix" | "credit_card" | "boleto",
        "items": [
            {
                "id": "prod_abc",
                "name": "CARGO WIDE LEG",
                "size": "M",
                "quantity": 1,
                "price": 289.90
            }
        ],
        "total": 289.90
    }
    """

    # Validação mínima
    required_fields = ["customer", "items", "total", "payment_method"]
    for field in required_fields:
        if field not in order:
            raise HTTPException(
                status_code=422,
                detail=f"Campo obrigatório ausente: {field}"
            )

    if not order["items"]:
        raise HTTPException(status_code=422, detail="O pedido não pode ter 0 itens.")

    customer = order["customer"]
    for field in ["name", "email", "address"]:
        if field not in customer or not customer[field]:
            raise HTTPException(
                status_code=422,
                detail=f"Dado do cliente ausente: {field}"
            )

    # Monta documento
    order_id = str(uuid.uuid4())[:8].upper()  # ex: A3F9B2C1
    order_number = f"DRP-{order_id}"

    document = {
        "order_number": order_number,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "customer": {
            "name": customer["name"].strip(),
            "email": customer["email"].strip().lower(),
            "address": customer["address"].strip(),
        },
        "payment_method": order["payment_method"],
        "items": [
            {
                "id": item.get("id", ""),
                "name": item.get("name", ""),
                "size": item.get("size", ""),
                "quantity": int(item.get("quantity", 1)),
                "price": float(item.get("price", 0)),
                "subtotal": round(float(item.get("price", 0)) * int(item.get("quantity", 1)), 2),
            }
            for item in order["items"]
        ],
        "total": round(float(order["total"]), 2),
    }

    # Salva no Firestore
    if db:
        try:
            db.collection("orders").document(order_number).set(document)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar no Firestore: {str(e)}")
    else:
        # Modo desenvolvimento sem Firebase — apenas loga
        print(f"[DEV] Pedido gerado (sem Firebase): {document}")

    return {
        "success": True,
        "order_number": order_number,
        "message": "Pedido recebido com sucesso.",
        "total": document["total"],
        "status": "pending",
    }


# ──────────────────────────────────────────────
# GET /orders/{order_number}  — consulta pedido
# ──────────────────────────────────────────────
@router.get("/{order_number}")  
async def get_order(order_number: str):
    """Retorna os dados de um pedido pelo número (ex: DRP-A3F9B2C1)."""

    if not db:
        raise HTTPException(status_code=503, detail="Banco de dados não configurado.")

    try:
        doc = db.collection("orders").document(order_number.upper()).get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar Firestore: {str(e)}")

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    return doc.to_dict()