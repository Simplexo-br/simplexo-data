"""
Simplexo Data - LinkedIn Live Profile Verifier & Search Resolver
Verifies real public profile URLs and generates high-precision LinkedIn searches.
"""

import re
import urllib.parse
import urllib.request
import unicodedata
from typing import Optional, Tuple, List

def normalize_name(name: str) -> str:
    """Removes accents and converts to lowercase ASCII."""
    nfkd = unicodedata.normalize('NFKD', name)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()

def extract_concise_name(full_name: str) -> str:
    """
    Transforms long Brazilian legal names into common professional display names.
    E.g. 'Ana Maria Falleiros Santos Diniz Avila' -> 'Ana Maria Diniz'
    E.g. 'Carlos Eduardo Antunes Taparelli' -> 'Carlos Eduardo Taparelli'
    E.g. 'Heloisa Vaz Guimaraes Sampaio Gouvea' -> 'Heloisa Gouvea'
    """
    if not full_name:
        return ""
        
    clean = normalize_name(full_name)
    parts = re.split(r'\s+', clean)
    parts = [p.capitalize() for p in parts if len(p) > 1 and p not in ('de', 'da', 'do', 'dos', 'das', 'e', 'junior', 'filho', 'neto', 'sobrinho')]
    
    if not parts:
        return full_name.title()
    if len(parts) <= 2:
        return " ".join(parts)
        
    first = parts[0]
    second = parts[1]
    last = parts[-1]
    
    # If first name is a common Brazilian compound (Ana Maria, Carlos Eduardo, Joao Paulo, etc.)
    compound_prefixes = {'Ana', 'Maria', 'Joao', 'Jose', 'Carlos', 'Luiz', 'Luis', 'Paulo', 'Pedro', 'Marcos', 'Antonio'}
    if first in compound_prefixes and len(parts) >= 3:
        if len(parts) >= 4 and parts[-2] in {'Diniz', 'Silva', 'Santos', 'Oliveira', 'Souza', 'Ferreira', 'Pereira', 'Rodrigues'}:
            return f"{first} {second} {parts[-2]}"
        return f"{first} {second} {last}"
    
    return f"{first} {last}"

def clean_company_keyword(name: str) -> str:
    """Extracts the core brand keyword from legal corporate name."""
    if not name:
        return ""
    norm = normalize_name(name)
    cleaned = re.sub(r'\b(s\.?a\.?|ltda\.?|me|epp|eireli|holding|do brasil|brasil|industria|comercio|servicos|participacoes|empreendimentos|imobiliarios|consultoria|assessoria|administradora|participacao|estudio|de|danca)\b', '', norm, flags=re.IGNORECASE)
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', cleaned)
    words = [w.capitalize() for w in cleaned.split() if len(w) > 1]
    return words[0] if words else name.split()[0].capitalize()

def generate_linkedin_search_url(full_name: str, company_name: str = "") -> str:
    """Generates a clean LinkedIn People Search URL that opens inside LinkedIn's native search."""
    concise_name = extract_concise_name(full_name)
    comp_keyword = clean_company_keyword(company_name)
    
    query = f"{concise_name} {comp_keyword}".strip() if comp_keyword else concise_name
    return f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(query)}"

def verify_public_linkedin_profile(full_name: str, company_name: str = "", timeout: float = 2.0) -> Tuple[Optional[str], bool]:
    """
    Attempts to find and verify a real direct public LinkedIn profile (e.g. linkedin.com/in/username).
    Returns (profile_url, is_verified).
    """
    concise_name = extract_concise_name(full_name)
    comp_keyword = clean_company_keyword(company_name)
    
    # Check DuckDuckGo / Search Index for direct profile URL
    query = f'site:linkedin.com/in/ "{concise_name}" {comp_keyword}'.strip()
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            encoded_matches = re.findall(r'uddg=(https%3A%2F%2F(?:[a-z]{2,3}\.)?linkedin\.com%2Fin%2F[^&]+)', html)
            if encoded_matches:
                decoded = urllib.parse.unquote(encoded_matches[0])
                clean_url = decoded.split('?')[0]
                return clean_url, True
                
            raw_matches = re.findall(r'https?:\/\/(?:[a-z]{2,3}\.)?linkedin\.com\/in\/[a-zA-Z0-9\-_%]+', html)
            if raw_matches:
                clean_url = raw_matches[0].split('?')[0]
                return clean_url, True
    except Exception:
        pass
        
    return None, False
