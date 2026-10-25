# Sales Analytics Platform

An interactive sales-performance dashboard built as a Junior Data Analyst portfolio project. It uses a clearly labelled **Synthetic Demo Sales Dataset**, generated reproducibly with 10,000 transactions across three years.

## Initial phase: runnable analytics foundation

This checkpoint provides a database-backed FastAPI application, an accessible dashboard with dynamic KPIs and monthly trend data, a normalised data model, deterministic synthetic seeding, and focused automated tests. The next phases will add the import/validation workflow, deeper product/customer/region analysis, exports, data quality, insights, and Power BI guidance.

## Stack

Python, FastAPI, SQLAlchemy, Pandas, Pytest, HTML/CSS/JavaScript. SQL Server is the production schema target; the app automatically uses SQLite locally when `DATABASE_URL` is blank, enabling an immediate demo without credentials.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`. On first start the app creates `data/sales_analytics.db` and seeds the synthetic data.

## Test

```powershell
pytest
```

## SQL Server setup

Run `database/schema.sql` against SQL Server, then set `DATABASE_URL` in `.env` to a SQLAlchemy SQL Server connection URL. A SQL Server seed importer will be added alongside the ingestion workflow.

## KPI definitions

See [docs/kpi-definitions.md](docs/kpi-definitions.md).
