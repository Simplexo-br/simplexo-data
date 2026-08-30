# Conceptual Data Model

| Aggregate | Purpose | Ownership |
|---|---|---|
| Company / Establishment | identidade legal e unidades | global data plane |
| Observation / SourceBatch | fato com fonte/tempo e artefato | global data plane |
| ProviderResult | resultado bruto/normalizado | tenant-aware data plane |
| SavedSearch / Segment / List | critérios e seleções | tenant/application |
| Prospect / Promotion | snapshot e linhagem a partner/lead | tenant/application |
| Entitlement / WalletEntry | acesso e ledger imutável | tenant/application |
| ConversionFeedback | resultado comercial | tenant/application |

IDs são strings opacas e não codificam database/company/domínio. Tabelas tenant-owned possuem ownership imutável e índices de autorização. Fatos e inferências são tipos distintos.
