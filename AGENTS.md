# AGENTS.md — Simplexo Data

Antes de qualquer tarefa, leia este arquivo, `.simplexo/state.yaml` e `docs/CURRENT.md`; recupere branch, commit, PRs, issues, CI e Project #13. Não apague/reestruture trabalho existente sem auditoria.

## Objetivo e limites

Pesquisar, analisar, segmentar, enriquecer e qualificar empresas brasileiras, promovendo seleções explícitas a prospects/CRM. Não é banco de listas, CRM/BI/filas/API paralelos. Odoo 18 Community é o Application Plane; PostgreSQL dedicado, GCS e BigQuery formam o Data Plane central; Simplexo Intelligence é o Intelligence Plane. A base nacional nunca deve ser replicada em Odoo ou convertida em `res.partner`.

**Simplexo Score é outro produto.** É proibido criar módulos de score de crédito/risco neste repositório.

## OCA-FIRST

Antes de implementar: verificar Odoo Core 18, OCA 18.0 e código Simplexo; documentar gap em `docs/OCA_REUSE_MATRIX.md`. Não alterar Core. Reusar capacidades mantidas quando atenderem ao gap.

## Segurança, tenancy e dados

Nunca fixar database, `company_id`, `user_id`, domínio, URL, IP, tenant, credencial, API key, servidor ou caminho. Secrets fora do Git. Objetos tenant-owned exigem ownership explícito, regras deny-by-default e testes negativos. Não confiar em `sudo()` para fluxos tenant-facing.

Preservar valor bruto/normalizado, fonte, licença/termos, timestamps, parser, confiança e freshness. IA não transforma inferência em fato. Providers usam contrato comum, timeout, rate limit, cache, circuit breaker, observabilidade e waterfall determinístico. Uso produtivo depende de validação jurídica/técnica.

LGPD by design: minimização, finalidade, retenção, rastreabilidade, direitos do titular e avaliação de base legal.

## Entrega

Não declarar pronto/testado/CI/screenshot/homologado sem evidência real. Em UI, aguardar aprovação humana para `VISUAL_APPROVED`. Em cada checkpoint atualize `CURRENT.md`, `state.yaml`, changelog, issue/Project e evidências; registre implementado, pendente, testes/resultados, commit/PR/CI, bloqueios, riscos e `next_action`.
