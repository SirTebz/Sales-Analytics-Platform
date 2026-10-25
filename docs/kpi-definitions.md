# KPI definitions

All dashboard KPI calculations use completed order items within the selected order-date range.

| KPI | Formula | Interpretation / limitation |
|---|---|---|
| Revenue | `SUM(quantity × unit price × (1 - discount))` | Net transactional sales in ZAR. |
| Cost | `SUM(quantity × unit cost)` | Historical line-item cost. |
| Profit | `Revenue - Cost` | Gross profit; excludes overheads and tax. |
| Profit margin | `Profit / Revenue × 100` | Returns 0 when revenue is zero. |
| Average order value | `Revenue / orders` | Unavailable when no orders exist. |

