from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid
import json

from database import get_connection

router = APIRouter()


# POST /orders/ — cria novo pedido
@router.post("/", status_code=201)
async def create_order(order: dict):

    required_fields = ["customer", "items", "total", "payment_method"]

    for field in required_fields:
        if field not in order:
            raise HTTPException(
                status_code=422,
                detail=f"Campo obrigatório ausente: {field}"
            )

    if not order["items"]:
        raise HTTPException(
            status_code=422,
            detail="O pedido não pode ter 0 itens."
        )

    customer = order["customer"]

    for field in ["name", "email", "address"]:
        if field not in customer or not customer[field]:
            raise HTTPException(
                status_code=422,
                detail=f"Dado do cliente ausente: {field}"
            )

    order_id = str(uuid.uuid4())[:8].upper()
    order_number = f"DRP-{order_id}"

    items = [
        {
            "id": item.get("id", ""),
            "name": item.get("name", ""),
            "size": item.get("size", ""),
            "quantity": int(item.get("quantity", 1)),
            "price": float(item.get("price", 0)),
            "subtotal": round(
                float(item.get("price", 0)) *
                int(item.get("quantity", 1)),
                2
            )
        }
        for item in order["items"]
    ]

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
        "items": items,
        "total": round(float(order["total"]), 2),
    }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO orders (
            order_number,
            status,
            created_at,
            customer_name,
            customer_email,
            customer_address,
            payment_method,
            items,
            total
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        document["order_number"],
        document["status"],
        document["created_at"],
        document["customer"]["name"],
        document["customer"]["email"],
        document["customer"]["address"],
        document["payment_method"],
        json.dumps(document["items"]),
        document["total"]
    ))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "order_number": order_number,
        "message": "Pedido recebido com sucesso.",
        "total": document["total"],
        "status": "pending",
    }


# GET /orders/{order_number} — consulta pedido
@router.get("/{order_number}")
async def get_order(order_number: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE order_number = ?
    """, (order_number.upper(),))

    order = cursor.fetchone()

    connection.close()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    order = dict(order)

    return {
        "order_number": order["order_number"],
        "status": order["status"],
        "created_at": order["created_at"],
        "customer": {
            "name": order["customer_name"],
            "email": order["customer_email"],
            "address": order["customer_address"],
        },
        "payment_method": order["payment_method"],
        "items": json.loads(order["items"]),
        "total": order["total"],
    }
