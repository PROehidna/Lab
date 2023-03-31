from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_base.db"  # Тестовая БД

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_create_shop():
    response = client.post(
        "/shops/",
        json={"email": "test@mail.com", "delivery_charge": True}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@mail.com"

def test_create_exist_shop():
    response = client.post(
        "/shops/",
        json={"email": "test@mail.com", "delivery_charge": True}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Shop email is already exist"

def test_read_shops():
    response = client.get("/shops/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["email"] == "test@mail.com"

def test_get_shop_by_id():
    response = client.get("/shops/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@mail.com"

def test_shop_not_found():
    response = client.get("/shops/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Shop not found"



def test_add_order_to_delivery():
    response = client.post(
        "/orders/1/deliveries/",
        json={"date_delivery": "1970-01-01", "address": "Улица Тестов", "client_name": "Тейлор Тестов", "courier_name": "Тестовый курьер"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["date_delivery"] == "1970-01-01"
    assert data["address"] == "Улица Тестов"
    assert data["client_name"] == "Тейлор Тестов"
    assert data["courier_name"] == "Тестовый курьер"
    assert data["order_id"] == 1


def test_get_deliveries():
    response = client.get("/deliveries/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["date_delivery"] == "1970-01-01"
    assert data[0]["address"] == "Улица Тестов"
    assert data[0]["client_name"] == "Тейлор Тестов"
    assert data[0]["courier_name"] == "Тестовый курьер"
    assert data[0]["order_id"] == 1


    
def test_get_delivery_by_id():
    response = client.get("/deliveries/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["address"] == "Улица Тестов"

def test_delivery_not_found():
    response = client.get("/deliveries/3")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Delivery not found"

def test_create_exist_delivery_order():
    response = client.post(
        "/orders/1/deliveries/",
        json={"date_delivery": "1970-01-01", "address": "Улица Тестов", "client_name": "Тейлор Тестов", "courier_name": "Тестовый курьер"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Delivery order id already exist"



def test_create_product():
    response = client.post(
        "/products/",
        json={"product_name": "Тестовый продукт", "firm": "Тестовая фирма", "model": "Тестовая модель", "tech_character" : "Тестовые характеристики", "price": 1000, "lifetime": "2022-11-11", "picture": "test.png"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "Тестовый продукт"


def test_get_product():
    response = client.get("/products/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["product_name"] == "Тестовый продукт"


def test_get_product_by_id():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/products/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["product_name"] == "Тестовый продукт"

def test_product_not_found():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/products/3")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Product not found"

def test_create_exist_product():
    response = client.post(
        "/products/",
        json={"product_name": "Тестовый продукт", "firm": "Тестовая фирма", "model": "Тестовая модель", "tech_character" : "Тестовые характеристики", "price": 1000, "lifetime": "2022-11-11", "picture": "test.png"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Product name is already exist"


def test_add_order_to_product_shop():
    response = client.post(
        "/products/1/orders/1/",
        json={
            "order_date": "1970-01-01", 
            "amount": 1, 
            "client_name": "Тейлор Тестов", 
            "phone": "111222333", 
            "order_confirmation": True, 
            "product_id": 1,
            "shop_id": 1
    }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["order_date"] == "1970-01-01"
    assert data["amount"] == 1
    assert data["client_name"] == "Тейлор Тестов"
    assert data["phone"] == "111222333"
    assert data["order_confirmation"] == True
    assert data["product_id"] == 1
    assert data["shop_id"] == 1


def test_get_order_by_id():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/orders/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["amount"] == 1

def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["amount"] == 1

def test_order_not_found():
    response = client.get("/orders/3")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Order not found"
