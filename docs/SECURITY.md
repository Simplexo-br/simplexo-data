# Security Baseline

- tenant leakage: ownership/policy e testes negativos;
- secrets: Secret Manager, rotação, contas mínimas, redaction;
- injection: schemas, operadores allowlisted e SQL parametrizado;
- export abuse: quotas, caps, anomalias e auditoria;
- supply chain: pins, SCA/licença, branch/workflows protegidos;
- provider compromise: egress allowlist, timeout, size/schema e quarentena;
- poisoning: checksum, origem, lineage e reconciliação;
- AI leakage: tools allowlisted, tenant context e sem fact writes autônomos.

Produção exige threat model, incident response, pentest, backup/restore, RPO/RTO, rotação e vulnerability SLA aprovados.
