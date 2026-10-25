from decimal import Decimal
from types import SimpleNamespace

from app.analytics.kpis import calculate_kpis


def test_calculates_authoritative_kpis():
    items = [SimpleNamespace(quantity=2, unit_price=Decimal("100"), discount=Decimal("0.1"), unit_cost=Decimal("55"))]
    actual = calculate_kpis(items, order_count=1, customers=1, products=1)
    assert actual["revenue"] == 180.0
    assert actual["cost"] == 110.0
    assert actual["profit"] == 70.0
    assert round(actual["profit_margin"], 2) == 38.89
    assert actual["average_order_value"] == 180.0

