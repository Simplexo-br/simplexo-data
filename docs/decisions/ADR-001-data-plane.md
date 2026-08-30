# ADR-001: Central national data plane

**Status:** Proposed — 2026-08-30

Bulk/raw/canônico ficam em GCS/PostgreSQL/BigQuery centrais e são expostos pelo gateway, evitando duplicação/freshness divergente em Odoo. Trade-off: dependência de disponibilidade/latência e maior obrigação de segurança/FinOps central.
