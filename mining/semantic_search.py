import os
import re
import unicodedata
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, List, Optional

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://simplexo:simplexo_secure_pass_2026@localhost:5432/simplexo_data")

def remove_accents(s: str) -> str:
    if not s:
        return ""
    nfkd = unicodedata.normalize('NFKD', s)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

# Sector to CNAE prefix mapping
SECTOR_CNAE_MAP = {
    "software": "620",
    "tecnologia": "620",
    "ti": "620",
    "sistemas": "620",
    "saude": "86",
    "hospital": "861",
    "hospitais": "861",
    "clinica": "863",
    "clinicas": "863",
    "medico": "863",
    "farmacia": "477",
    "farmacias": "477",
    "farmaceutica": "212",
    "farmaceuticos": "212",
    "laboratorios": "212",
    "laboratorio": "212",
    "medicamentos": "212",
    "cosmeticos": "206",
    "cosmetico": "206",
    "perfumaria": "206",
    "embalagens": "222",
    "plastico": "222",
    "construcao": "412",
    "obras": "412",
    "engenharia": "711",
    "transporte": "493",
    "transportes": "493",
    "logistica": "493",
    "frota": "493",
    "alimentos": "109",
    "chocolate": "109",
    "chocolates": "109",
    "cacau": "109",
    "bebidas": "111",
    "restaurante": "561",
    "distribuidora": "46",
    "distribuidoras": "46",
    "comercio atacadista": "46",
    "metalurgica": "25",
    "quimica": "20",
    "energia": "351",
    "solar": "351",
    "consultoria": "702",
    "contabilidade": "692",
    "advocacia": "691",
    "educacao": "85",
    "escola": "851",
    "escolas": "851",
    "faculdade": "853",
    "faculdades": "853"
}

STATE_MAP = {
    "sao paulo": "SP", "sp": "SP",
    "rio de janeiro": "RJ", "rj": "RJ",
    "minas gerais": "MG", "mg": "MG",
    "parana": "PR", "pr": "PR",
    "santa catarina": "SC", "sc": "SC",
    "rio grande do sul": "RS", "rs": "RS",
    "bahia": "BA", "ba": "BA",
    "goias": "GO", "go": "GO",
    "distrito federal": "DF", "brasilia": "DF", "df": "DF",
    "pernambuco": "PE", "pe": "PE",
    "ceara": "CE", "ce": "CE",
    "espirito santo": "ES", "es": "ES",
    "mato grosso": "MT", "mt": "MT",
    "mato grosso do sul": "MS", "ms": "MS",
    "para": "PA", "pa": "PA",
    "amazonas": "AM", "am": "AM"
}

CITY_MAP = {
    "sao paulo": "SAO PAULO",
    "campinas": "CAMPINAS",
    "guarulhos": "GUARULHOS",
    "sao bernardo": "SAO BERNARDO DO CAMPO",
    "santo andre": "SANTO ANDRE",
    "osasco": "OSASCO",
    "ribeirao preto": "RIBEIRAO PRETO",
    "sorocaba": "SOROCABA",
    "rio de janeiro": "RIO DE JANEIRO",
    "niteroi": "NITEROI",
    "belo horizonte": "BELO HORIZONTE",
    "uberlandia": "UBERLANDIA",
    "curitiba": "CURITIBA",
    "londrina": "LONDRINA",
    "maringa": "MARINGA",
    "florianopolis": "FLORIANOPOLIS",
    "joinville": "JOINVILLE",
    "blumenau": "BLUMENAU",
    "porto alegre": "PORTO ALEGRE",
    "caxias do sul": "CAXIAS DO SUL",
    "salvador": "SALVADOR",
    "recife": "RECIFE",
    "fortaleza": "FORTALEZA",
    "goiania": "GOIANIA"
}

def parse_natural_language_query(prompt: str) -> Dict[str, Any]:
    clean_prompt = remove_accents(prompt.lower().strip())
    
    extracted_state = None
    extracted_city = None
    extracted_cnae = None
    extracted_keywords = []
    has_whatsapp_filter = False
    min_score = 0
    revenue_bracket = None
    detected_signals = []

    # 1. Geography extraction
    for city_name, formatted_city in CITY_MAP.items():
        if city_name in clean_prompt:
            extracted_city = formatted_city
            detected_signals.append(f"Cidade: {formatted_city.title()}")
            break

    for state_name, state_code in STATE_MAP.items():
        padded = f" {clean_prompt} "
        if f" {state_name} " in padded or f" em {state_name}" in padded or f" no {state_name}" in padded or f" na {state_name}" in padded or f" de {state_name}" in padded:
            extracted_state = state_code
            detected_signals.append(f"Estado: {state_code}")
            break

    # 2. Sector / Industry extraction
    for sector_key, cnae_prefix in SECTOR_CNAE_MAP.items():
        if sector_key in clean_prompt:
            extracted_cnae = cnae_prefix
            extracted_keywords.append(sector_key)
            detected_signals.append(f"Setor: {sector_key.title()} (CNAE {cnae_prefix})")
            break

    # 3. WhatsApp signal
    if "whatsapp" in clean_prompt or "zap" in clean_prompt:
        has_whatsapp_filter = True
        detected_signals.append("WhatsApp Ativo")

    # 4. Revenue / Size signals
    if "faturamento alto" in clean_prompt or "grande porte" in clean_prompt or "enterprise" in clean_prompt or "milhoes" in clean_prompt:
        revenue_bracket = "GRANDE"
        min_score = max(min_score, 75)
        detected_signals.append("Porte: Grande")
    elif "medio porte" in clean_prompt or "medio" in clean_prompt:
        revenue_bracket = "MEDIO"
        min_score = max(min_score, 60)
        detected_signals.append("Porte: Médio")
    elif "pequeno" in clean_prompt or "epp" in clean_prompt:
        revenue_bracket = "EPP"
        detected_signals.append("Porte: EPP")
    elif "mei" in clean_prompt:
        revenue_bracket = "MEI"
        detected_signals.append("Tipo: MEI")

    # 5. Score Signals
    if "score alto" in clean_prompt or "alta pontuacao" in clean_prompt or "qualificadas" in clean_prompt:
        min_score = max(min_score, 70)
        detected_signals.append("Score Mínimo: 70+")

    tokens = [t for t in re.split(r'[\s,]+', clean_prompt) if len(t) > 3 and t not in {"para", "com", "sem", "mais", "onde", "todas", "empresas", "empresa", "estado", "sao", "paulo", "industrias", "industria"}]
    search_term = " ".join(tokens) if not extracted_cnae else None

    return {
        "raw_prompt": prompt,
        "extracted_state": extracted_state,
        "extracted_city": extracted_city,
        "extracted_cnae": extracted_cnae,
        "search_term": search_term,
        "has_whatsapp": has_whatsapp_filter,
        "revenue_bracket": revenue_bracket,
        "min_score": min_score,
        "detected_signals": detected_signals
    }

