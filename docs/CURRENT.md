# CURRENT.md — Status do Projeto Simplexo Data

**Data:** 17/09/2026  
**Status Geral:** ✅ **Stack 3.0 Enterprise: Stone Station (B2B/B2C), DataFlow™ Waterfall, DatAService & Simplexo Reveal (Intent Data)**

---

## 1. Infraestrutura e VM Dedicada (8.234.211.34)
* **Host:** GCP Compute Engine simplexo-data-mining (us-east4-a).
* **Disco:** 250 GB (partição /dev/sda1 operando com folga).
* **Swap:** 8 GB ativo.
* **Containers Ativos & Saudáveis:**
  * simplexo_postgres (PostgreSQL 16 com pg_trgm, unaccent, uuid-ossp)
  * simplexo_redis (Redis 7)
  * simplexo_gateway (FastAPI REST Gateway v3.0 na porta 8000)
  * simplexo_mining_worker (Worker de Mineração, Technographics e Lead Scoring)
* **URL de Produção:** http://8.234.211.34:8000/ (HTTP 200 OK — 100% Operacional)

---

## 2. Simplexo Data Suite 3.0 Entregue

1. **Stone Station (B2B & B2C)**:
   - Motor B2B com +40 filtros de ICP corporativo (`POST /api/v1/stonestation/search/b2b`).
   - Motor B2C com +70 critérios para sócios, administradores e decisores (`POST /api/v1/stonestation/search/b2c`).
   - Gestor de créditos de consulta e extrato em tempo real (`GET /api/v1/stonestation/credits/balance`).

2. **DataFlow™ Waterfall Enrichment**:
   - Enriquecimento em cascata determinística L1 (Redis Cache) -> L2 (PostgreSQL Data Plane) -> L3 (BigQuery/RFB Live) -> L4 (DNS/MX Resolver) -> L5 (Google X-Ray / QSA Decisors) com latência total em milissegundos (`GET /api/v1/enrich/dataflow/{cnpj}`).

3. **DatAService & Batch Sanitizer**:
   - Higienização de bases CSV em lote com deduplicação e cálculo de Score de Assertividade Cadastral e Localização (0 a 100) sem avaliação de risco de crédito (`POST /api/v1/dataservice/sanitize`).

4. **Simplexo Reveal (Pixel & Intent Data)**:
   - Identificador em tempo real de visitantes com Reverse IP e ASN, scoring de intenção de compra B2B (0 a 100) e exportação em 1 clique para o Simplexo Vendas CRM (`GET /api/v1/reveal/feed` e `GET /api/v1/reveal/snippet`).

---

## 3. Ingestão da Base Nacional & Google BigQuery Data Lake
* data_core.simples_nacional: 50.396.768 registros carregados via streaming COPY.
* data_core (MEIs): 17.523.665 MEIs ativos e históricos indexados.
* data_core (CNAEs): 1.359 códigos CNAE estruturados com descrições e catálogo de 14 macro-segmentos econômicos.
* Multi-CNAE & Macro-Segment Filtering: Suporte completo a tags/chips múltiplos de CNAE e seleção de verticais econômicas na busca e no Stone Station B2B.
* Google BigQuery Integration: Dataset simplexo_data_lake conectado e resiliente.
* CNO (Obras Civis), PGFN (Dívida Ativa), Comex Stat, PNCP (Licitações) e ANTT (Frotas) 100% integrados.
