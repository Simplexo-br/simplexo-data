"""
Simplexo Data - Commercial Quality Scoring Engine
Calculates lead qualification score (0-100) based on verified channels and decisors.
"""

from typing import Dict, Any

def calculate_commercial_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scoring Criteria:
      - WhatsApp confirmado/válido: +30
      - Telefone válido:            +20
      - E-mail corporativo válido:  +20
      - Decisor identificado:       +15
      - Site ativo/encontrado:      +10
      - Dados recentes (<30 dias):  +5
      
    Grades:
      - 90–100: EXCELENTE
      - 70–89:  MUITO_BOM
      - 50–69:  BOM
      - 30–49:  BAIXO
      - 0–29:   MUITO_BAIXO
    """
    total_score = 0
    breakdown = {}

    has_valid_whatsapp = bool(data.get("whatsapps"))
    has_valid_phone = bool(data.get("phones") or data.get("cadastral_phone_1"))
    has_valid_email = bool(data.get("emails") or data.get("cadastral_email"))
    has_website = bool(data.get("website") or data.get("digital_footprint", {}).get("website_url"))
    has_decision_maker = bool(data.get("decision_makers") or data.get("has_decision_maker"))
    is_fresh = bool(data.get("is_fresh", True))

    if has_valid_whatsapp:
        total_score += 30
        breakdown["whatsapp"] = 30

    if has_valid_phone:
        total_score += 20
        breakdown["phone"] = 20

    if has_valid_email:
        total_score += 20
        breakdown["email"] = 20

    if has_decision_maker:
        total_score += 15
        breakdown["decision_maker"] = 15

    if has_website:
        total_score += 10
        breakdown["website"] = 10

    if is_fresh:
        total_score += 5
        breakdown["freshness"] = 5

    total_score = min(total_score, 100)

    if total_score >= 90:
        grade = "EXCELENTE"
    elif total_score >= 70:
        grade = "MUITO_BOM"
    elif total_score >= 50:
        grade = "BOM"
    elif total_score >= 30:
        grade = "BAIXO"
    else:
        grade = "MUITO_BAIXO"

    return {
        "total_score": total_score,
        "score_grade": grade,
        "has_valid_whatsapp": has_valid_whatsapp,
        "has_valid_phone": has_valid_phone,
        "has_valid_email": has_valid_email,
        "has_website": has_website,
        "has_decision_maker": has_decision_maker,
        "score_breakdown": breakdown
    }
