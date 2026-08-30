# Data Architecture

- **Raw/GCS:** objetos imutáveis, manifest, checksum, aquisição e termos/licença.
- **Validated:** schema/semântica, parser e quarentena.
- **Canonical/PostgreSQL:** empresa, estabelecimento, regimes, CNAE, sócios e dimensões como observações históricas.
- **Serving/PostgreSQL:** projeções de busca, Company 360 e resumos de qualidade/freshness.
- **BigQuery:** histórico curado, cohorts, market sizing, qualidade e features.

Toda observação registra fonte/ID, `observed_at`, `ingested_at`, validade, raw URI/checksum, parser/schema, lineage, confiança e classificação jurídica.

Pipeline: descobrir -> baixar para objeto único -> verificar -> registrar batch -> parse streaming -> validar/quarentenar -> merge idempotente -> projeções -> métricas. Raw nunca é sobrescrito. CNPJ é string normalizada preparada para transição alfanumérica; formatação é separada. Conflitos permanecem observações, não overwrite silencioso.
