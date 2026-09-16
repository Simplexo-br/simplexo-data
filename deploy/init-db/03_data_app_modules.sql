-- ==========================================================
-- SIMPLEXO DATA - 03_DATA_APP_MODULES.SQL
-- Schema migration for 5 Commercial Intelligence Modules
-- ==========================================================

CREATE SCHEMA IF NOT EXISTS data_app;

-- 1. Meus Alertas (Radar de Monitoramento de Mercado)
CREATE TABLE IF NOT EXISTS data_app.user_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) DEFAULT 'admin',
    name VARCHAR(255) NOT NULL,
    cnae_prefix VARCHAR(10),
    state_code VARCHAR(2),
    city_name VARCHAR(100),
    min_score INT DEFAULT 70,
    min_revenue_bracket VARCHAR(50),
    monitor_cno BOOLEAN DEFAULT FALSE,
    frequency VARCHAR(20) DEFAULT 'DAILY',
    is_active BOOLEAN DEFAULT TRUE,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Eventos / Notificações geradas pelos alertas
CREATE TABLE IF NOT EXISTS data_app.alert_notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_id UUID REFERENCES data_app.user_alerts(id) ON DELETE CASCADE,
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE,
    event_type VARCHAR(50) DEFAULT 'NEW_COMPANY_OPENED',
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Minhas Listas (Gestão de Prospecção & ICPs Salvos)
CREATE TABLE IF NOT EXISTS data_app.lead_lists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id VARCHAR(100) DEFAULT 'default',
    user_id VARCHAR(100) DEFAULT 'admin',
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tag_color VARCHAR(20) DEFAULT '#3b82f6',
    filter_criteria JSONB DEFAULT '{}'::JSONB,
    total_leads_count INT DEFAULT 0,
    created_by VARCHAR(100) DEFAULT 'admin',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE data_app.lead_lists ADD COLUMN IF NOT EXISTS user_id VARCHAR(100) DEFAULT 'admin';
ALTER TABLE data_app.lead_lists ADD COLUMN IF NOT EXISTS tag_color VARCHAR(20) DEFAULT '#3b82f6';
ALTER TABLE data_app.lead_lists ALTER COLUMN filter_criteria DROP NOT NULL;
ALTER TABLE data_app.lead_lists ALTER COLUMN tenant_id DROP NOT NULL;

CREATE TABLE IF NOT EXISTS data_app.lead_list_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_list_id UUID REFERENCES data_app.lead_lists(id) ON DELETE CASCADE,
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'NOVO',
    notes TEXT,
    promoted_to_crm BOOLEAN DEFAULT FALSE,
    crm_lead_id VARCHAR(100),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_list_item UNIQUE (lead_list_id, establishment_id)
);

ALTER TABLE data_app.lead_list_items ADD COLUMN IF NOT EXISTS notes TEXT;
ALTER TABLE data_app.lead_list_items ADD COLUMN IF NOT EXISTS added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

-- 3. Histórico de Pesquisas
CREATE TABLE IF NOT EXISTS data_app.search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) DEFAULT 'admin',
    query_term VARCHAR(255),
    state_code VARCHAR(2),
    cnae_prefix VARCHAR(10),
    min_score INT DEFAULT 0,
    filters_applied JSONB DEFAULT '{}'::JSONB,
    results_count INT DEFAULT 0,
    searched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Central de Exportações
CREATE TABLE IF NOT EXISTS data_app.export_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) DEFAULT 'admin',
    export_format VARCHAR(20) NOT NULL,
    destination_name VARCHAR(100) DEFAULT 'Download Local',
    leads_count INT NOT NULL DEFAULT 0,
    file_name VARCHAR(255),
    file_size_kb INT DEFAULT 0,
    status VARCHAR(30) DEFAULT 'CONCLUIDO',
    exported_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Assistente de Vendas (Briefings & Pitches IA)
CREATE TABLE IF NOT EXISTS data_app.sales_briefings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    establishment_id UUID REFERENCES data_core.establishments(id) ON DELETE CASCADE,
    decisor_name VARCHAR(255),
    pitch_type VARCHAR(50) DEFAULT 'WHATSAPP_ICEBREAKER',
    value_proposition TEXT,
    suggested_pitch TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices de Performance
CREATE INDEX IF NOT EXISTS idx_alerts_user ON data_app.user_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_lists_user ON data_app.lead_lists(user_id);
CREATE INDEX IF NOT EXISTS idx_list_items_list ON data_app.lead_list_items(lead_list_id);
CREATE INDEX IF NOT EXISTS idx_history_user ON data_app.search_history(user_id, searched_at DESC);
CREATE INDEX IF NOT EXISTS idx_exports_user ON data_app.export_logs(user_id, exported_at DESC);
