# ADR-004: BigQuery for analytics, not OLTP

**Status:** Proposed — 2026-08-30

BigQuery recebe histórico/analytics; PostgreSQL serve busca/360/controle e GCS preserva fontes. Evita scans analíticos imprevisíveis na request path.
