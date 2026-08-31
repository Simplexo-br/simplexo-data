# Governança de contexto — CTEP

## Finalidade e precedência

O Context & Token Efficiency Protocol reduz releitura, reanálise e comunicação redundante sem reduzir correção, segurança, rastreabilidade ou gates. Ele otimiza o modo de operar; não muda objetivo, escopo, arquitetura, requisitos ou decisões do Simplexo Data. Requisitos explícitos mais críticos prevalecem e a exceção deve ser registrada brevemente no `PROJECT_STATE.md`.

## Documentação em camadas

1. **Operacional:** `PROJECT_STATE.md`, porta de entrada curta.
2. **Normativa:** `AGENTS.md`, este documento, arquitetura, segurança, contratos e ADRs.
3. **Evidência/histórico:** `CURRENT.md`, changelog, benchmarks, pesquisas, planos e resultados.

A leitura começa na camada 1 e expande somente para responder uma dúvida, dependência, risco ou falha concreta.

## Leitura seletiva e evidências

Ordem: `PROJECT_STATE.md` → Git recente/diff → arquivos afetados → dependências/contratos/testes diretos → documentação necessária. Antes de benchmark, auditoria ou pesquisa, localizar evidência persistente, verificar data/versão/premissa/escopo e executar apenas o delta. Reexecutar quando versão, ambiente, requisito, dados ou risco mudarem, ou quando a evidência for insuficiente.

## Context budgets

- `LOW`: mudança local, clara, reversível; estado, Git, arquivos/testes diretos.
- `MEDIUM`: comportamento compartilhado, integração/contrato local, dependências moderadas ou migração limitada.
- `HIGH`: autenticação/autorização, segurança, dados persistentes, multiempresa, infraestrutura, integração externa crítica, arquitetura, release ou migração relevante.

Elevar o budget durante a tarefa se surgir risco novo e registrar o motivo quando útil. Budget não limita testes/gates obrigatórios.

## Full audit

Permitido somente por solicitação explícita; mudança arquitetural/de segurança/modelo; major upgrade; migração irreversível; incidente/regressão sistêmica; release crítico; inconsistência relevante; evidência ausente/baixa; ou impacto transversal não delimitável. Definir motivo e escopo. “Garantir tudo” não basta.

## Testes progressivos

Executar estática/sintaxe, unitário direto, módulo, integração e suítes/gates amplos conforme risco. Interromper cedo em falha explicativa, corrigir a causa e repetir do nível adequado. É proibido apagar, ignorar, afrouxar ou substituir testes e gates por raciocínio ou inspeção visual.

## Odoo 18 Community

Ler primeiro manifest, dependências, modelos/views e testes afetados. Seguir REUSE-FIRST/OCA-FIRST sem adicionar dependência automaticamente. ACLs, record rules, grupos, `sudo`, companies e superfícies externas são HIGH e exigem testes permitidos/negados e cross-company. Alterações de schema/XML/dependências avaliam instalação limpa, upgrade/migração, integridade, idempotência e recuperação. UI exige homologação por perfis/companies; evidência visual não substitui testes.

## Git, estado e comunicação

Git preserva intenção/evidência; usar status/diff/log curto e histórico profundo apenas para perguntas concretas. Commits pequenos e coerentes. `PROJECT_STATE.md` registra somente estado durável, links e próxima ação, não logs/conversa. Outputs informam resultado, mudanças, validação, riscos e próximo passo, sem narrativa repetitiva.

## Métricas de eficiência

Registrar `context_efficiency` em `.simplexo/state.yaml` nos checkpoints quando o custo for baixo. Métricas são diagnósticas e nunca justificam leitura/teste insuficiente:

- `context_budget`, `selective_reading_used`, `full_audit_triggered`;
- evidências reutilizadas/novas, arquivos lidos/alterados, expansões;
- `targeted_tests_first`, `avoidable_rework_detected`.

## Manutenção

Atualizar a síntese apenas quando fatos duráveis mudarem. Remover bloqueios resolvidos e estado transitório. Não duplicar fontes detalhadas. Revisar os links e comandos mínimos em checkpoints de fase, mudanças de gate ou inconsistências detectadas.
