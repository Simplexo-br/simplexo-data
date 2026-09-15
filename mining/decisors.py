"""
Simplexo Data - Decisor Finder & Executive Profiler
Enriches QSA partners and team members with executive role mappings, inferred corporate emails, and LinkedIn discovery links.
"""

import re
import unicodedata
from typing import List, Dict, Any
from mining.email_validator import validate_corporate_email

EXECUTIVE_KEYWORDS = {
    "Socio-Administrador": ["socio", "administrador", "diretor", "ceo"],
    "Presidente": ["presidente", "ceo", "chief executive officer"],
    "Diretor Comercial": ["comercial", "vendas", "sales", "cro"],
    "Diretor Financeiro": ["financeiro", "cfo", "financas"],
    "Diretor de Tecnologia": ["tecnologia", "cto", "ti", "sistemas"],
    "Diretor de Operacoes": ["operacoes", "coo", "operacional"]
}

def normalize_name(name: str) -> str:
    """Removes accents and converts to lowercase ASCII."""
    nfkd = unicodedata.normalize('NFKD', name)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()

def infer_email_patterns(full_name: str, domain: str) -> List[str]:
    """
    Generates standard corporate email patterns:
    - first.last@domain
    - first@domain
    - firstinitial.last@domain
    """
    if not domain or not full_name:
        return []
    
    clean = normalize_name(full_name)
    parts = re.split(r'\s+', clean)
    parts = [p for p in parts if len(p) > 1 and p not in ('de', 'da', 'do', 'dos', 'das', 'e', 'junior', 'filho', 'neto', 'sobrinho')]
    
    if not parts:
        return []
    
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ""
    
    patterns = []
    if last:
        patterns.append(f"{first}.{last}@{domain}")
        patterns.append(f"{first[0]}{last}@{domain}")
        patterns.append(f"{first}_{last}@{domain}")
    patterns.append(f"{first}@{domain}")
    
    return patterns

def profile_decisors(partners_qsa: List[Dict], domain: str = "") -> List[Dict[str, Any]]:
    """
    Enriches QSA partners list with decisor profiles, LinkedIn search URLs and verified email guesses.
    """
    decisors = []
    
    for partner in partners_qsa:
        name = partner.get("name") or partner.get("partner_name", "")
        role = partner.get("role") or partner.get("qualification_desc", "Sócio / Administrador")
        
        if not name:
            continue
            
        inferred_emails = infer_email_patterns(name, domain) if domain else []
        validated_emails = [validate_corporate_email(em) for em in inferred_emails]
        
        linkedin_query = f"https://www.google.com/search?q=site:linkedin.com/in/+{name.replace(' ', '+')}"
        
        decisors.append({
            "name": name,
            "formal_role": role,
            "seniority": "C-Level / Sócio" if any(w in role.lower() for w in ["administrador", "diretor", "presidente", "socio"]) else "Gestão",
            "domain": domain,
            "inferred_emails": validated_emails,
            "linkedin_search_url": linkedin_query
        })
        
    return decisors
