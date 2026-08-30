# Provider Framework and Sources

Adapters declaram campos, classe da fonte, termos, freshness, timeout, rate limit, cache e custo; retornam referência raw, observações normalizadas, confiança e erros. Orquestrador usa waterfall determinístico, circuit breaker, retries limitados, negative cache e métricas.

| Source | Role | Disposition |
|---|---|---|
| RFB CNPJ | baseline bulk oficial | primária; arquivar raw/layout |
| BrasilAPI | API comunitária | revisão técnica/jurídica |
| OpenCNPJ | lookup aberto | confirmar licença/SLA/restrições |
| CNPJ.ws public | lookup | limite público baixo; fallback |
| ReceitaWS public | lookup/cache | 3 req/min e cache-only miss; fallback |
| IBGE e referências | dimensões | avaliar dataset a dataset |

“Acessível publicamente” não significa permitido armazenar/redistribuir/comercializar. Habilitação produtiva exige decisão registrada. Precedência é por campo/caso; conflitos permanecem observações. Inferências são rotuladas.
