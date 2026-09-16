-- Simplexo Data - Canonical Data Core Schema
-- Database initialization with extensions, core entities, sources, observations and commercial scoring

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Schema for canonical data plane
CREATE SCHEMA IF NOT EXISTS data_core;
CREATE SCHEMA IF NOT EXISTS data_mining;
CREATE SCHEMA IF NOT EXISTS data_app;

-- ==========================================================
-- 1. DATA CORE (Base Cadastral & Entidades Primárias)
-- ==========================================================

-- Tabela de Empresas (Raiz do CNPJ)
CREATE TABLE IF NOT EXISTS data_core.companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cnpj_base VARCHAR(14) NOT NULL UNIQUE, -- Raiz do CNPJ (suporta alfanumérico)
    legal_name VARCHAR(255) NOT NULL,      -- Razão Social
    legal_nature_code VARCHAR(10),         -- Código da Natureza Jurídica
    legal_nature_desc VARCHAR(255),
    share_capital NUMERIC(18, 2) DEFAULT 0, -- Capital Social
    company_size VARCHAR(20),              -- Porte da Empresa (ME, EPP, DEMAIS)
    federative_entity VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Estabelecimentos (Matrizes e Filiais)
CREATE TABLE IF NOT EXISTS data_core.establishments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES data_core.companies(id) ON DELETE CASCADE,
    cnpj VARCHAR(20) NOT NULL UNIQUE,      -- CNPJ Completo (Normalizado)
    cnpj_order VARCHAR(4) NOT NULL,        -- Ordem (0001 = Matriz, 0002... = Filial)
    cnpj_dv VARCHAR(2) NOT NULL,           -- Dígito Verificador
    trade_name VARCHAR(255),               -- Nome Fantasia
    registration_status VARCHAR(20) NOT NULL, -- Situação Cadastral (ATIVA, BAIXADA, etc.)
    status_date DATE,                      -- Data da Situação Cadastral
    status_reason VARCHAR(255),            -- Motivo da Situação
    start_activity_date DATE,              -- Data de Início de Atividade
    cnae_main VARCHAR(10) NOT NULL,        -- CNAE Principal
    cnae_main_desc TEXT,
    cnae_secondary TEXT[],                 -- Array de CNAEs Secundários
    
    -- Endereço / Localização
    street_type VARCHAR(50),
    street VARCHAR(255),
    number VARCHAR(50),
    complement VARCHAR(255),
    neighborhood VARCHAR(100),
    zip_code VARCHAR(10),                  -- CEP
    city_code VARCHAR(10),                 -- Código Município IBGE/RFB
    city_name VARCHAR(100) NOT NULL,       -- Município
    state_code VARCHAR(2) NOT NULL,        -- UF (SP, RJ, etc.)
    country_name VARCHAR(100) DEFAULT 'BRASIL',
    
    -- Contatos Cadastrais (Origem Receita)
    cadastral_email VARCHAR(255),
    cadastral_phone_1 VARCHAR(20),
    cadastral_phone_2 VARCHAR(20),
    cadastral_fax VARCHAR(20),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Sócios e Administradores (QSA)
