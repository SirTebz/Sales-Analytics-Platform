from collections.abc import Iterable
from decimal import Decimal


ZERO = Decimal("0")


def calculate_kpis(items: Iterable[object], order_count: int, customers: int, products: int) -> dict[str, float | int | None]:
    """Calculate the platform's authoritative KPI definitions from order items."""
    materialized = list(items)
    revenue = sum((Decimal(item.quantity) * item.unit_price * (Decimal("1") - item.discount) for item in materialized), ZERO)
    cost = sum((Decimal(item.quantity) * item.unit_cost for item in materialized), ZERO)
    profit = revenue - cost
    units = sum(item.quantity for item in materialized)
    return {
        "revenue": float(revenue),
        "cost": float(cost),
        "profit": float(profit),
        "profit_margin": float((profit / revenue * 100) if revenue else ZERO),
        "orders": order_count,
        "units_sold": units,
        "average_order_value": float(revenue / order_count) if order_count else None,
        "customers": customers,
        "products": products,
    }

