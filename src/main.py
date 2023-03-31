from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():

    db = SessionLocal()# pragma: no cover
    try:# pragma: no cover
        yield db# pragma: no cover
    finally:# pragma: no cover
        db.close()# pragma: no cover


@app.get("/shops/", response_model=list[schemas.Shop])
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    shops = crud.get_shops(db, skip=skip, limit=limit)
    return shops

@app.get("/shops/{shop_id}", response_model=schemas.Shop)
def read_shop_by_id(shop_id: int, db: Session = Depends(get_db)):

    db_shop = crud.get_shop_by_id(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return db_shop


@app.post("/shops/", response_model=schemas.Shop)
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(get_db)):

    db_shop = crud.get_shop_by_email(db, email=shop.email)
    if db_shop:
        raise HTTPException(status_code=400, detail="Shop email is already exist")
    return crud.create_shop(db=db, shop=shop)



@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):

    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    db_product = crud.get_product_by_name(db, product_name=product.product_name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product name is already exist")
    return crud.create_product(db=db, product=product)


@app.post("/products/{product_id}/orders/{shop_id}", response_model=schemas.Order)
def create_order_for_product_shop(
    shop_id: int, product_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)
):

    return crud.create_order_for_product_shop(db=db, order=order, product_id=product_id, shop_id=shop_id)




@app.get("/deliveries/", response_model=list[schemas.Delivery])
def read_deliveries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    deliveries = crud.get_deliveries(db, skip=skip, limit=limit)
    return deliveries

@app.get("/deliveries/{delivery_id}", response_model=schemas.Delivery)
def read_delivery_by_id(delivery_id: int, db: Session = Depends(get_db)):

    db_shop = crud.get_delivery_by_id(db, delivery_id=delivery_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return db_shop



@app.post("/orders/{order_id}/deliveries/", response_model=schemas.Delivery)
def create_delivery_for_order(
    order_id: int, delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = crud.get_delivery_by_order_id(db, order_id=order_id)
    if db_delivery:
        raise HTTPException(status_code=404, detail="Delivery order id already exist")
    return crud.create_order_delivery(db=db,delivery=delivery, order_id=order_id)


@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):

    db_order = crud.get_order_by_id(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

