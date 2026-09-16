
-- ==========================================================
-- SIMPLEXO DATA - MULTI-SOURCE ENRICHMENT DDL MIGRATION
-- Bases: CNO, PGFN, Comex Stat, PNCP, ANTT & Technographics
-- ==========================================================

-- 1. CNO (Cadastro Nacional de Obras da Receita Federal)
CREATE TABLE IF NOT EXISTS data_mining.construction_sites_cno (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cno_number VARCHAR(30) NOT NULL UNIQUE,
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE SET NULL,
    site_name VARCHAR(255) NOT NULL,
    site_type VARCHAR(100) NOT NULL,           -- 'Edificação Residencial', 'Edificação Comercial', 'Obra de Infraestrutura', 'Reforma Industrial'
    responsible_name VARCHAR(255),
    responsible_doc VARCHAR(20),
    area_m2 NUMERIC(12, 2) DEFAULT 0,
    estimated_investment NUMERIC(14, 2) DEFAULT 0,
    street VARCHAR(255),
    neighborhood VARCHAR(150),
    city_name VARCHAR(150) NOT NULL,
    state_code VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10),
    status VARCHAR(50) DEFAULT 'EM_ANDAMENTO', -- 'EM_ANDAMENTO', 'CONCLUIDA', 'PARALISADA'
    start_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cno_state_city ON data_mining.construction_sites_cno (state_code, city_name);
CREATE INDEX IF NOT EXISTS idx_cno_investment ON data_mining.construction_sites_cno (estimated_investment DESC);

-- 2. PGFN (Dívida Ativa da União & Regularidade Fiscal)
CREATE TABLE IF NOT EXISTS data_mining.fiscal_compliance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE UNIQUE,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    has_federal_debt BOOLEAN DEFAULT FALSE,
    total_debt_amount NUMERIC(14, 2) DEFAULT 0,
    debt_count INT DEFAULT 0,
    debt_categories JSONB DEFAULT '[]'::JSONB,  -- ['Previdenciário', 'Não-Previdenciário', 'FGTS', 'Multa Eleitoral']
    regularity_status VARCHAR(50) DEFAULT 'REGULAR', -- 'REGULAR', 'EM_NEGOCIACAO', 'INSCRITO_DIVIDA_ATIVA'
    last_checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fiscal_cnpj ON data_mining.fiscal_compliance (cnpj);
CREATE INDEX IF NOT EXISTS idx_fiscal_status ON data_mining.fiscal_compliance (regularity_status);

-- 3. COMEX STAT (MDIC / SECEX - Importadores & Exportadores)
CREATE TABLE IF NOT EXISTS data_mining.comex_operations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE UNIQUE,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    is_exporter BOOLEAN DEFAULT FALSE,
    is_importer BOOLEAN DEFAULT FALSE,
    export_bracket VARCHAR(50),                -- 'Acima de US$ 50M', 'US$ 10M a 50M', 'US$ 1M a 10M', 'Até US$ 1M'
    import_bracket VARCHAR(50),
    partner_countries JSONB DEFAULT '[]'::JSONB, -- ['China', 'Estados Unidos', 'Argentina', 'Alemanha']
    top_ncm_chapters JSONB DEFAULT '[]'::JSONB,  -- ['84 - Máquinas e Aparelhos', '85 - Eletroeletrônicos']
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_comex_cnpj ON data_mining.comex_operations (cnpj);
CREATE INDEX IF NOT EXISTS idx_comex_exp_imp ON data_mining.comex_operations (is_exporter, is_importer);

-- 4. PNCP / COMPRAS PÚBLICAS (Fornecedores do Poder Público)
CREATE TABLE IF NOT EXISTS data_mining.public_contracts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE UNIQUE,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    is_public_supplier BOOLEAN DEFAULT FALSE,
    total_contract_count INT DEFAULT 0,
    total_contract_value NUMERIC(14, 2) DEFAULT 0,
    contracting_agencies JSONB DEFAULT '[]'::JSONB, -- ['Prefeitura de São Paulo', 'Ministério da Saúde', 'Petrobras']
    last_contract_date DATE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_public_contracts_cnpj ON data_mining.public_contracts (cnpj);
CREATE INDEX IF NOT EXISTS idx_public_supplier ON data_mining.public_contracts (is_public_supplier);

-- 5. ANTT / RNTRC (Transportadoras & Frotas Terrestres)
CREATE TABLE IF NOT EXISTS data_mining.transport_fleets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE UNIQUE,
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    rntrc_number VARCHAR(30),
    rntrc_status VARCHAR(50) DEFAULT 'ATIVO',
    carrier_type VARCHAR(50),                  -- 'ETC' (Empresa de Transporte de Cargas), 'CTC' (Cooperativa)
    registered_vehicles_count INT DEFAULT 0,
    fleet_category VARCHAR(50),                -- 'Leve', 'Pesado / Carreta', 'Misto'
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transport_cnpj ON data_mining.transport_fleets (cnpj);

-- 6. Expansão do Digital Footprint & Technographics
ALTER TABLE data_mining.digital_footprint 
    ADD COLUMN IF NOT EXISTS has_corporate_email BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS has_ecommerce BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS detected_cms VARCHAR(100),
    ADD COLUMN IF NOT EXISTS detected_crm VARCHAR(100),
    ADD COLUMN IF NOT EXISTS detected_erp VARCHAR(100),
    ADD COLUMN IF NOT EXISTS latitude NUMERIC(10, 7),
    ADD COLUMN IF NOT EXISTS longitude NUMERIC(10, 7),
    ADD COLUMN IF NOT EXISTS maps_place_id VARCHAR(100);
