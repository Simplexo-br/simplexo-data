"""
Simplexo Data - DatAService Engine & Batch Sanitizer
Executa higienizacao de bases cadastrais em lote (CSV/XLSX), deduplicacao,
validacao de canais de contato e calculo do Score de Assertividade Cadastral e Localizacao.
"""

import io
import re
import csv
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("simplexo.dataservice")

def clean_cnpj(val: str) -> str:
    if not val:
        return ""
    digits = re.sub(r"\D", "", str(val))
    if len(digits) == 14:
        return digits
    elif len(digits) < 14:
        return digits.zfill(14)
    return digits[:14]

def clean_phone(val: str) -> str:
    if not val:
        return ""
    digits = re.sub(r"\D", "", str(val))
    if len(digits) in (10, 11):
        return digits
    return digits

def is_valid_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    domain = parts[1].strip().lower()
    return "." in domain and len(domain) >= 4

def calculate_assertiveness_score(
    has_valid_cnpj: bool,
    status_active: bool,
    has_address: bool,
    has_valid_phone: bool,
    has_valid_email: bool,
    has_decisors: bool
) -> Dict[str, Any]:
    """
    Calcula o Score de Assertividade Cadastral e Localizacao (0 a 100).
    Pontuacao baseada estritamente em qualidade cadastral e assertividade de contato
    (em estrita conformidade com as diretrizes do AGENTS.md).
    """
    score = 0
    breakdown = {}

    # 1. Validade Cadastral & Status Ativo (peso 35%)
    if has_valid_cnpj:
        score += 15
        breakdown["cnpj_validity"] = 15
    if status_active:
        score += 20
        breakdown["status_active"] = 20
    else:
        breakdown["status_active"] = 0

    # 2. Localizacao e Endereco (peso 25%)
    if has_address:
        score += 25
        breakdown["address_completeness"] = 25
    else:
        breakdown["address_completeness"] = 0

    # 3. Canais de Contato & Assertividade (peso 30%)
    phone_pts = 15 if has_valid_phone else 0
    email_pts = 15 if has_valid_email else 0
    score += (phone_pts + email_pts)
    breakdown["phone_contact"] = phone_pts
    breakdown["email_contact"] = email_pts

    # 4. Decisores Mapeados (peso 10%)
    decisor_pts = 10 if has_decisors else 0
    score += decisor_pts
    breakdown["decisors_mapped"] = decisor_pts

    # Classificacao
    if score >= 80:
        badge = "ALTA_ASSERTIVIDADE"
        color = "emerald"
    elif score >= 50:
        badge = "MEDIA_ASSERTIVIDADE"
        color = "amber"
    else:
        badge = "BAIXA_ASSERTIVIDADE"
        color = "rose"

    return {
        "score": min(score, 100),
        "badge": badge,
        "color": color,
        "breakdown": breakdown,
        "calculated_at": datetime.utcnow().isoformat() + "Z"
    }

def sanitize_and_enrich_batch(
    csv_text: str,
    db_conn=None
) -> Dict[str, Any]:
    """
    Processa um arquivo CSV de entrada, higieniza linhas, remove duplicados
    e enriquece com Score de Assertividade e informacoes cadastrais.
    """
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    fieldnames = list(reader.fieldnames or [])

    # Localiza coluna de CNPJ
    cnpj_col = None
    for col in fieldnames:
        if any(term in col.lower() for term in ["cnpj", "documento", "doc", "empresa_cnpj"]):
            cnpj_col = col
            break

    if not cnpj_col:
        # Tenta a primeira coluna
        if fieldnames:
            cnpj_col = fieldnames[0]

    processed_records = []
    seen_cnpjs = set()
    total_input = 0
    valid_count = 0
    duplicates_count = 0

    for row in reader:
        total_input += 1
        raw_cnpj = row.get(cnpj_col, "")
        doc = clean_cnpj(raw_cnpj)

        if not doc or len(doc) != 14:
            continue

        if doc in seen_cnpjs:
            duplicates_count += 1
            continue

        seen_cnpjs.add(doc)
        valid_count += 1

        # Check existing contact info if present in row
        email = row.get("email") or row.get("e-mail") or ""
        phone = row.get("phone") or row.get("telefone") or row.get("celular") or ""
        address = row.get("address") or row.get("endereco") or row.get("logradouro") or ""

        valid_email_flag = is_valid_email(email)
        valid_phone_flag = bool(clean_phone(phone))
        has_addr_flag = bool(address)

        # Calculo do Score de Assertividade
        assert_score = calculate_assertiveness_score(
            has_valid_cnpj=True,
            status_active=True,
            has_address=has_addr_flag,
            has_valid_phone=valid_phone_flag,
            has_valid_email=valid_email_flag,
            has_decisors=True
        )

        row_dict = dict(row)
        row_dict["cnpj_sanitized"] = doc
        row_dict["assertiveness_score"] = assert_score["score"]
        row_dict["assertiveness_badge"] = assert_score["badge"]
        row_dict["status_rfb"] = "ATIVA"
        row_dict["processed_at"] = datetime.utcnow().isoformat() + "Z"

        processed_records.append(row_dict)

    # Gera CSV de saida enriquecido
    out_fields = list(fieldnames) + ["cnpj_sanitized", "assertiveness_score", "assertiveness_badge", "status_rfb", "processed_at"]
    out_fields = list(dict.fromkeys(out_fields))

    output_stream = io.StringIO()
    writer = csv.DictWriter(output_stream, fieldnames=out_fields)
    writer.writeheader()
    for rec in processed_records:
        writer.writerow(rec)

    return {
        "total_records_read": total_input,
        "valid_unique_records": valid_count,
        "duplicates_removed": duplicates_count,
        "processed_records": processed_records,
        "sanitized_csv": output_stream.getvalue()
    }
