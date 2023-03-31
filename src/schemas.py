from pydantic import BaseModel
from datetime import date

class DeliveryBase(BaseModel):
    date_delivery: date
    address: str
    client_name: str
    courier_name: str 

class DeliveryCreate(DeliveryBase):
    pass

class Delivery(DeliveryBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True



class OrderBase(BaseModel):
    order_date: date
    amount: int
    client_name: str
    phone: str
    order_confirmation: bool


class OrderCreate(OrderBase):
    pass

class Order(OrderBase):

    id: int
    shop_id: int
    product_id: int

    deliveries: list[Delivery] = []

    class Config: 
        orm_mode = True






class ProductBase(BaseModel):

    product_name: str
    firm: str
    model: str
    tech_character: str
    price: int
    lifetime: date
    picture: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    orders: list[Order] = []

    class Config:

        orm_mode = True



class ShopBase(BaseModel):
    email: str
    delivery_charge: bool

class ShopCreate(ShopBase):
    pass

class Shop(ShopBase):
    id: int

    orders: list[Order] = []

    class Config:

        orm_mode = True

