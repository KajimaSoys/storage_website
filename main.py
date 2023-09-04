from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

from service import Product, product_insert, product_select, get_options
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
    if product_insert(product):
        return {"message": "Product created successfully"}
    else:
        return {"message": "An error occurred on product creation"}


@app.get("/products/")
def get_products(
        name: str = Query(None),
        type: str = Query(None),
        manufacturer: str = Query(None),
        min_price: str = Query(None),
        max_price: str = Query(None)
):
    products = product_select(name, type, manufacturer, min_price, max_price)

    return products


@app.get("/types/")
def get_unique_types():
    types = get_options("type")
    return {"types": types}


@app.get("/manufacturers/")
def get_unique_manufacturers():
    manufacturers = get_options("manufacturer")
    return {"manufacturers": manufacturers}


app.mount("/", StaticFiles(directory="static"), name="static")
