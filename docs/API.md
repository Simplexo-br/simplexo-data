# API Baseline

HTTPS versionada atrás do Data Gateway: schemas tipados, cursor pagination, filtros allowlisted, idempotency em mutações, erros padronizados e correlation IDs. Autenticação identifica instalação/tenant; autorização verifica escopo, entitlement e ownership. Rate limit por tenant/credencial/operação. OpenAPI deriva da implementação. Bulk/long-running vira job. Provider internals/credentials nunca são expostos.
