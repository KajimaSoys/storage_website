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


def db_insert(product):
    try:
        with get_cursor() as cursor:
            cursor.execute("""
                    INSERT INTO products (name, type, price, date, weight, height, width, depth, manufacturer)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, product.model_dump().values()) 
        logger.info("Product created successfully!")
        return True
    except Exception:
        logger.exception("An error occurred on product creation!")
        return False


def db_select(name, type, manufacturer, min_price, max_price, min_weight, max_weight):
    with get_cursor() as cursor:
        query = "SELECT * FROM products WHERE TRUE"
        params = []

        if name:
            query += " AND name=%s"
            params.append(name.lower())
        if type:
            query += " AND type=%s"
            params.append(type.lower())
        if manufacturer:
            query += " AND manufacturer=%s"
            params.append(manufacturer.lower())
        if min_price is not None:
            query += " AND price>=%s"
            params.append(min_price)
        if max_price is not None:
            query += " AND price<=%s"
            params.append(max_price)
        if min_weight is not None:
            query += " AND weight>=%s"
            params.append(min_weight)
        if max_weight is not None:
            query += " AND weight<=%s"
            params.append(max_weight)

        cursor.execute(query, params)
        products = cursor.fetchall()

    return products
