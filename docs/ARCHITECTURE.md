# Architecture

```text
Sources -> GCS raw -> validation -> PostgreSQL canonical/serving
                     \-----------> BigQuery history/analytics
Odoo installations -> Data Gateway -> auth/policy -> search/360/enrichment
Odoo: lists/prospects/CRM/commerce     Data: provenance/quality/freshness
Simplexo Intelligence -> governed views -> labeled insights
```

O gateway é a única fronteira pública da base nacional. Odoo guarda referências, artefatos do usuário e registros promovidos, não o corpus. BigQuery é analítico, nunca caminho OLTP síncrono; PostgreSQL serve entidades/busca; GCS é landing/archive imutável.

Cada requisição carrega tenant, instalação, ator, correlation ID e entitlements. O gateway autentica, autoriza, mede, limita e audita. Promoção usa chave idempotente `(tenant, source_company_id, target_type)` e registra versão do snapshot.

Começar modular, separando deployables somente com evidência de escala/segurança. Reusar primitivas gerenciadas/OCA em vez de criar filas ou frameworks.
