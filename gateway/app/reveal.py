"""
Simplexo Data - Reveal Engine (B2B Website De-anonymization & Visitor Tracking)
Generates client tracking JS, handles IP-to-Company identification, and computes Buying Intent scores.
"""

import re
import time
import socket
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger("simplexo.reveal")

# In-memory store for recent reveal visitor events (cached in gateway memory and synchronized)
_REVEAL_VISITORS_LOG: List[Dict[str, Any]] = [
    {
        "id": "rev-101",
        "company_name": "TOTVS S.A.",
        "cnpj": "53113791000122",
        "domain": "totvs.com.br",
        "location": "São Paulo, SP",
        "page_visited": "/solucoes/enterprise",
        "referrer": "https://www.google.com.br/",
        "buying_intent_score": 92,
        "intent_badge": "ALTA INTENÇÃO",
        "duration_seconds": 185,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "rev-102",
        "company_name": "EMBRAER S.A.",
        "cnpj": "07689002000189",
        "domain": "embraer.com",
        "location": "São José dos Campos, SP",
        "page_visited": "/precos",
        "referrer": "https://br.linkedin.com/",
        "buying_intent_score": 88,
        "intent_badge": "ALTA INTENÇÃO",
        "duration_seconds": 240,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "rev-103",
        "company_name": "WEG EQUIPAMENTOS ELETRICOS S.A.",
        "cnpj": "07175725000100",
        "domain": "weg.net",
        "location": "Jaraguá do Sul, SC",
        "page_visited": "/api/v1/docs",
        "referrer": "Direct",
        "buying_intent_score": 75,
        "intent_badge": "MÉDIA INTENÇÃO",
        "duration_seconds": 95,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
]

PIXEL_JS = """
(function() {
    var endpoint = window.SIMPLEXO_REVEAL_URL || '/api/v1/reveal/identify';
    var payload = {
        url: window.location.href,
        referrer: document.referrer,
        title: document.title,
        screen: window.screen.width + 'x' + window.screen.height,
        timestamp: new Date().toISOString()
    };
    
    if (navigator.sendBeacon) {
        navigator.sendBeacon(endpoint, JSON.stringify(payload));
    } else {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', endpoint, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(payload));
    }
})();
"""

def generate_tracking_snippet(base_url: str = "http://8.234.211.34:8000") -> str:
    """
    Gera o snippet HTML/JS pronto para instalacao no header do website.
    """
    clean_base = base_url.rstrip("/")
    return f'<script src="{clean_base}/api/v1/reveal/pixel.js" async></script>'

def resolve_ip_to_host(ip: str) -> Dict[str, Any]:
    """
    Performs reverse DNS resolution to identify organization or ISP.
    """
    if not ip or ip in ("127.0.0.1", "localhost", "::1"):
        return {
            "ip": ip,
            "hostname": "localhost-test",
            "is_datacenter": False,
            "resolved": True
        }
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return {
            "ip": ip,
            "hostname": host,
            "is_datacenter": any(dc in host.lower() for dc in ["aws", "google", "digitalocean", "azure", "cloudflare", "linode", "oracle"]),
            "resolved": True
        }
    except Exception:
        return {
            "ip": ip,
            "hostname": None,
            "is_datacenter": False,
            "resolved": False
        }

def calculate_intent_score(url: str, referrer: str = "", duration_sec: int = 60) -> Dict[str, Any]:
    """
    Calcula a nota de Intencao de Compra (Buying Intent) do visitante B2B (0 a 100).
    """
    score = 40  # Base score for visit

    # High-intent pages
    high_intent_keywords = ["preco", "pricing", "planos", "contato", "demo", "proposta", "enterprise", "comprar"]
    med_intent_keywords = ["solucoes", "produtos", "funcionalidades", "features", "cases", "api"]

    url_lower = (url or "").lower()
    if any(k in url_lower for k in high_intent_keywords):
        score += 35
    elif any(k in url_lower for k in med_intent_keywords):
        score += 20

    # Referrer bonus
    ref_lower = (referrer or "").lower()
    if "linkedin" in ref_lower or "google" in ref_lower:
        score += 15

    # Duration bonus
    if duration_sec > 120:
        score += 10
    elif duration_sec > 45:
        score += 5

    final_score = min(score, 100)
    badge = "ALTA INTENÇÃO" if final_score >= 80 else ("MÉDIA INTENÇÃO" if final_score >= 60 else "BAIXA INTENÇÃO")

    return {
        "intent_score": final_score,
        "badge": badge
    }

def log_visitor_event(
    company_name: str,
    cnpj: str,
    domain: str,
    location: str,
    page_visited: str,
    referrer: str,
    intent_score: int,
    duration_seconds: int = 60
) -> Dict[str, Any]:
    """
    Registra evento de visitante identificado na memoria/feed do Reveal.
    """
    badge = "ALTA INTENÇÃO" if intent_score >= 80 else ("MÉDIA INTENÇÃO" if intent_score >= 60 else "BAIXA INTENÇÃO")
    record = {
        "id": f"rev-{int(time.time()*1000)}",
        "company_name": company_name,
        "cnpj": cnpj,
        "domain": domain,
        "location": location,
        "page_visited": page_visited,
        "referrer": referrer or "Direct",
        "buying_intent_score": intent_score,
        "intent_badge": badge,
        "duration_seconds": duration_seconds,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
    _REVEAL_VISITORS_LOG.insert(0, record)
    # Keep last 50 events
    if len(_REVEAL_VISITORS_LOG) > 50:
        _REVEAL_VISITORS_LOG.pop()
    return record

def get_recent_identified_visitors() -> List[Dict[str, Any]]:
    return list(_REVEAL_VISITORS_LOG)
