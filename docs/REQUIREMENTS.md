# Requirements Baseline

## Funcionais

1. Pesquisar por identificação, nome, CNAE, localização, situação, porte e enriquecimentos.
2. Salvar segmentos/listas tenant-owned.
3. Exibir Company 360 com provenance, quality, freshness e divergências.
4. Promover seleção explícita a prospect e depois parceiro/CRM com idempotência/deduplicação.
5. Enriquecer por waterfall observável.
6. Medir ICP/scoring comercial e feedback de conversão, com explicabilidade.
7. API tenant-aware com entitlement, quota, wallet/créditos e auditoria.
8. Planos, assinatura, checkout, provisioning e onboarding reutilizando Odoo/OCA.

## Não funcionais

Isolamento deny-by-default; sem hardcodes/secrets; histórico/provenance; busca paginada e limitada; idempotência/retry/circuit breaker/DLQ; observabilidade; acessibilidade e pt-BR; LGPD by design.

P95, volume, RPO/RTO, disponibilidade, freshness, qualidade e orçamento por tenant ainda precisam de metas aprovadas.
