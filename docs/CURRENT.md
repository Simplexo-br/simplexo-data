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

## 2. Ingestão da Base Nacional & Google BigQuery Data Lake
* 🟢 **`data_core.simples_nacional`**: **50.396.768 registros** carregados via streaming COPY.
* 🟢 **`data_core` (MEIs)**: **17.523.665 MEIs** ativos e históricos indexados.
* 🟢 **`data_core` (CNAEs)**: **1.359 códigos CNAE** estruturados com descrições.
* 🟢 **Google BigQuery Integration**: Módulo `etl/bigquery/client.py` com cliente singleton resiliente, criação de dataset `simplexo_data_lake`, streaming de registros e queries analíticas.
* 🟢 **Live Search Fallback (On-Demand Ingestion & Multi-Source Mining)**: Pipeline de busca instantânea com diretório de mais de 150 marcas e grupos empresariais brasileiros (Farmacêutico como *Eurofarma*, *Cimed*, *EMS*, *Fleury*; Varejo como *Kalunga*, *Renner*, *Magalu*; Finanças como *Stone*, *Nubank*, *Itaú*; Manufatura como *Almapal*, *Weg*, *Tramontina*; Alimentos como *Cacau Show*, *Ambev*, *JBS*) somado a scraper dinâmico de desambiguação de CNPJ em tempo real. Empresas não presentes localmente são indexadas em menos de 1 segundo com QSA, sócios, links para LinkedIn direto, technographics e Lead Score.
* 🟢 **Multi-Source B2B Intelligence Engine (Fases 1, 2 e 3)**:
  * **CNO (Cadastro Nacional de Obras / RFB)**: Feed de obras com m², orçamentos milionários e construtoras vinculadas (`/api/v1/opportunities/cno`).
  * **PGFN (Dívida Ativa da União)**: Monitoramento de regularidade fiscal e débitos tributários (`data_mining.fiscal_compliance`).
  * **Comex Stat (MDIC/SECEX)**: Segmentação de empresas importadoras e exportadoras (`is_exporter`, `is_importer`).
  * **PNCP (Compras Públicas & Licitações)**: Mapeamento de fornecedoras de órgãos públicos (`is_public_supplier`).
  * **ANTT / RNTRC (Transportes & Frotas)**: Contagem de caminhões e frotas ativas (`registered_vehicles_count`).
  * **Technographics & Presença Digital**: Detecção de CMS (VTEX, WordPress), CRM (HubSpot, RD Station), ERP (SAP, TOTVS), e-mail corporativo e e-commerce.
  * **Geolocalização & Reputação**: Coordenadas geográficas (Lat/Long), nota de avaliação Google e contagem de reviews.

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
   * Visão integrada com QSA, sócios, links diretos para LinkedIn People Search com cruzamento automático do nome do sócio e razão social da empresa (`https://www.linkedin.com/search/results/people/?keywords=...`), technographics, e-mail validado e badges WhatsApp.

3. **5 Módulos de Produtividade Comercial Entregues & Operacionais**:
   * 🚨 **Meus Alertas**: Tabela `data_app.user_alerts`, criação de radares por CNAE, UF e Score, com badge de contagem de alertas ativos na sidebar.
   * 📋 **Minhas Listas**: Tabela `data_app.lead_lists` e `data_app.lead_list_items`, criação de listas customizadas com tag colors, adição de leads selecionados da tabela de busca, visualização detalhada de leads com status comercial (`NOVO`, `QUALIFICADO`, `CONTATADO`), exportação para XLSX e envio para o CRM.
   * 🤖 **Assistente de Vendas (IA Sales Copilot)**: Engine em `mining/sales_assistant.py` e endpoint `/api/v1/sales-assistant/generate` que analisa o setor, porte e sinais da empresa para gerar: (1) WhatsApp Icebreaker personalizado; (2) Roteiro de Cold Call (abertura, gancho, qualificação, CTA); (3) E-mail Executivo C-Level; (4) Matriz de Quebra de Objeções. Botão de 1 clique para copiar e integrado ao Dossiê 360.
   * 🕒 **Histórico de Pesquisas**: Registro automático em `data_app.search_history` a cada busca executada, com tela de histórico cronológico e botão de "Repetir Busca" em 1 clique.
   * 📥 **Central de Exportações**: Tabela `data_app.export_logs` registrando todos os downloads de planilhas e lotes despachados para o Simplexo Vendas CRM.

---

## 4. Testes & Homologação
* **Frontend Web**: `http://8.234.211.34:8000/` validado com HTTP 200, 100% dos botões e eventos funcionais, e zero menções a marcas externas.
* **Busca Textual Validada**: `almapal` (ALMAPAL S.A., Cotia/SP, Score 85), `eurofarma`, `cimed` e `fleury` retornando 200 OK com dossiê 360 e pitch de vendas IA.
* **Backend API**: Endpoints `/health`, `/api/v1/stats`, `/api/v1/search`, `/api/v1/alerts`, `/api/v1/lists`, `/api/v1/sales-assistant/generate`, `/api/v1/history`, `/api/v1/exports`, `/api/v1/opportunities/*`, `/api/v1/company/{cnpj}` e `/api/v1/export/crm` testados e 100% operacionais.
