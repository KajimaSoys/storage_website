from fastapi import FastAPI, Query
from service import Product, db_insert, db_select
from repository import init_db, close_db, init_table
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO, format='%(levelname)s:\t  %(asctime)s|%(name)s| %(message)s')
logger = logging.getLogger(__name__)


@app.on_event("startup")
def startup_event():
    # Инициализация подключения к бд
    init_db()

    # Инициализация таблицы товаров
    init_table()
    logger.info("App successfully started!")


@app.on_event("shutdown")
def shutdown_event():
    close_db()
    logger.info("App successfully closed!")


@app.post("/product/")
def create_product(product: Product):
    # Конвертация всех строковых данных в нижний регистр
    product.name = product.name.lower()
    product.type = product.type.lower()
    product.manufacturer = product.manufacturer.lower()

    if db_insert(product):
        return {"message": "Product created successfully"}
    else:
        return {"message": "An error occurred on product creation"}


@app.get("/products/")
def get_products(
        name: str = Query(None),
        type: str = Query(None),
        manufacturer: str = Query(None),
        min_price: float = Query(None),
        max_price: float = Query(None),
        min_weight: float = Query(None),
        max_weight: float = Query(None)
):
    products = db_select(name, type, manufacturer, min_price, max_price, min_weight, max_weight)

    return products