def execute_semantic_search(prompt: str, limit: int = 50) -> Dict[str, Any]:
    parsed = parse_natural_language_query(prompt)
    
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            sql = """
                SELECT 
                    e.id, e.cnpj, e.trade_name, c.legal_name, e.city_name, e.state_code,
                    e.cnae_main, e.cnae_main_desc, c.company_size, c.share_capital,
                    COALESCE(s.total_score, 75) as score,
                    COALESCE(s.score_grade, 'BOM') as score_grade,
                    COALESCE(s.has_valid_whatsapp, TRUE) as has_whatsapp,
                    COALESCE(sn.is_simples, FALSE) as is_simples,
                    COALESCE(sn.is_mei, FALSE) as is_mei
                FROM data_core.establishments e
                JOIN data_core.companies c ON c.id = e.company_id
                LEFT JOIN data_core.simples_nacional sn ON sn.cnpj_base = c.cnpj_base
                LEFT JOIN data_mining.commercial_scores s ON s.establishment_id = e.id
                WHERE 1=1
            """
            params = []

            if parsed["extracted_state"]:
                sql += " AND e.state_code = %s"
                params.append(parsed["extracted_state"])

            if parsed["extracted_city"]:
                sql += " AND e.city_name ILIKE %s"
                params.append(f"%{parsed['extracted_city']}%")

            if parsed["extracted_cnae"]:
                sql += " AND e.cnae_main LIKE %s"
                params.append(f"{parsed['extracted_cnae']}%")

            if parsed["search_term"]:
                sql += " AND (e.trade_name ILIKE %s OR c.legal_name ILIKE %s OR e.cnae_main_desc ILIKE %s)"
                params.extend([f"%{parsed['search_term']}%", f"%{parsed['search_term']}%", f"%{parsed['search_term']}%"])

            if parsed["has_whatsapp"]:
                sql += " AND COALESCE(s.has_valid_whatsapp, TRUE) = TRUE"

            if parsed["min_score"] > 0:
                sql += " AND COALESCE(s.total_score, 75) >= %s"
                params.append(parsed["min_score"])

            sql += " ORDER BY COALESCE(s.total_score, 75) DESC, e.updated_at DESC LIMIT %s;"
            params.append(limit)

            cur.execute(sql, tuple(params))
            results = cur.fetchall()

            if not results:
                if parsed["extracted_cnae"]:
                    cur.execute("""
                        SELECT 
                            e.id, e.cnpj, e.trade_name, c.legal_name, e.city_name, e.state_code,
                            e.cnae_main, e.cnae_main_desc, c.company_size, c.share_capital,
                            COALESCE(s.total_score, 75) as score,
                            COALESCE(s.score_grade, 'BOM') as score_grade,
                            COALESCE(s.has_valid_whatsapp, TRUE) as has_whatsapp,
                            COALESCE(sn.is_simples, FALSE) as is_simples,
                            COALESCE(sn.is_mei, FALSE) as is_mei
                        FROM data_core.establishments e
                        JOIN data_core.companies c ON c.id = e.company_id
                        LEFT JOIN data_core.simples_nacional sn ON sn.cnpj_base = c.cnpj_base
                        LEFT JOIN data_mining.commercial_scores s ON s.establishment_id = e.id
                        WHERE e.cnae_main LIKE %s
                        ORDER BY COALESCE(s.total_score, 75) DESC LIMIT %s;
                    """, (f"{parsed['extracted_cnae']}%", limit))
                    results = cur.fetchall()

            for r in results:
                size = r["company_size"]
                if r["is_mei"]:
                    r["revenue_label"] = "Até R$ 81 mil / ano"
                elif size == '01' or r["is_simples"]:
                    r["revenue_label"] = "R$ 360 mil a R$ 4,8 milhões / ano"
                elif size == '05':
                    r["revenue_label"] = "Acima de R$ 10 milhões / ano"
                else:
                    r["revenue_label"] = "R$ 4,8 a R$ 10 milhões / ano"

            return {
                "count": len(results),
                "ai_intent": parsed,
                "detected_signals": parsed["detected_signals"],
                "results": results
            }
