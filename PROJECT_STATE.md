# PROJECT_STATE

## Identidade

- Objetivo: plataforma brasileira B2B de Data Intelligence e Sales Intelligence integrada ao Odoo.
- Escopo atual: Fase 0 — discovery e arquitetura; nenhum addon/serviço implementado.
- Stack: Odoo 18 Community; PostgreSQL, GCS e BigQuery; Simplexo Intelligence.
- Repositório: `Simplexo-br/simplexo-data`; branch base `main`.
- Operação: CTEP permanente; detalhes em [governança](docs/GOVERNANCE.md).

## Estado atual

- Entrega em andamento: revisão e gate da arquitetura da Fase 0.
- Branch de migração CTEP: `chore/ctep-governance`.
- Baseline técnica: commits `016c113` e `af8442c`.
- Project #13: acessível, 15 itens, issues #1–#15 vinculadas, todos em `Todo` na última verificação.
- Drive oficial: acessível e vazio na última verificação.
- CI: workflows criados, mas runners não iniciam por billing/spending limit do GitHub.
- PRs: nenhum antes desta migração.

## Bloqueios e gates

- Blocker externo: corrigir billing/spending de GitHub Actions e rerodar CI.
- Gate humano: revisão/aprovação arquitetural antes da Fase 1.
- Gates pendentes: revisão jurídica de providers/LGPD e decisão de licença.
- Não iniciar Data Core, addons Odoo ou ingestão antes do gate de saída da Fase 0.

## Decisões e restrições ativas

- Data Plane nacional central: [ADR-001](docs/decisions/ADR-001-data-plane.md).
- Odoo guarda operação/promovidos, não o corpus: [ADR-002](docs/decisions/ADR-002-odoo-boundary.md).
- Providers substituíveis e governados: [ADR-003](docs/decisions/ADR-003-provider-framework.md).
- BigQuery analítico, PostgreSQL serving: [ADR-004](docs/decisions/ADR-004-bigquery.md).
- Tenant explícito e deny-by-default: [ADR-005](docs/decisions/ADR-005-multitenancy.md).
- Intelligence não altera fatos autonomamente: [ADR-006](docs/decisions/ADR-006-intelligence.md).
- ADRs permanecem `Proposed`; CTEP não altera seu status.
- Simplexo Score/crédito/risco é outro produto e permanece proibido neste repositório.

## Mapa operacional

- Entrada/instruções: `PROJECT_STATE.md`, `AGENTS.md`, `docs/GOVERNANCE.md`.
- Estado detalhado: `.simplexo/state.yaml`, `docs/CURRENT.md`, `docs/CHANGELOG.md`.
- Escopo/requisitos: `docs/PROJECT_CHARTER.md`, `docs/REQUIREMENTS.md`.
- Arquitetura/dados: `docs/ARCHITECTURE.md`, `docs/DATA_ARCHITECTURE.md`, `docs/DATA_MODEL.md`.
- Reuso/pesquisa: `docs/OCA_REUSE_MATRIX.md`, `docs/BENCHMARK.md`, `docs/PROVIDERS.md`.
- Controles: `docs/SECURITY.md`, `docs/LGPD.md`, `docs/AI_GOVERNANCE.md`, `docs/FINOPS.md`.
- Entrega: `docs/ROADMAP.md`, `docs/TEST_PLAN.md`, `docs/DEPLOYMENT.md`.
- CI: `.github/workflows/docs.yml`; backlog: GitHub Project #13 / issues #1–#15.
- Código/testes/infra: ainda inexistentes; criar progressivamente, nunca como placeholders.

## Evidências reutilizáveis

- Benchmark competitivo: [snapshot 2026-08-30](docs/BENCHMARK.md); atualizar somente o delta quando versão/mercado mudar.
- Auditoria Odoo/OCA: [matriz 18.0 inicial](docs/OCA_REUSE_MATRIX.md); pins/licenças/install tests ainda pendentes.
- Providers/fontes: [registro inicial](docs/PROVIDERS.md); aprovação legal ainda pendente.
- Arquitetura e modelo: documentos acima e ADRs; não refazer sem gatilho técnico.
- Histórico da recuperação e CI: [CURRENT](docs/CURRENT.md).

## Validação

- LOW documental: arquivos requeridos, `git diff --check`, YAML parse e scan de private key.
- MEDIUM: LOW + links/contratos/testes diretamente afetados.
- HIGH: MEDIUM + decisões, segurança/multiempresa, instalação/upgrade, rollback e gates pertinentes.
- Odoo: validar progressivamente manifest/sintaxe, testes direcionados, instalação limpa, upgrade/migração e integridade.
- UI: homologação funcional/visual por permissões e companies representativas; aprovação humana quando exigida.
- Nunca declarar CI verde enquanto Actions não executar steps com sucesso.

## Próximos passos

1. Concluir revisão/PR da migração CTEP sem mudança funcional.
2. Corrigir billing/spending de Actions e obter CI documental executado/verde.
3. Revisar os documentos de Fase 0, completar pins/licenças/validações pendentes e registrar deltas.
4. Obter aprovação humana do gate arquitetural.
5. Somente então iniciar a issue #2 — Fase 1 Data Core.

## Exceções e riscos abertos

- A antiga regra de ler sempre `AGENTS.md`, `state.yaml` e `CURRENT.md` integralmente foi substituída pela entrada seletiva CTEP; os três continuam canônicos em suas responsabilidades.
- O Prompt Master exige recuperação ampla por fase/checkpoint; nesses eventos ele é gatilho legítimo de budget HIGH/full audit.
- CNPJ alfanumérico, SLAs, RPO/RTO, custos, licença e termos de providers seguem sem aprovação final.

## CTEP

- Context budget padrão: LOW; elevar para MEDIUM/HIGH pelos riscos definidos em `AGENTS.md`.
- Última revisão desta síntese: 2026-08-31.
- Primeira execução: HIGH; full audit solicitado explicitamente para migração de governança.
- Métricas desta migração: selective reading após auditoria; evidências reutilizadas 6 ADRs + benchmark + OCA matrix + providers; nenhuma decisão reaberta.
- Manutenção: atualizar apenas fatos duráveis e manter preferencialmente 60–150 linhas.
