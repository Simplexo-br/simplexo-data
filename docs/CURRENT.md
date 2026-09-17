# CURRENT.md — Status do Projeto Simplexo Data

**Data:** 17/09/2026  
**Status Geral:** ✅ **Stack 2.4 Enterprise: Extensão Chrome Copilot (Manifest V3), Deduplicação & Supressão de Listas (Anti-churn) e Grafo Interativo de Grupo Econômico & QSA**

---

## 1. Infraestrutura e VM Dedicada (8.234.211.34)
* **Host:** GCP Compute Engine simplexo-data-mining (us-east4-a).
* **Disco:** 250 GB (partição /dev/sda1 operando com folga).
* **Swap:** 8 GB ativo.
* **Containers Ativos & Saudáveis:**
  * simplexo_postgres (PostgreSQL 16 com pg_trgm, unaccent, uuid-ossp)
  * simplexo_redis (Redis 7)
  * simplexo_gateway (FastAPI REST Gateway v2.4 na porta 8000)
  * simplexo_mining_worker (Worker de Mineração, Technographics e Lead Scoring)
* **URL de Produção:** http://8.234.211.34:8000/ (HTTP 200 OK — 100% Operacional)

---

## 2. As 3 Fases de Inovação Entregues

1. **Fase 1: Extensão Google Chrome (Simplexo Web Copilot)**:
   - Pacote Manifest V3 em extensions/chrome_copilot/ (manifest.json, popup.html, popup.js, content.js, background.js, icons/).
   - Detecção em tempo real de CNPJs em websites institucionais e perfis corporativos do LinkedIn.
   - Pop-up com enriquecimento 360, faturamento presumido, decisores do QSA com links diretos para LinkedIn e botões WhatsApp (wa.me).
   - Exportação direta de leads para o Simplexo Vendas CRM em 1 clique via /api/v1/export/crm/direct.
   - Endpoint de download automático do pacote .zip em /api/v1/extension/download e nova tela explicativa na barra lateral.

2. **Fase 2: Deduplicação & Supressão de Listas (Anti-churn)**:
   - Tabela data_app.suppression_lists e endpoints /api/v1/suppression/list, /api/v1/suppression/upload, /api/v1/suppression/{id} e /api/v1/suppression/clear.
   - Upload de planilhas CSV com deduplicação e normalização automática de CNPJs e domínios.
   - Switch ativo de proteção anti-churn no painel de busca avançada que omite clientes existentes tanto nas pesquisas quanto nas exportações.

3. **Fase 3: Grafo Visual de Grupo Econômico & QSA (Network Graph)**:
   - Endpoint /api/v1/company/{cnpj}/network-graph gerando nós e arestas conectados com categorização visual (Matriz, Sócios Administradores, Filiais Operacionais e Holdings Coligadas).
   - Renderizador em HTML5 Canvas interativo no modal Dossiê 360 com nós coloridos, atualização em tempo real, física de posições e suporte a navegação por nós.

---

## 3. Ingestão da Base Nacional & Google BigQuery Data Lake
* data_core.simples_nacional: 50.396.768 registros carregados via streaming COPY.
* data_core (MEIs): 17.523.665 MEIs ativos e históricos indexados.
* data_core (CNAEs): 1.359 códigos CNAE estruturados com descrições.
* Google BigQuery Integration: Dataset simplexo_data_lake conectado e resiliente.
* CNO (Obras Civis), PGFN (Dívida Ativa), Comex Stat, PNCP (Licitações) e ANTT (Frotas) 100% integrados.
