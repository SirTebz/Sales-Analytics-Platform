from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.analytics.kpis import calculate_kpis
from app.database import Base, SessionLocal, engine
from app.models import Customer, Order, OrderItem, Product
from app.services.seed import seed_demo_data

ROOT_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="Sales Analytics Platform", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT_DIR / "frontend"), name="static")


def get_session():
    with SessionLocal() as session:
        yield session


@app.on_event("startup")
def initialise_application() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        seed_demo_data(session)


@app.get("/", include_in_schema=False)
def dashboard_page():
    return FileResponse(ROOT_DIR / "frontend" / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "dataset": "Synthetic Demo Sales Dataset"}


@app.get("/api/dashboard/summary")
def dashboard_summary(start_date: date | None = None, end_date: date | None = None, session: Session = Depends(get_session)):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=422, detail="start_date must not be after end_date")
    statement = select(OrderItem).join(Order)
    order_statement = select(Order)
    if start_date:
        statement = statement.where(Order.order_date >= start_date)
        order_statement = order_statement.where(Order.order_date >= start_date)
    if end_date:
        statement = statement.where(Order.order_date <= end_date)
        order_statement = order_statement.where(Order.order_date <= end_date)
    items = session.scalars(statement).all()
    orders = session.scalars(order_statement).all()
    customer_count = len({order.customer_id for order in orders})
    product_count = len({item.product_id for item in items})
    return {"dataset": "Synthetic Demo Sales Dataset", "filters": {"start_date": start_date, "end_date": end_date}, "kpis": calculate_kpis(items, len(orders), customer_count, product_count)}


@app.get("/api/sales/trends")
def sales_trends(session: Session = Depends(get_session)):
    rows = session.execute(select(Order.order_date, OrderItem.quantity, OrderItem.unit_price, OrderItem.unit_cost, OrderItem.discount).join(OrderItem).order_by(Order.order_date)).all()
    monthly: dict[str, dict[str, float | int]] = {}
    for ordered_on, quantity, unit_price, unit_cost, discount in rows:
        period = ordered_on.strftime("%Y-%m")
        bucket = monthly.setdefault(period, {"period": period, "revenue": 0.0, "profit": 0.0, "units": 0})
        revenue = float(quantity * unit_price * (1 - discount))
        bucket["revenue"] += revenue
        bucket["profit"] += revenue - float(quantity * unit_cost)
        bucket["units"] += quantity
    return list(monthly.values())

