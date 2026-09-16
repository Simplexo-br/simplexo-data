# CURRENT.md — Status do Projeto Simplexo Data

**Data:** 15/09/2026  
**Status Geral:** ✅ **Stack 2.0 Completa, Interface Light Moderna Inspirada na Data Stone, 50.39M Registros Nacionais e Todas as Features Operacionais**

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
* **URL de Produção:** `http://8.234.211.34:8000/` (HTTP 200 OK)

---

## 2. Ingestão da Base Nacional
* 🟢 **`data_core.simples_nacional`**: **50.396.768 registros** carregados via streaming COPY.
* 🟢 **`data_core` (MEIs)**: **17.523.665 MEIs** ativos e históricos indexados.
* 🟢 **`data_core` (CNAEs)**: **1.359 códigos CNAE** estruturados com descrições.
* 🟢 **Pipeline RFB WebDAV**: Mapeamento e download automatizado do lote mensal `2026-09` oficial da Receita Federal.

---

## 3. Módulos & Interface Visual Data Stone 2.0

1. **Design System Claro & Moderno (Benchmark Data Stone / Oportunidados)**:
   * Interface Enterprise em Modo Claro (`#F8FAFC`, cartões `#FFFFFF` com bordas sutis `#E2E8F0`, tipografia *Plus Jakarta Sans* e contrastes `#0F172A`).
   * Omnibar de busca global (`Ctrl + K`) com atalhos por setor (Software, Transportes, Saúde, Alimentos, Construção).
   * Dashboards analíticos em tempo real com gráficos Chart.js (Distribuição Geográfica e Faixa de Faturamento).
2. **5 Planos Comerciais de Assinatura & Cotas de Exportação**:
   * *Bronze* (500 leads), *Prata* (2.000 leads), *Ouro* (6.000 leads), *Diamante* (15.000 leads) e *Black Enterprise* (ilimitado/personalizado).
   * Ciclos Mensal e Anual (33% OFF + dobro de cotas no anual) com modal de checkout integrado e gestão de créditos.
3. **Radar de Oportunidades Recentes & Obras CNO**:
   * Monitoramento de novas aberturas nos últimos 30 dias com botão de qualificação instantânea.
   * Feeds de Obras CNO com valor de investimento estimado, área em m² e atalho direto para WhatsApp do responsável.
4. **Exportação & Conexão Simplexo Vendas / CRM**:
   * Exportação seletiva de leads para o funil comercial do Simplexo Vendas e downloads diretos em CSV/Excel.
5. **Dossiê Company 360 Slide-over**:
   * Visão integrada com QSA, sócios, links para LinkedIn, technographics, e-mail validado e badges WhatsApp.

---

## 4. Testes & Homologação
* **Frontend Web**: `http://8.234.211.34:8000/` validado com HTTP 200, 100% dos botões e eventos funcionais, e zero menções a marcas externas.
* **Backend API**: Endpoints `/health`, `/api/v1/stats`, `/api/v1/search`, `/api/v1/plans`, `/api/v1/dashboard/charts`, `/api/v1/opportunities/*`, `/api/v1/company/{cnpj}` e `/api/v1/export/crm` testados e operacionais.
