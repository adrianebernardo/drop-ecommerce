from fastapi import APIRouter, HTTPException
from models.schemas import Product, ProductUpdate
from database import get_connection
import json

router = APIRouter()


@router.get("/")
async def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    result = []

    for product in products:
        item = dict(product)

        item["images"] = json.loads(item["images"]) if item["images"] else []
        item["sizes"] = json.loads(item["sizes"]) if item["sizes"] else []
        item["active"] = bool(item["active"])

        result.append(item)

    return result


@router.get("/{product_id}")
async def get_product(product_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    connection.close()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    item = dict(product)

    item["images"] = json.loads(item["images"]) if item["images"] else []
    item["sizes"] = json.loads(item["sizes"]) if item["sizes"] else []
    item["active"] = bool(item["active"])

    return item


@router.post("/")
async def create_product(product: Product):
    connection = get_connection()
    cursor = connection.cursor()

    data = product.model_dump()

    cursor.execute("""
        INSERT INTO products (
            name,
            description,
            price,
            stock,
            category,
            image_url,
            image_product,
            images,
            sizes,
            active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["description"],
        data["price"],
        data["stock"],
        data.get("category"),
        data.get("image_url"),
        data.get("image_product"),
        json.dumps(data.get("images", [])),
        json.dumps(data.get("sizes", [])),
        1
    ))

    connection.commit()

    product_id = cursor.lastrowid

    connection.close()

    return {
        "id": product_id,
        **data,
        "active": True
    }


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    product: ProductUpdate
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    if not cursor.fetchone():
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    data = product.model_dump(exclude_none=True)

    for field in ["images", "sizes"]:
        if field in data:
            data[field] = json.dumps(data[field])

    if data:
        fields = ", ".join(f"{key} = ?" for key in data)
        values = list(data.values())
        values.append(product_id)

        cursor.execute(
            f"UPDATE products SET {fields} WHERE id = ?",
            values
        )

    connection.commit()
    connection.close()

    return {
        "message": "Produto atualizado com sucesso"
    }


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM products WHERE id = ?",
        (product_id,)
    )

    if not cursor.fetchone():
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Produto deletado com sucesso"
    }
