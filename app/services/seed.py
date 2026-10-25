"""Reproducible synthetic demo-data generator."""
from datetime import date, timedelta
from decimal import Decimal
from random import Random

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Category, Customer, Order, OrderItem, Product

REGIONS = {
    "Gauteng": "Johannesburg", "Western Cape": "Cape Town", "KwaZulu-Natal": "Durban",
    "Eastern Cape": "Gqeberha", "Free State": "Bloemfontein", "Limpopo": "Polokwane",
}
CATALOGUE = [
    ("Electronics", "Wireless Headphones", 420, 799), ("Electronics", "Office Monitor", 2100, 3499),
    ("Office", "Ergonomic Chair", 1500, 2699), ("Office", "Notebook Set", 55, 119),
    ("Home", "Coffee Maker", 680, 1199), ("Home", "Desk Lamp", 190, 399),
]


def seed_demo_data(session: Session, order_total: int = 10_000) -> bool:
    """Seed deterministic synthetic data only when the database is empty."""
    if session.scalar(select(func.count()).select_from(Order)):
        return False
    rng = Random(20261025)
    categories = {}
    for index, name in enumerate(sorted({row[0] for row in CATALOGUE}), 1):
        categories[name] = Category(id=index, name=name)
    session.add_all(categories.values())
    products = []
    for index, (category, name, cost, price) in enumerate(CATALOGUE, 1):
        products.append(Product(id=index, name=name, category_id=categories[category].id, unit_cost=Decimal(str(cost)), unit_price=Decimal(str(price))))
    session.add_all(products)
    customers = []
    region_names = list(REGIONS)
    for index in range(1, 401):
        region = region_names[(index - 1) % len(region_names)]
        customers.append(Customer(id=index, name=f"Demo Customer {index:03d}", region=region, city=REGIONS[region], segment=("Enterprise" if index % 7 == 0 else "SMB"), created_date=date(2022, 1, 1) + timedelta(days=index)))
    session.add_all(customers)
    session.flush()
    start = date(2023, 1, 1)
    for order_id in range(1, order_total + 1):
        # Seasonal uplift creates realistic, discoverable variation without a preset narrative.
        offset = rng.randrange(0, 365 * 3)
        ordered_on = start + timedelta(days=offset)
        customer = customers[rng.randrange(len(customers))]
        order = Order(id=order_id, order_date=ordered_on, customer_id=customer.id, region=customer.region, status="Completed")
        session.add(order)
        for line in range(1 if rng.random() < .72 else 2):
            product = products[rng.choices(range(len(products)), weights=[27, 8, 13, 30, 10, 12])[0]]
            quantity = rng.randint(1, 3 if product.id in (2, 3) else 8)
            discount = Decimal("0.10") if rng.random() < .18 else Decimal("0")
            session.add(OrderItem(id=(order_id * 2) + line, order_id=order_id, product_id=product.id, quantity=quantity, unit_price=product.unit_price, discount=discount, unit_cost=product.unit_cost))
    session.commit()
    return True

