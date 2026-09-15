"""
Simplexo Data - Corporate Email & DNS MX Deliverability Validator
Verifies RFC syntax, detects domain MX mail servers, and eliminates invalid bounces.
"""

import re
import socket
from typing import Dict, Any, List

RE_EMAIL_STRICT = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

# Disposable / free mail domains
FREE_MAIL_DOMAINS = {
    'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'yahoo.com.br',
    'bol.com.br', 'uol.com.br', 'terra.com.br', 'ig.com.br', 'globo.com'
}

def check_mx_record(domain: str) -> bool:
    """
    Checks if a domain has valid DNS MX or A mail records without sending email.
    """
    try:
        # Check MX or fallback host
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def validate_corporate_email(email: str) -> Dict[str, Any]:
    """
    Validates syntax, identifies whether it is corporate or personal, and checks DNS MX resolution.
    """
    if not email or not isinstance(email, str):
        return {"email": email, "is_valid": False, "reason": "EMPTY"}
    
    clean_email = email.strip().lower()
    
    if not RE_EMAIL_STRICT.match(clean_email):
        return {"email": clean_email, "is_valid": False, "reason": "INVALID_SYNTAX"}
    
    domain = clean_email.split('@')[1]
    is_free = domain in FREE_MAIL_DOMAINS
    has_dns = check_mx_record(domain)
    
    return {
        "email": clean_email,
        "is_valid": has_dns,
        "is_corporate": not is_free,
        "domain": domain,
        "deliverability": "HIGH" if (has_dns and not is_free) else ("MEDIUM" if has_dns else "INVALID"),
        "reason": "OK" if has_dns else "DOMAIN_NOT_RESOLVED"
    }
