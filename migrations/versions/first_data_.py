"""empty message

Revision ID: first_data
Revises: 2c022b2c8f99
Create Date: 2022-11-27 02:10:35.765949

"""
from alembic import op
# import sqlalchemy as sa
from src.models import Delivery, Product, Shop, Order
from sqlalchemy import orm
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = '2c022b2c8f99'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    shop1 = Shop(email="famous@gmail.com", delivery_charge=True)
    shop2 = Shop(email="cheap@gmail.com", delivery_charge=False)
    session.add_all([shop1, shop2])
    session.flush()

    product1 = Product(product_name='Утюг', firm='Panasonic', model="2022 года", tech_character="1200 – 1500 Вт", price=10000, lifetime=datetime(2025, 1, 10, 10, 10), picture="flaitroin.jpg")
    product2 = Product(product_name='Электрочайник', firm='Samsung', model="2000 года", tech_character="Комфорки 3", price=1500, lifetime=datetime(2022, 6, 10, 10, 10), picture="electric.jpg")
    product3 = Product(product_name='Холодильник', firm='Bosh', model="New ver 2.0", tech_character="Красивый и объёмный", price=20000, lifetime=datetime(2030, 1, 10, 10, 10), picture="fridge.jpg")
    product4 = Product(product_name='Плита', firm='Philips', model="Future boom", tech_character="4 комфорки", price=4500, lifetime=datetime(2024, 1, 10, 10, 10), picture="oven.jpg")
    
    session.add_all([product1, product2, product3, product4])
    session.flush()

    order1 = Order(order_date=datetime(2022, 9, 10, 12, 30), amount=1, client_name ="Сергей Орлов", phone="909122", order_confirmation=True, product_id=product3.id, shop_id=shop2.id)
    order2 = Order(order_date=datetime(2023, 10, 5, 11), amount=2, client_name ="Никита Гришин", phone="122112", order_confirmation=False, product_id=product2.id, shop_id=shop1.id)
    order3 = Order(order_date=datetime(2018, 1, 10, 6, 10), amount=5, client_name ="Антон Гаранин", phone="551242", order_confirmation=True, product_id=product4.id, shop_id=shop1.id)
    order4 = Order(order_date=datetime(2015, 12, 30, 12, 30), amount=10, client_name ="Алексей Тестов", phone="11111", order_confirmation=False, product_id=product1.id, shop_id=shop2.id)
    

    session.add_all([order1, order2, order3, order4])
    session.commit()

    delivery1 = Delivery(date_delivery=datetime(2022,10,10,12,10), address="Улица Тещина 11", client_name="Яков Шишин", courier_name="Мария Янова", order_id=order1.id)
    delivery2 = Delivery(date_delivery=datetime(2018,2,10,12,10), address="Улица Минина 22", client_name="Яков Шишин", courier_name="Мария Янова", order_id=order3.id)
    delivery3 = Delivery(date_delivery=datetime(2016,10,10,12,10), address="Улица Громова 40", client_name="Яков Шишин", courier_name="Мария Янова", order_id=order4.id)
    delivery4 = Delivery(date_delivery=datetime(2023,11,10,12,10), address="Улица Широкова 1", client_name="Яков Шишин", courier_name="Мария Янова", order_id=order2.id)


    session.add_all([delivery1, delivery2, delivery3, delivery4])
    session.commit()


def downgrade() -> None:
    pass