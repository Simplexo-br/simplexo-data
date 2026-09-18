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

CORPORATE_ENTITY_PATTERNS = [
    r'\bLTDA\b', r'\bS\.?A\.?\b', r'\bS/A\b', r'\bLLC\b', r'\bINC\b', r'\bHOLDING\b',
    r'\bPARTICIPACOES\b', r'\bPARTICIPACAO\b', r'\bINVESTIMENTOS\b', r'\bFUNDO\b',
    r'\bCORP\b', r'\bCORPORATION\b', r'\bGMBH\b', r'\bB\.?V\.?\b', r'\bLIMITED\b',
    r'\bLTD\b', r'\bEIRELI\b', r'\bME\b', r'\bEPP\b', r'\bADMINISTRADORA\b',
    r'\bSERVICOS\b', r'\bINDUSTRIA\b', r'\bCOMERCIO\b', r'\bEMPREENDIMENTOS\b',
    r'\bCONSULTORIA\b', r'\bBANCO\b', r'\bCAPITAL\b', r'\bSECURITIZADORA\b',
    r'\bASSOCIACAO\b', r'\bCOOPERATIVA\b', r'\bLATIN AMERICA\b', r'\bAMERICA LATINA\b',
    r'\bINTERNATIONAL\b', r'\bINTERNACIONAL\b', r'\bGROUP\b', r'\bGRUPO\b'
]

def is_corporate_entity(name: str) -> bool:
    """Detects if a QSA member is a Corporate Entity / Holding / PJ rather than a physical person."""
    if not name:
        return False
    norm = normalize_name(name).upper()
    # Check if contains corporate keywords
    for pat in CORPORATE_ENTITY_PATTERNS:
        if re.search(pat, norm, re.IGNORECASE):
            return True
    # Check if contains digits (e.g. CNPJ formatted)
    if any(c.isdigit() for c in name):
        return True
    return False

def clean_company_for_search(name: str) -> str:
    if not name:
        return ""
    # Normalize accents first
    text = normalize_name(name)
    # Join dotted acronyms like I.B.A.C. -> IBAC
    text = re.sub(r'\b([a-z])\.([a-z])\.', r'\1\2', text)
    text = re.sub(r'\b([a-z])\.', r'\1', text)
    cleaned = re.sub(r'\b(s\.?a\.?|ltda\.?|me|epp|eireli|holding|do brasil|brasil|industria|comercio|servicos|participacoes|empreendimentos|imobiliarios|consultoria|assessoria|administradora|participacao)\b', '', text, flags=re.IGNORECASE)
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', cleaned)
    words = [w.capitalize() for w in cleaned.split() if len(w) > 1 and w.lower() not in ('e', 'de', 'da', 'do', 'dos', 'das')]
    return ' '.join(words[:2]) if words else name.split()[0].capitalize()

def clean_person_for_search(name: str) -> str:
    if not name:
        return ""
    # Normalize accents
    clean = normalize_name(name)
    words = [p.capitalize() for p in clean.split() if len(p) > 1 and p.lower() not in ('de', 'da', 'do', 'dos', 'das', 'e', 'junior', 'filho', 'neto', 'sobrinho')]
    return " ".join(words) if words else name.title()

from mining.linkedin_verifier import (
    extract_concise_name,
    clean_company_keyword,
    generate_linkedin_search_url,
    verify_public_linkedin_profile
)

def profile_decisors(partners_qsa: List[Dict], domain: str = "", company_name: str = "") -> List[Dict[str, Any]]:
    """
    Enriches QSA partners list with decisor profiles, verified direct LinkedIn profiles,
    and high-precision native LinkedIn people searches.
    """
    decisors = []
    
    for partner in partners_qsa:
        name = partner.get("name") or partner.get("partner_name", "")
        role = partner.get("role") or partner.get("qualification_desc", "Sócio / Administrador")
        
        if not name:
            continue
            
        is_pj = is_corporate_entity(name) or any(k in role.lower() for k in ["pessoa juridica", "socio domiciliado no exterior", "socio pj", "entidade"])
        
        clean_person = clean_person_for_search(name)
        concise_name = extract_concise_name(name) if not is_pj else name
        name_parts = clean_person.split()
        is_valid_person = (not is_pj) and len(name_parts) >= 2
        
        inferred_emails = infer_email_patterns(name, domain) if (domain and is_valid_person) else []
        validated_emails = [validate_corporate_email(em) for em in inferred_emails]
        
        # Determine verified LinkedIn direct profile vs native search
        has_verified_linkedin = False
        linkedin_direct_url = None
        linkedin_search_url = ""
        
        if is_valid_person:
            # 1. Check if direct profile already registered in partner record
            raw_linkedin = partner.get("linkedin_url") or partner.get("linkedin")
            if raw_linkedin and "linkedin.com/in/" in raw_linkedin:
                has_verified_linkedin = True
                linkedin_direct_url = raw_linkedin
            
            # 2. Native LinkedIn Search URL (Opens clean inside LinkedIn with concise name)
            linkedin_search_url = generate_linkedin_search_url(name, company_name)
        
        decisors.append({
            "name": name,
            "display_name": concise_name if is_valid_person else name,
            "concise_name": concise_name,
            "formal_role": role,
            "seniority": "Holding / Sócia PJ" if is_pj else ("C-Level / Sócio" if any(w in role.lower() for w in ["administrador", "diretor", "presidente", "socio"]) else "Gestão"),
            "domain": domain,
            "is_person": not is_pj,
            "has_linkedin": has_verified_linkedin,
            "linkedin_url": linkedin_direct_url,
            "linkedin_search_url": linkedin_search_url,
            "inferred_emails": validated_emails,
            "search_query": f"{concise_name} {clean_company_keyword(company_name)}".strip() if is_valid_person else ""
        })
        
    return decisors


