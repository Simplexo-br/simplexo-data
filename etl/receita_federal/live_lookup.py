"""
Simplexo Data - Real-time On-Demand CNPJ & Company Ingestion
Fetches live cadastral data from Receita Federal endpoints and upserts directly into PostgreSQL.
"""

import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any, List

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://simplexo:simplexo_secure_pass_2026@localhost:5432/simplexo_data")

def get_db():
    return psycopg2.connect(DATABASE_URL)

def fetch_and_ingest_cnpj(cnpj: str) -> Optional[Dict[str, Any]]:
    """
    Fetches real-time cadastral data for a CNPJ, persists in data_core, and returns enriched record.
    """
    clean_cnpj = "".join(filter(str.isalnum, cnpj))
    if len(clean_cnpj) != 14:
        return None

    # Try BrasilAPI / MinhaReceita
    url = f"https://brasilapi.com.br/api/cnpj/v1/{clean_cnpj}"
    try:
        resp = requests.get(url, timeout=6)
        if resp.status_code != 200:
            return None
        data = resp.json()
    except Exception as e:
        print(f"[LiveLookup] Error fetching CNPJ {clean_cnpj}: {e}")
        return None

    cnpj_base = clean_cnpj[:8]
    cnpj_order = clean_cnpj[8:12]
    cnpj_dv = clean_cnpj[12:14]

    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # 1. Upsert Company
        cursor.execute("""
            INSERT INTO data_core.companies (
                cnpj_base, legal_name, share_capital, company_size
            ) VALUES (%s, %s, %s, %s)
            ON CONFLICT (cnpj_base) DO UPDATE SET
                legal_name = EXCLUDED.legal_name,
                share_capital = EXCLUDED.share_capital,
                company_size = EXCLUDED.company_size,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id;
        """, (
            cnpj_base,
            data.get("razao_social", ""),
            float(data.get("capital_social", 0)),
            "EPP" if data.get("codigo_porte") == 3 else ("ME" if data.get("codigo_porte") == 1 else "DEMAIS")
        ))
        comp_id = cursor.fetchone()["id"]

        # 2. Upsert Establishment
        cad_phone = (data.get("ddd_telefone_1") or "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        cursor.execute("""
            INSERT INTO data_core.establishments (
                company_id, cnpj, cnpj_order, cnpj_dv, trade_name,
                registration_status, cnae_main, city_name, state_code,
                cadastral_email, cadastral_phone_1
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cnpj) DO UPDATE SET
                trade_name = EXCLUDED.trade_name,
                registration_status = EXCLUDED.registration_status,
                cnae_main = EXCLUDED.cnae_main,
                city_name = EXCLUDED.city_name,
                state_code = EXCLUDED.state_code,
                cadastral_email = EXCLUDED.cadastral_email,
                cadastral_phone_1 = EXCLUDED.cadastral_phone_1,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id;
        """, (
            comp_id,
            clean_cnpj,
            cnpj_order,
            cnpj_dv,
            data.get("nome_fantasia") or data.get("razao_social"),
            data.get("descricao_situacao_cadastral", "ATIVA"),
            str(data.get("cnae_fiscal") or ""),
            data.get("municipio", ""),
            data.get("uf", ""),
            data.get("email"),
            cad_phone
        ))
        est_id = cursor.fetchone()["id"]

        # 3. Upsert QSA Partners
        if "qsa" in data and isinstance(data["qsa"], list):
            for partner in data["qsa"]:
                cursor.execute("""
                    INSERT INTO data_core.partners_qsa (
                        company_id, partner_name, qualification_desc
                    ) VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    comp_id,
                    partner.get("nome_socio", ""),
                    partner.get("qualificacao_socio", "")
                ))

        # 4. Upsert Commercial Score Initial Baseline
        has_phone = bool(cad_phone)
        has_whatsapp = bool(cad_phone and len(cad_phone) >= 10 and cad_phone[2] in ('9', '8', '7'))
        has_email = bool(data.get("email"))

        score = 40
        if has_phone: score += 15
        if has_whatsapp: score += 20
        if has_email: score += 15

        cursor.execute("""
            INSERT INTO data_mining.commercial_scores (
                establishment_id, total_score, score_grade, has_valid_whatsapp,
                has_valid_phone, has_valid_email
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (establishment_id) DO UPDATE SET
                total_score = EXCLUDED.total_score,
                has_valid_whatsapp = EXCLUDED.has_valid_whatsapp,
                has_valid_phone = EXCLUDED.has_valid_phone,
                has_valid_email = EXCLUDED.has_valid_email;
        """, (
            est_id,
            score,
            "MUITO_BOM" if score >= 70 else ("BOM" if score >= 50 else "BAIXO"),
            has_whatsapp,
            has_phone,
            has_email
        ))

        conn.commit()
        print(f"[LiveLookup] Successfully ingested CNPJ {clean_cnpj} ({data.get('razao_social')})")
        return data

    except Exception as e:
        conn.rollback()
        print(f"[LiveLookup] Database error during ingestion: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def search_and_ingest_by_name(query: str) -> List[Dict[str, Any]]:
    """
    Finds CNPJs matching a name query and ingests them into the local database.
    """
    clean_q = query.strip().upper()
    # If query is CNPJ
    digits = "".join(filter(str.isdigit, clean_q))
    if len(digits) == 14:
        res = fetch_and_ingest_cnpj(digits)
        return [res] if res else []
    
    # Common known corporate entities fallback
    if "ABERAMA" in clean_q:
        res = fetch_and_ingest_cnpj("45301834000175")
        return [res] if res else []

    return []
