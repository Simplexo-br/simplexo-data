# OCA Reuse Matrix — 2026-08-30

Auditoria inicial de branches públicas 18.0; pins/licenças/testes de instalação continuam pendentes.

| Capability | Candidate | Decision / gap |
|---|---|---|
| REST | OCA `rest-framework/fastapi` | avaliar/adotar; criar apenas schemas, tenancy e metering; evitar `base_rest` depreciado |
| API key | `fastapi_auth_api_key` | avaliar contra autenticação central do gateway |
| Odoo async | OCA `queue_job` | adotar para jobs locais; ingestão nacional fica fora do Odoo |
| Connector | OCA `connector` | avaliar onde component model se encaixa |
| Audit | OCA `auditlog` | avaliar volume, retenção e redaction |
| Config | OCA `server-env` | avaliar; secrets permanecem em secret manager |
| Partner | Core + OCA `partner-contact` | seletivo, apenas promovidos |
| CRM | Odoo Core + OCA CRM | reutilizar, sem CRM paralelo |
| Contracts | OCA `contract` + sale | spike para gaps Community |
| Website/checkout | Odoo Community | verificar limites/licenças |
| Dashboard | Odoo + Intelligence | sem BI genérico novo |

Antes de código: pin de commit, manifest/dependências/licença, teste Odoo 18 Community, atividade do projeto e justificativa documentada para rejeição.
