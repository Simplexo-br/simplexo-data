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

import urllib.parse

def clean_company_for_search(name: str) -> str:
    if not name:
        return ""
    # Join dotted acronyms like I.B.A.C. -> IBAC
    text = re.sub(r'\b([A-Za-z])\.([A-Za-z])\.', r'\1\2', name)
    text = re.sub(r'\b([A-Za-z])\.', r'\1', text)
    cleaned = re.sub(r'\b(S\.?A\.?|LTDA\.?|ME|EPP|EIRELI|HOLDING|DO BRASIL|BRASIL|INDUSTRIA|COMERCIO|SERVICOS|PARTICIPACOES)\b', '', text, flags=re.IGNORECASE)
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', cleaned)
    words = [w.capitalize() for w in cleaned.split() if len(w) > 1 or w.isupper()]
    return ' '.join(words[:2]) if words else name.split()[0]

def clean_person_for_search(name: str) -> str:
    if not name:
        return ""
    parts = [p.capitalize() for p in name.split() if len(p) > 1 and p.lower() not in ('de', 'da', 'do', 'dos', 'das', 'e', 'junior', 'filho', 'neto', 'sobrinho')]
    if len(parts) >= 2:
        return f"{parts[0]} {parts[-1]}"
    return name.title()

def profile_decisors(partners_qsa: List[Dict], domain: str = "", company_name: str = "") -> List[Dict[str, Any]]:
    """
    Enriches QSA partners list with decisor profiles, high-precision LinkedIn people search URLs and verified email guesses.
    """
    decisors = []
    clean_company = clean_company_for_search(company_name)
    
    for partner in partners_qsa:
        name = partner.get("name") or partner.get("partner_name", "")
        role = partner.get("role") or partner.get("qualification_desc", "Sócio / Administrador")
        
        if not name:
            continue
            
        inferred_emails = infer_email_patterns(name, domain) if domain else []
        validated_emails = [validate_corporate_email(em) for em in inferred_emails]
        
        # High Precision Clean Search: "Mariela Palacios Almapal"
        clean_person = clean_person_for_search(name)
        search_query = f"{clean_person} {clean_company}".strip()
        linkedin_direct_url = f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(search_query)}"
        
        decisors.append({
            "name": name,
            "display_name": clean_person,
            "formal_role": role,
            "seniority": "C-Level / Sócio" if any(w in role.lower() for w in ["administrador", "diretor", "presidente", "socio"]) else "Gestão",
            "domain": domain,
            "inferred_emails": validated_emails,
            "linkedin_search_url": linkedin_direct_url
        })
        
    return decisors
