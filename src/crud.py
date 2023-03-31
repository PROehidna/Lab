from sqlalchemy.orm import Session

from src import models, schemas


def create_shop(db: Session, shop: schemas.ShopCreate):

    db_shop = models.Shop(email=shop.email, delivery_charge=shop.delivery_charge)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def create_product(db: Session, product: schemas.ProductCreate):

    db_product = models.Product(product_name=product.product_name, firm=product.firm, model=product.model, tech_character=product.tech_character, price=product.price, lifetime=product.lifetime, picture=product.picture)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_order_delivery(db: Session, delivery: schemas.DeliveryCreate, order_id: int):
 
    db_delivery = models.Delivery(**delivery.dict(), order_id=order_id)
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery


def create_order_for_product_shop(db: Session, order: schemas.OrderCreate, product_id: int, shop_id: int):
 
    db_order = models.Order(**order.dict(), product_id=product_id, shop_id=shop_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_shop_by_id(db:Session, shop_id: int):
    return db.query(models.Shop).filter(models.Shop.id==shop_id).first()

def get_order_by_id(db:Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id==order_id).first()

def get_product_by_id(db:Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id==product_id).first()

def get_delivery_by_id(db:Session, delivery_id: int):
    return db.query(models.Delivery).filter(models.Delivery.id==delivery_id).first()

def get_delivery_by_order_id(db: Session, order_id: int):
    return db.query(models.Delivery).filter(models.Delivery.order_id == order_id).first()



def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.product_name == product_name).first()

def get_shop_by_email(db: Session, email: str):
    return db.query(models.Shop).filter(models.Shop.email == email).first()



def get_products(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Product).offset(skip).limit(limit).all()

def get_orders(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Order).offset(skip).limit(limit).all()

def get_deliveries(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Delivery).offset(skip).limit(limit).all()

def get_shops(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Shop).offset(skip).limit(limit).all()