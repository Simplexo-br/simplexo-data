# AGENTS.md — Simplexo Data

## Entrada obrigatória e CTEP

Este repositório adota permanentemente o **CTEP — Context & Token Efficiency Protocol**. Antes de qualquer tarefa, siga a leitura seletiva e pare quando houver contexto seguro:

1. `PROJECT_STATE.md` (resumo operacional e links relevantes);
2. `git status`, log curto e diff relacionado;
3. arquivos diretamente afetados;
4. dependências, chamadores, contratos, testes e configuração diretos;
5. somente a documentação necessária para resolver dúvida ou risco concreto.

Não releia todo o repositório, histórico ou documentação por rotina. Reutilize evidências válidas indicadas no `PROJECT_STATE.md`. Consulte `.simplexo/state.yaml` e `docs/CURRENT.md` quando a tarefa alterar checkpoint, estado canônico ou exigir histórico detalhado. Leia `docs/GOVERNANCE.md` para a política completa.

Classifique a tarefa com o menor context budget seguro: `LOW` (local/reversível), `MEDIUM` (dependências/contrato moderados) ou `HIGH` (segurança, autorização, dados persistentes, multiempresa, migração, infraestrutura, release ou arquitetura). Eleve o budget se o risco crescer.

Full audit somente por gatilho explícito: pedido de auditoria; mudança de arquitetura, segurança ou modelo de dados; upgrade principal; migração irreversível; incidente/regressão sistêmica; release crítico; inconsistência relevante; evidência insuficiente; ou impacto transversal não delimitável. Registre o gatilho e escopo.

## Objetivo e limites

Pesquisar, analisar, segmentar, enriquecer e qualificar empresas brasileiras, promovendo seleções explícitas a prospects/CRM. Não é banco de listas, CRM/BI/filas/API paralelos. Odoo 18 Community é o Application Plane; PostgreSQL dedicado, GCS e BigQuery formam o Data Plane central; Simplexo Intelligence é o Intelligence Plane. A base nacional nunca deve ser replicada em Odoo ou convertida em `res.partner`.

**Simplexo Score é outro produto.** É proibido criar módulos de score de crédito/risco neste repositório.

## OCA-FIRST

Antes de implementar: procurar primeiro no projeto; verificar módulos já aprovados, Odoo Core 18 e OCA 18.0; reutilizar a matriz e evidências existentes; pesquisar apenas o delta necessário; documentar gap em `docs/OCA_REUSE_MATRIX.md`. Não alterar Core nem adicionar dependência automaticamente. Reusar capacidades mantidas quando atenderem ao gap.

## Segurança, tenancy e dados

Nunca fixar database, `company_id`, `user_id`, domínio, URL, IP, tenant, credencial, API key, servidor ou caminho. Secrets fora do Git. Objetos tenant-owned exigem ownership explícito, regras deny-by-default e testes negativos. Não confiar em `sudo()` para fluxos tenant-facing.

Preservar valor bruto/normalizado, fonte, licença/termos, timestamps, parser, confiança e freshness. IA não transforma inferência em fato. Providers usam contrato comum, timeout, rate limit, cache, circuit breaker, observabilidade e waterfall determinístico. Uso produtivo depende de validação jurídica/técnica.

LGPD by design: minimização, finalidade, retenção, rastreabilidade, direitos do titular e avaliação de base legal.

Mudanças em ACLs, record rules, grupos, `sudo()`, `company_id/company_ids`, controllers/RPC/portal/website ou isolamento multiempresa são `HIGH`. Testar usuários e empresas permitidos/negados e vazamento cross-company. Mudanças em manifest, modelos, campos, XML, constraints, sequências ou dependências devem considerar sintaxe, teste direcionado, instalação limpa, upgrade/migração, integridade, idempotência e rollback conforme o risco. Alterações visuais exigem homologação em empresas/perfis representativos e evidência quando requerida; inspeção visual não substitui testes.

## Testes e comunicação progressivos

Validar do específico ao amplo: estática/sintaxe → unitário direto → módulo → integração → suíte, segurança, desempenho e homologação exigidos pelo risco/gate. Falhar cedo, corrigir causa-raiz e repetir do nível adequado. Nunca remover/afrouxar teste, cobertura, segurança ou release gate para economizar contexto.

Atualizações e entrega devem informar somente resultado, mudanças materiais, validações reais, riscos/bloqueios e próximo passo útil. Evite narrar leituras/comandos ou repetir documentação.

## Entrega

Não declarar pronto/testado/CI/screenshot/homologado sem evidência real. Em UI, aguardar aprovação humana para `VISUAL_APPROVED`. Git é memória técnica; `PROJECT_STATE.md` é memória operacional curta. Em cada checkpoint material atualize `PROJECT_STATE.md`, `CURRENT.md`, `state.yaml`, changelog, issue/Project e evidências aplicáveis. Registre apenas fatos duráveis: implementado, pendente, testes/resultados, commit/PR/CI, bloqueios, riscos e `next_action`.
