-- DDL for ETL Scheduler Logs and Continuous Ingestion
CREATE TABLE IF NOT EXISTS data_app.etl_schedule_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_name VARCHAR(100) NOT NULL,
    source_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'RUNNING', -- RUNNING, COMPLETED, FAILED, SKIPPED
    records_processed BIGINT DEFAULT 0,
    records_updated BIGINT DEFAULT 0,
    execution_time_seconds NUMERIC(10, 2) DEFAULT 0.0,
    details JSONB DEFAULT '{}'::jsonb,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_etl_schedule_logs_job ON data_app.etl_schedule_logs(job_name, started_at DESC);
