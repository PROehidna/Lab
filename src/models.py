from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class BaseModel(Base):
    """
    Абстартный базовый класс, где описаны все поля и методы по умолчанию
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"# pragma: no cover


class Shop(BaseModel):
    __tablename__ = "shops"

    email = Column(String, unique=True, index=True)
    delivery_charge = Column(Boolean, default=True)

    order = relationship("Order", back_populates="shop")

class Product(BaseModel):
    __tablename__ = "products"

    product_name = Column(String, unique=True, index=True)
    firm = Column(String)
    model = Column(String)
    tech_character = Column(String)
    price = Column(Integer)
    lifetime = Column(DateTime)
    picture = Column(String)

    order = relationship("Order", back_populates="product")

class Order(BaseModel):
    __tablename__ = "orders"

    order_date = Column(DateTime)
    amount = Column(Integer)
    client_name = Column(String)
    phone = Column(String)
    order_confirmation = Column(Boolean, default=True)

    shop_id = Column(Integer, ForeignKey("shops.id"))
    product_id = Column(Integer, ForeignKey("products.id"))


    shop = relationship("Shop", back_populates="order")
    product = relationship("Product", back_populates="order")
    delivery = relationship("Delivery", back_populates="order")

class Delivery(BaseModel):
    __tablename__ = "deliveries"

    date_delivery = Column(DateTime)
    address = Column(String)
    client_name = Column(String)
    courier_name = Column(String)
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship("Order", back_populates="delivery")