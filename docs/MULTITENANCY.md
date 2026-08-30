# Multi-tenancy

Tenant é principal comercial/de segurança e não equivale automaticamente a database ou `company_id`. Mapeamentos tenant-instalação-database-company são configuração explícita.

O gateway resolve tenant da credencial autenticada, nunca do body; tabelas/caches/jobs tenant-owned carregam tenant; policy valida ownership/entitlement deny-by-default. Odoo usa `_check_company_auto`, `check_company`, defaults e record rules quando aplicável. Analytics cross-tenant somente autorizado/desidentificado.

Testar duas instalações, dois bancos, múltiplas companies, mesmo CNPJ selecionado por tenants distintos, troca de credencial, IDs adivinhados, cache/job bleed e caminhos admin/`sudo`.
