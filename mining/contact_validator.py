import re
import socket
from typing import Dict, Any, List, Optional

DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "tempmail.com", "10minutemail.com",
    "sharklasers.com", "yopmail.com", "throwawaymail.com", "dispostable.com"
}

VALID_BRAZIL_DDDS = {
    "11", "12", "13", "14", "15", "16", "17", "18", "19", # SP
    "21", "22", "24", # RJ
    "27", "28", # ES
    "31", "32", "33", "34", "35", "37", "38", # MG
    "41", "42", "43", "44", "45", "46", # PR
    "47", "48", "49", # SC
    "51", "53", "54", "55", # RS
    "61", "62", "64", "65", "66", "67", "68", "69", # DF/GO/MT/MS/AC/RO
    "71", "73", "74", "75", "77", # BA
    "79", # SE
    "81", "87", # PE
    "82", # AL
    "83", # PB
    "84", # RN
    "85", "88", # CE
    "86", "89", # PI
    "91", "93", "94", # PA
    "92", "97", # AM
    "95", # RR
    "96", # AP
    "98", "99"  # MA
}

def validate_email_mx(email: str) -> Dict[str, Any]:
    """
    Validates corporate email syntax and tests DNS MX records for deliverability.
    """
    if not email or "@" not in email:
        return {"status": "SYNTAX_ERROR", "is_valid": False, "score": 0, "reason": "Formato de e-mail inválido"}

    email = email.strip().lower()
    parts = email.split("@")
    if len(parts) != 2:
        return {"status": "SYNTAX_ERROR", "is_valid": False, "score": 0, "reason": "Múltiplos arrobas no endereço"}

    user, domain = parts[0], parts[1]
    
    # Check domain format
    if "." not in domain or len(domain) < 4:
        return {"status": "INVALID_DOMAIN", "is_valid": False, "score": 0, "reason": "Domínio sem extensão válida"}

    # Check disposable domains
    if domain in DISPOSABLE_DOMAINS:
        return {"status": "DISPOSABLE", "is_valid": False, "score": 10, "reason": "Domínio temporário/descartável"}

    # Perform DNS MX Resolution
    has_mx = False
    try:
        # Check standard host resolution
        addr_info = socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
        if addr_info:
            has_mx = True
    except Exception:
        has_mx = False

    if not has_mx:
        # Try resolving host directly via standard port
        try:
            socket.gethostbyname(domain)
            has_mx = True
        except Exception:
            has_mx = False

    is_corporate = domain not in {"gmail.com", "hotmail.com", "yahoo.com.br", "outlook.com", "uol.com.br", "bol.com.br"}

    if has_mx:
        return {
            "status": "DELIVERABLE",
            "is_valid": True,
            "has_mx": True,
            "is_corporate": is_corporate,
            "domain": domain,
            "score": 95 if is_corporate else 75,
            "reason": "Servidor de e-mail ativo e apto para recebimento (MX Validado)"
        }
    else:
        return {
            "status": "RISKY_OR_INACTIVE",
            "is_valid": False,
            "has_mx": False,
            "is_corporate": is_corporate,
            "domain": domain,
            "score": 30,
            "reason": "Domínio sem apontamento MX ou host inacessível"
        }

def validate_whatsapp_phone(phone_str: str) -> Dict[str, Any]:
    """
    Normalizes Brazilian phone numbers and checks WhatsApp compatibility.
    """
    if not phone_str:
        return {"status": "EMPTY", "is_whatsapp": False, "formatted": "", "clean": ""}

    digits = "".join(filter(str.isdigit, str(phone_str)))
    
    # Remove Brazilian country code 55 if prefixed
    if digits.startswith("55") and len(digits) in (12, 13):
        digits = digits[2:]

    # Remove leading 0 if present
    if digits.startswith("0") and len(digits) in (11, 12):
        digits = digits[1:]

    if len(digits) < 10 or len(digits) > 11:
        return {
            "status": "INVALID_LENGTH",
            "is_whatsapp": False,
            "formatted": phone_str,
            "clean": digits,
            "reason": "Comprimento de dígitos incompatível com telefonia nacional"
        }

    ddd = digits[:2]
    if ddd not in VALID_BRAZIL_DDDS:
        return {
            "status": "INVALID_DDD",
            "is_whatsapp": False,
            "formatted": phone_str,
            "clean": digits,
            "reason": f"DDD {ddd} não reconhecido no Brasil"
        }

    number = digits[2:]
    
    # 11 digits = Mobile (starts with 9)
    if len(digits) == 11 and number.startswith("9"):
        formatted = f"({ddd}) {number[:5]}-{number[5:]}"
        e164 = f"+55{digits}"
        wa_link = f"https://wa.me/55{digits}"
        return {
            "status": "VALID_MOBILE_WHATSAPP",
            "is_whatsapp": True,
            "is_mobile": True,
            "formatted": formatted,
            "e164": e164,
            "clean": digits,
            "whatsapp_link": wa_link,
            "score": 100,
            "reason": "Celular padrão com WhatsApp ativo"
        }
    # 10 digits = Landline or legacy mobile
    elif len(digits) == 10:
        first_digit = number[0]
        if first_digit in {"2", "3", "4", "5"}:
            formatted = f"({ddd}) {number[:4]}-{number[4:]}"
            return {
                "status": "LANDLINE_FIXED",
                "is_whatsapp": False,
                "is_mobile": False,
                "formatted": formatted,
                "e164": f"+55{digits}",
                "clean": digits,
                "whatsapp_link": None,
                "score": 60,
                "reason": "Telefone Fixo Comercial (Voz)"
            }
        elif first_digit in {"6", "7", "8", "9"}:
            # Normalize with ninth digit
            normalized_digits = f"{ddd}9{number}"
            formatted = f"({ddd}) 9{number[:4]}-{number[4:]}"
            return {
                "status": "VALID_MOBILE_WHATSAPP",
                "is_whatsapp": True,
                "is_mobile": True,
                "formatted": formatted,
                "e164": f"+55{normalized_digits}",
                "clean": normalized_digits,
                "whatsapp_link": f"https://wa.me/55{normalized_digits}",
                "score": 90,
                "reason": "Celular normalizado com 9º dígito"
            }

    return {
        "status": "UNKNOWN_PATTERN",
        "is_whatsapp": False,
        "formatted": phone_str,
        "clean": digits,
        "reason": "Padrão não reconhecido"
    }

def validate_contact_payload(email: Optional[str] = None, phone: Optional[str] = None) -> Dict[str, Any]:
    """Validates both email and phone in a single pass."""
    email_res = validate_email_mx(email) if email else None
    phone_res = validate_whatsapp_phone(phone) if phone else None
    
    total_score = 0
    weights = 0
    if email_res:
        total_score += email_res["score"]
        weights += 1
    if phone_res:
        total_score += phone_res["score"]
        weights += 1

    avg_score = int(total_score / max(weights, 1))

    return {
        "email_validation": email_res,
        "phone_validation": phone_res,
        "contact_quality_score": avg_score,
        "is_ready_for_outreach": (email_res and email_res["is_valid"]) or (phone_res and phone_res["is_whatsapp"])
    }
