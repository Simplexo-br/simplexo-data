"""
Simplexo Data - Receita Federal High-Speed ETL Loader
Parses raw RFB CSV/ZIP files and streams them into PostgreSQL data_core schema.
"""

import os
import glob
import zipfile
import psycopg2
from typing import Optional

def get_db_connection():
    db_url = os.getenv("DATABASE_URL", "postgresql://simplexo:simplexo_secure_pass_2026@localhost:5432/simplexo_data")
    return psycopg2.connect(db_url)

def load_cnaes(zip_path: str):
    """Parses Cnaes.zip and loads into data_core reference tables or metadata."""
    print(f"[Loader] Processing Cnaes file: {zip_path}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for filename in zf.namelist():
            with zf.open(filename, 'r') as csv_file:
                copy_sql = """
                CREATE TEMP TABLE staging_cnaes (
                    code VARCHAR(10),
                    description VARCHAR(255)
                ) ON COMMIT DROP;
                """
                cursor.execute(copy_sql)
                print(f"[Loader] Streaming {filename} into staging...")
                cursor.copy_expert(
                    "COPY staging_cnaes FROM STDIN WITH (FORMAT csv, DELIMITER ';', QUOTE '\"', ENCODING 'LATIN1')",
                    csv_file
                )
                cursor.execute("SELECT COUNT(*) FROM staging_cnaes;")
                count = cursor.fetchone()[0]
                print(f"[Loader] Loaded {count} CNAE definitions.")
                conn.commit()

    cursor.close()
    conn.close()

def load_simples(zip_path: str):
    """Parses Simples.zip and bulk loads into data_core.simples_nacional using COPY."""
    print(f"[Loader] Processing Simples file: {zip_path}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for filename in zf.namelist():
            with zf.open(filename, 'r') as csv_file:
                copy_sql = """
                CREATE TEMP TABLE staging_simples (
                    cnpj_base VARCHAR(14),
                    simples_opt_str VARCHAR(1),
                    simples_start_str VARCHAR(10),
                    simples_end_str VARCHAR(10),
                    mei_opt_str VARCHAR(1),
                    mei_start_str VARCHAR(10),
                    mei_end_str VARCHAR(10)
                ) ON COMMIT DROP;
                """
                cursor.execute(copy_sql)
                print(f"[Loader] Streaming {filename} into staging...")
                cursor.copy_expert(
                    "COPY staging_simples FROM STDIN WITH (FORMAT csv, DELIMITER ';', QUOTE '\"', ENCODING 'LATIN1')",
                    csv_file
                )
                
                print(f"[Loader] Upserting Simples Nacional into data_core.simples_nacional...")
                upsert_sql = """
                INSERT INTO data_core.simples_nacional (
                    cnpj_base, is_simples, simples_opt_date, simples_excl_date,
                    is_mei, mei_opt_date, mei_excl_date
                )
                SELECT 
                    cnpj_base,
                    (simples_opt_str = 'S'),
                    TO_DATE(NULLIF(simples_start_str, '00000000'), 'YYYYMMDD'),
                    TO_DATE(NULLIF(simples_end_str, '00000000'), 'YYYYMMDD'),
                    (mei_opt_str = 'S'),
                    TO_DATE(NULLIF(mei_start_str, '00000000'), 'YYYYMMDD'),
                    TO_DATE(NULLIF(mei_end_str, '00000000'), 'YYYYMMDD')
                FROM staging_simples
                ON CONFLICT (cnpj_base) DO UPDATE SET
                    is_simples = EXCLUDED.is_simples,
                    simples_opt_date = EXCLUDED.simples_opt_date,
                    simples_excl_date = EXCLUDED.simples_excl_date,
                    is_mei = EXCLUDED.is_mei,
                    mei_opt_date = EXCLUDED.mei_opt_date,
                    mei_excl_date = EXCLUDED.mei_excl_date,
                    updated_at = CURRENT_TIMESTAMP;
                """
                cursor.execute(upsert_sql)
                conn.commit()
                print(f"[Loader] Finished loading Simples Nacional from {filename}.")

    cursor.close()
    conn.close()

def load_empresas(zip_path: str):
    """Parses Empresas.zip files and bulk loads into data_core.companies using COPY."""
    print(f"[Loader] Processing Empresas file: {zip_path}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for filename in zf.namelist():
            with zf.open(filename, 'r') as csv_file:
                copy_sql = """
                CREATE TEMP TABLE staging_companies (
                    cnpj_base VARCHAR(14),
                    legal_name VARCHAR(255),
                    legal_nature_code VARCHAR(10),
                    qualif VARCHAR(10),
                    share_capital_str VARCHAR(50),
                    company_size VARCHAR(20),
                    federative_entity VARCHAR(100)
                ) ON COMMIT DROP;
                """
                cursor.execute(copy_sql)
                
                print(f"[Loader] Streaming {filename} into staging...")
                cursor.copy_expert(
                    "COPY staging_companies FROM STDIN WITH (FORMAT csv, DELIMITER ';', QUOTE '\"', ENCODING 'LATIN1')",
                    csv_file
                )
                
                upsert_sql = """
                INSERT INTO data_core.companies (
                    cnpj_base, legal_name, legal_nature_code, share_capital, company_size, federative_entity
                )
                SELECT 
                    cnpj_base,
                    legal_name,
                    legal_nature_code,
                    COALESCE(NULLIF(REPLACE(share_capital_str, ',', '.'), '')::NUMERIC, 0),
                    CASE company_size
                        WHEN '01' THEN 'ME'
                        WHEN '03' THEN 'EPP'
                        WHEN '05' THEN 'DEMAIS'
                        ELSE 'NAO_INFORMADO'
                    END,
                    federative_entity
                FROM staging_companies
                ON CONFLICT (cnpj_base) DO UPDATE SET
                    legal_name = EXCLUDED.legal_name,
                    legal_nature_code = EXCLUDED.legal_nature_code,
                    share_capital = EXCLUDED.share_capital,
                    company_size = EXCLUDED.company_size,
                    updated_at = CURRENT_TIMESTAMP;
                """
                cursor.execute(upsert_sql)
                conn.commit()
                print(f"[Loader] Finished loading {filename}.")

    cursor.close()
    conn.close()

def load_estabelecimentos(zip_path: str):
    """Parses Estabelecimentos.zip files and bulk loads into data_core.establishments using COPY."""
    print(f"[Loader] Processing Estabelecimentos file: {zip_path}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for filename in zf.namelist():
            with zf.open(filename, 'r') as csv_file:
                copy_sql = """
                CREATE TEMP TABLE staging_establishments (
                    cnpj_base VARCHAR(14),
                    cnpj_order VARCHAR(4),
                    cnpj_dv VARCHAR(2),
                    matriz_filial VARCHAR(1),
                    trade_name VARCHAR(255),
                    registration_status VARCHAR(2),
                    status_date_str VARCHAR(10),
                    status_reason VARCHAR(255),
                    city_exterior VARCHAR(100),
                    country_code VARCHAR(10),
                    start_activity_str VARCHAR(10),
                    cnae_main VARCHAR(10),
                    cnae_sec TEXT,
                    street_type VARCHAR(50),
                    street VARCHAR(255),
                    number VARCHAR(50),
                    complement VARCHAR(255),
                    neighborhood VARCHAR(100),
                    zip_code VARCHAR(10),
                    state_code VARCHAR(2),
                    city_code VARCHAR(10),
                    ddd_1 VARCHAR(10),
                    phone_1 VARCHAR(20),
                    ddd_2 VARCHAR(10),
                    phone_2 VARCHAR(20),
                    ddd_fax VARCHAR(10),
                    fax VARCHAR(20),
                    cadastral_email VARCHAR(255),
                    special_situation VARCHAR(100),
                    special_situation_date VARCHAR(10)
                ) ON COMMIT DROP;
                """
                cursor.execute(copy_sql)
                
                print(f"[Loader] Streaming {filename} into staging...")
                cursor.copy_expert(
                    "COPY staging_establishments FROM STDIN WITH (FORMAT csv, DELIMITER ';', QUOTE '\"', ENCODING 'LATIN1')",
                    csv_file
                )
                
                upsert_sql = """
                INSERT INTO data_core.establishments (
                    company_id, cnpj, cnpj_order, cnpj_dv, trade_name, registration_status,
                    status_date, start_activity_date, cnae_main, street_type, street, number,
                    complement, neighborhood, zip_code, city_code, city_name, state_code,
                    cadastral_email, cadastral_phone_1, cadastral_phone_2
                )
                SELECT 
                    c.id,
                    CONCAT(s.cnpj_base, s.cnpj_order, s.cnpj_dv),
                    s.cnpj_order,
                    s.cnpj_dv,
                    s.trade_name,
                    CASE s.registration_status
                        WHEN '01' THEN 'NULA'
                        WHEN '02' THEN 'ATIVA'
                        WHEN '03' THEN 'SUSPENSA'
                        WHEN '04' THEN 'INAPTA'
                        WHEN '08' THEN 'BAIXADA'
                        ELSE 'OUTRA'
                    END,
                    TO_DATE(NULLIF(s.status_date_str, '0'), 'YYYYMMDD'),
                    TO_DATE(NULLIF(s.start_activity_str, '0'), 'YYYYMMDD'),
                    s.cnae_main,
                    s.street_type,
                    s.street,
                    s.number,
                    s.complement,
                    s.neighborhood,
                    s.zip_code,
                    s.city_code,
                    COALESCE(s.city_code, 'NAO_INFORMADO'),
                    s.state_code,
                    NULLIF(LOWER(s.cadastral_email), ''),
                    NULLIF(CONCAT(s.ddd_1, s.phone_1), ''),
                    NULLIF(CONCAT(s.ddd_2, s.phone_2), '')
                FROM staging_establishments s
                LEFT JOIN data_core.companies c ON c.cnpj_base = s.cnpj_base
                ON CONFLICT (cnpj) DO UPDATE SET
                    trade_name = EXCLUDED.trade_name,
                    registration_status = EXCLUDED.registration_status,
                    status_date = EXCLUDED.status_date,
                    updated_at = CURRENT_TIMESTAMP;
                """
                cursor.execute(upsert_sql)
                conn.commit()
                print(f"[Loader] Finished loading {filename}.")

    cursor.close()
    conn.close()

def run_full_load(raw_dir: str = "/data/rfb_raw"):
    """Runs the loader across all downloaded zip files in raw_dir."""
    cnaes_files = sorted(glob.glob(os.path.join(raw_dir, "*Cnaes*.zip")))
    simples_files = sorted(glob.glob(os.path.join(raw_dir, "*Simples*.zip")))
    empresa_files = sorted(glob.glob(os.path.join(raw_dir, "*Empresas*.zip")))
    estab_files = sorted(glob.glob(os.path.join(raw_dir, "*Estabelecimentos*.zip")))
    
    for f in cnaes_files:
        load_cnaes(f)

    for f in simples_files:
        load_simples(f)

    for f in empresa_files:
        load_empresas(f)
        
    for f in estab_files:
        load_estabelecimentos(f)

if __name__ == "__main__":
    run_full_load("/data/rfb_raw")
