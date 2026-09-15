# CURRENT.md — Status do Projeto Simplexo Data

**Data:** 15/09/2026  
**Status Geral:** ✅ **Stack 2.0 Completa, 50.39M Registros Nacionais e Todas as 5 Features Avançadas Operacionais e Testadas**

---

## 1. Infraestrutura e VM Dedicada (`8.234.211.34`)
* **Host:** GCP Compute Engine `simplexo-data-mining` (`us-east4-a`).
* **Disco:** 250 GB (partição `/dev/sda1` redimensionada e operando com folga).
* **Swap:** 8 GB ativo.
* **Containers Ativos & Saudáveis:**
  * `simplexo_postgres` (PostgreSQL 16 com `pg_trgm`, `unaccent`, `uuid-ossp`)
  * `simplexo_redis` (Redis 7)
  * `simplexo_gateway` (FastAPI REST Gateway v2.0 na porta 8000)
  * `simplexo_mining_worker` (Worker 2.0 de Mineração, Technographics e Lead Scoring)

---

## 2. Ingestão da Base Nacional
* 🟢 **`data_core.simples_nacional`**: **50.396.768 registros** carregados via streaming COPY.
* 🟢 **`data_core` (MEIs)**: **17.523.665 MEIs** ativos e históricos indexados.
* 🟢 **`data_core` (CNAEs)**: **1.359 códigos CNAE** estruturados com descrições.
* 🟢 **Pipeline RFB WebDAV**: Mapeamento e download automatizado do lote mensal `2026-09` oficial da Receita Federal.

---

## 3. Módulos Avançados de Inteligência B2B Implementados

1. **Detecção de Tecnologias (Technographics)** (`mining/technographics.py`):
   * Mapeamento automatizado de ERPs (*TOTVS, SAP, Senior, Linx, Sankhya, Omie, Tiny, Bling, Odoo*), E-commerces (*VTEX, Shopify, Nuvemshop, WooCommerce, Magento*) e CRMs (*RD Station, HubSpot, ActiveCampaign, Salesforce*).
2. **Inferência de Faturamento Estimado & Faixa de Funcionários** (`mining/estimator.py`):
   * Modelagem estatística combinando porte RFB, capital social, CNAE e enquadramento Simples Nacional.
3. **Localizador de Decisores & Validador de E-mails com DNS MX** (`mining/decisors.py` e `mining/email_validator.py`):
   * Cruzamento de QSA com cargos executivos, inferência de padrões de e-mail corporativo e checagem de registros MX sem envio de mensagens.
4. **Módulo de Enriquecimento em Lote (Batch CSV API)** (`POST /api/v1/enrich/batch`):
   * Upload de planilhas CSV com CNPJs para qualificação e enriquecimento instantâneo.
5. **Simplexo Reveal (B2B Website De-anonymization)** (`gateway/app/reveal.py`):
   * Script JavaScript leve (`/api/v1/reveal/pixel.js`) e endpoint de resolução reversa (`/api/v1/reveal/identify`) para identificação de empresas visitantes.

---

## 4. Testes & Homologação
* **Testes unitários**: `python -m tests.test_features` executado e aprovado com 100% de sucesso.
* **Testes na VM**: Endpoints `/health`, `/api/v1/stats`, `/api/v1/search`, `/api/v1/company/{cnpj}`, `/api/v1/enrich/batch` e `/api/v1/reveal/pixel.js` validados via curl e HTTP live.
