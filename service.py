from pydantic import BaseModel
from datetime import date
from repository import get_cursor
import logging

logger = logging.getLogger(__name__)


class Product(BaseModel):
    name: str
    type: str
    price: float
    date: date
    weight: float
    height: float
    width: float
    depth: float
    manufacturer: str


def product_insert(product):
    try:
        with get_cursor() as cursor:
            cursor.execute("""
                    INSERT INTO products (name, type, price, date, weight, height, width, depth, manufacturer)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, tuple(product.model_dump().values()))
        logger.info("Product created successfully!")
        return True
    except Exception:
        logger.exception("An error occurred on product creation!")
        return False


def product_select(name, type, manufacturer, min_price, max_price):
    with get_cursor() as cursor:
        query = "SELECT * FROM products WHERE TRUE"
        params = []

        if name:
            query += " AND name ILIKE %s"
            params.append(f"%{name.lower()}%")
        if type:
            query += " AND type ILIKE %s"
            params.append(f"%{type.lower()}%")
        if manufacturer:
            query += " AND manufacturer ILIKE %s"
            params.append(f"%{manufacturer.lower()}%")
        if min_price:
            query += " AND price>=%s"
            params.append(min_price)
        if max_price:
            query += " AND price<=%s"
            params.append(max_price)

        cursor.execute(query, params)
        products = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        products = [dict(zip(columns, row)) for row in products]

    return products


def get_options(column_name):
    with get_cursor() as cursor:
        query = f"SELECT DISTINCT {column_name} FROM products"
        cursor.execute(query)
        unique_values = cursor.fetchall()

        unique_values = [value[0] for value in unique_values]
    return unique_values
