# CURRENT — 2026-08-31

## Estado real

Fase 0 (`in_progress`). O repositório oficial foi recuperado na `main`; antes deste checkpoint continha apenas README no commit inicial `a84c836`. Não havia addons, serviços, documentação, issues, PRs ou workflows.

O Drive oficial foi listado e está vazio. O Project #13 está acessível e contém 15 itens, correspondentes às issues #1–#15; na verificação de 2026-08-31 todos estavam em `Todo`.

## Este checkpoint

Criada baseline de continuidade, charter/requisitos, benchmark, matriz OCA, arquiteturas, providers, tenancy, segurança, LGPD, IA, comercial, FinOps, ADRs, roadmap, templates e CI documental. Issues [#1](https://github.com/Simplexo-br/simplexo-data/issues/1) a [#15](https://github.com/Simplexo-br/simplexo-data/issues/15) representam as fases 0–14 e estão vinculadas ao Project #13. Isto não é produto implementado nem conclusão da fase.

Migração CTEP implementada em `chore/ctep-governance`: `PROJECT_STATE.md` é a memória operacional curta; `AGENTS.md` e `docs/GOVERNANCE.md` estabelecem leitura seletiva, budgets LOW/MEDIUM/HIGH, gatilhos de full audit, evidência reutilizável, testes progressivos e regras Odoo. Objetivo, escopo, arquitetura, requisitos, roadmap e ADRs não foram alterados.

Executado: recuperação Git, inventário, consulta de PRs/issues/runs, listagem do Drive, pesquisa oficial, auditoria documental, validação local de arquivos/YAML/segredos/whitespace, commit e push. Não executado: instalação Odoo, testes de addon, ingestão RFB, performance, isolamento e homologação visual.

Commit inicial da baseline: `016c113`. CI [run 33334919755](https://github.com/Simplexo-br/simplexo-data/actions/runs/33334919755): **failure sem execução de steps**. A anotação GitHub informa pagamentos recentes falhos ou spending limit; não é falha dos checks documentais. Rerun obrigatório após correção de billing.

## Bloqueios/riscos

Actions bloqueado por billing/spending; licença provisória; providers aguardam parecer jurídico; SLAs/RPO/RTO/custos aguardam validação; CNPJ alfanumérico precisa ser suportado desde o modelo inicial.

## Próxima ação

Revisar/mesclar a migração CTEP, corrigir billing de Actions, rerodar CI, revisar os deltas pendentes da Fase 0 e aprovar o gate arquitetural. Só então abrir Fase 1 — Data Core.
