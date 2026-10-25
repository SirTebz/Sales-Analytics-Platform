from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column("CustomerID", primary_key=True)
    name: Mapped[str] = mapped_column("CustomerName", String(120), unique=True)
    region: Mapped[str] = mapped_column("Region", String(50), index=True)
    city: Mapped[str] = mapped_column("City", String(80))
    segment: Mapped[str] = mapped_column("CustomerSegment", String(30))
    created_date: Mapped[date] = mapped_column("CreatedDate", Date)
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column("CategoryID", primary_key=True)
    name: Mapped[str] = mapped_column("CategoryName", String(80), unique=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column("ProductID", primary_key=True)
    name: Mapped[str] = mapped_column("ProductName", String(120), unique=True)
    category_id: Mapped[int] = mapped_column("CategoryID", ForeignKey("categories.CategoryID"), index=True)
    unit_cost: Mapped[Decimal] = mapped_column("UnitCost", Numeric(12, 2))
    unit_price: Mapped[Decimal] = mapped_column("UnitPrice", Numeric(12, 2))
    category: Mapped[Category] = relationship(back_populates="products")


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column("OrderID", primary_key=True)
    order_date: Mapped[date] = mapped_column("OrderDate", Date, index=True)
    customer_id: Mapped[int] = mapped_column("CustomerID", ForeignKey("customers.CustomerID"), index=True)
    region: Mapped[str] = mapped_column("Region", String(50), index=True)
    status: Mapped[str] = mapped_column("OrderStatus", String(30))
    customer: Mapped[Customer] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column("OrderItemID", primary_key=True)
    order_id: Mapped[int] = mapped_column("OrderID", ForeignKey("orders.OrderID"), index=True)
    product_id: Mapped[int] = mapped_column("ProductID", ForeignKey("products.ProductID"), index=True)
    quantity: Mapped[int] = mapped_column("Quantity", Integer)
    unit_price: Mapped[Decimal] = mapped_column("UnitPrice", Numeric(12, 2))
    discount: Mapped[Decimal] = mapped_column("Discount", Numeric(5, 4))
    unit_cost: Mapped[Decimal] = mapped_column("UnitCost", Numeric(12, 2))
    order: Mapped[Order] = relationship(back_populates="items")
    product: Mapped[Product] = relationship()