CREATE TABLE IF NOT EXISTS data_core.partners_qsa (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES data_core.companies(id) ON DELETE CASCADE,
    partner_type VARCHAR(20),              -- Pessoa Física / Jurídica / Estrangeiro
    partner_name VARCHAR(255) NOT NULL,
    partner_doc VARCHAR(20),               -- CPF mascarado ou CNPJ do sócio
    qualification_code VARCHAR(10),
    qualification_desc VARCHAR(255),
    entry_date DATE,
    age_range VARCHAR(50),
    legal_rep_name VARCHAR(255),
    legal_rep_doc VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Simples Nacional & MEI
CREATE TABLE IF NOT EXISTS data_core.simples_nacional (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES data_core.companies(id) ON DELETE CASCADE,
    cnpj_base VARCHAR(14) UNIQUE,
    is_simples BOOLEAN DEFAULT FALSE,
    simples_opt_date DATE,
    simples_excl_date DATE,
    is_mei BOOLEAN DEFAULT FALSE,
    mei_opt_date DATE,
    mei_excl_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- 2. DATA MINING & ENRICHMENT ENGINE (Ativo Proprietário)
-- ==========================================================

-- Fontes de Dados e Auditoria
CREATE TABLE IF NOT EXISTS data_mining.sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_name VARCHAR(100) NOT NULL UNIQUE, -- ex: 'receita_federal', 'website_crawl', 'google_places', 'linkedin'
    source_type VARCHAR(50) NOT NULL,         -- 'public_open_data', 'web_mining', 'api_partner'
    confidence_weight NUMERIC(3, 2) DEFAULT 1.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Contatos Enriquecidos e Minerados
CREATE TABLE IF NOT EXISTS data_mining.contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE,
    contact_type VARCHAR(30) NOT NULL,        -- 'phone', 'whatsapp', 'email', 'website', 'linkedin', 'instagram'
    contact_value VARCHAR(255) NOT NULL,      -- O valor do contato (ex: +5511999999999 ou comercial@empresa.com.br)
    contact_label VARCHAR(100),               -- 'comercial', 'financeiro', 'diretoria', 'geral'
    is_validated BOOLEAN DEFAULT FALSE,       -- Se foi validado por SMTP/MX ou WhatsApp check
    validation_status VARCHAR(50),            -- 'valid', 'invalid', 'deliverable', 'number_exists'
    validated_at TIMESTAMP WITH TIME ZONE,
    source_id UUID REFERENCES data_mining.sources(id),
    confidence_score NUMERIC(5, 2) DEFAULT 0, -- Score do contato (0.0 a 100.0)
    raw_payload JSONB,                        -- Metadados da extração
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_est_contact UNIQUE (establishment_id, contact_type, contact_value)
);

-- Pessoas / Decisores Mapeados
CREATE TABLE IF NOT EXISTS data_mining.people (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES data_core.companies(id) ON DELETE CASCADE,
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE SET NULL,
    full_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(150),                   -- 'CEO', 'Diretor Comercial', 'Gerente de TI'
    is_decision_maker BOOLEAN DEFAULT FALSE,  -- Decisor comercial
    linkedin_url VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    source_id UUID REFERENCES data_mining.sources(id),
    confidence_score NUMERIC(5, 2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Presença Digital & Tech Stack
CREATE TABLE IF NOT EXISTS data_mining.digital_footprint (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE UNIQUE,
    website_url VARCHAR(255),
    domain_name VARCHAR(150),
    domain_created_at DATE,
    has_mx_record BOOLEAN DEFAULT FALSE,
    mail_provider VARCHAR(100),               -- 'Google Workspace', 'Microsoft 365', 'cPanel', etc.
    detected_technologies JSONB DEFAULT '[]'::JSONB, -- E-commerce, CMS, CRM detectados
    google_rating NUMERIC(2, 1),
    google_review_count INT DEFAULT 0,
    social_profiles JSONB DEFAULT '{}'::JSONB,
    last_crawled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Motor de Qualidade / Commercial Lead Score (0 a 100)
CREATE TABLE IF NOT EXISTS data_mining.commercial_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE UNIQUE,
    total_score INT NOT NULL DEFAULT 0,       -- 0 a 100
    score_grade VARCHAR(20) NOT NULL,         -- 'EXCELENTE' (90-100), 'MUITO_BOM' (70-89), 'BOM' (50-69), 'BAIXO' (30-49), 'MUITO_BAIXO' (0-29)
    has_valid_whatsapp BOOLEAN DEFAULT FALSE,
    has_valid_phone BOOLEAN DEFAULT FALSE,
    has_valid_email BOOLEAN DEFAULT FALSE,
    has_website BOOLEAN DEFAULT FALSE,
    has_decision_maker BOOLEAN DEFAULT FALSE,
    score_breakdown JSONB DEFAULT '{}'::JSONB,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fila e Controle de Jobs de Enriquecimento
CREATE TABLE IF NOT EXISTS data_mining.enrichment_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL,            -- 'web_crawl', 'whatsapp_validation', 'email_mx_check', 'deep_enrich'
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'RUNNING', 'COMPLETED', 'FAILED'
    priority INT DEFAULT 5,                   -- 1 (máxima) a 10 (mínima)
    retry_count INT DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- 3. DATA APP (Listas, Filtros & Integração Odoo / CRM)
-- ==========================================================

-- Listas Comerciais Salvas (Mailing)
CREATE TABLE IF NOT EXISTS data_app.lead_lists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    filter_criteria JSONB NOT NULL,           -- Critérios de filtro (CNAE, UF, Cidade, Score mínimo, etc.)
    total_leads_count INT DEFAULT 0,
    created_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Itens da Lista Comercial (Leads prontos para o vendedor)
CREATE TABLE IF NOT EXISTS data_app.lead_list_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_list_id UUID REFERENCES data_app.lead_lists(id) ON DELETE CASCADE,
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE,
    assigned_sales_rep VARCHAR(100),          -- Vendedor atribuído
    status VARCHAR(50) DEFAULT 'NOVO',        -- 'NOVO', 'QUALIFICADO', 'ATRIBUIDO', 'CONTATADO', 'CONVERTIDO', 'DESCARTADO'
    promoted_to_crm BOOLEAN DEFAULT FALSE,
    crm_lead_id VARCHAR(100),
    promoted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_list_est UNIQUE (lead_list_id, establishment_id)
);

-- ==========================================================
-- 4. ÍNDICES DE ALTA PERFORMANCE (Trigrams, B-Tree, GIN)
-- ==========================================================

-- Índices de busca cadastral
CREATE INDEX IF NOT EXISTS idx_companies_legal_name_trgm ON data_core.companies USING gin (legal_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_est_trade_name_trgm ON data_core.establishments USING gin (trade_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_est_cnpj ON data_core.establishments (cnpj);
CREATE INDEX IF NOT EXISTS idx_est_cnae_main ON data_core.establishments (cnae_main);
CREATE INDEX IF NOT EXISTS idx_est_state_city ON data_core.establishments (state_code, city_name);
CREATE INDEX IF NOT EXISTS idx_est_status ON data_core.establishments (registration_status);

-- Índices de busca de contatos e scores
CREATE INDEX IF NOT EXISTS idx_contacts_type_val ON data_mining.contacts (contact_type, contact_value);
CREATE INDEX IF NOT EXISTS idx_contacts_est_id ON data_mining.contacts (establishment_id);
CREATE INDEX IF NOT EXISTS idx_scores_total ON data_mining.commercial_scores (total_score DESC);
CREATE INDEX IF NOT EXISTS idx_scores_grade ON data_mining.commercial_scores (score_grade);

-- Inserção de Fontes Padrão
INSERT INTO data_mining.sources (source_name, source_type, confidence_weight)
VALUES 
    ('receita_federal', 'public_open_data', 0.90),
    ('website_crawler', 'web_mining', 0.85),
    ('whois_dns', 'web_mining', 0.95),
    ('google_places', 'web_mining', 0.80),
    ('whatsapp_checker', 'active_validation', 1.00),
    ('smtp_mx_checker', 'active_validation', 0.95)
ON CONFLICT (source_name) DO NOTHING;
