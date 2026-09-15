"""
Simplexo Data - Reveal Engine (B2B Website De-anonymization)
Generates client tracking JS and handles IP-to-Company identification.
"""

import re
import socket
from typing import Dict, Any, Optional

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

def resolve_ip_to_host(ip: str) -> Dict[str, Any]:
    """
    Performs reverse DNS resolution to identify organization or ISP.
    """
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return {
            "ip": ip,
            "hostname": host,
            "is_datacenter": any(dc in host for dc in ["aws", "google", "digitalocean", "azure", "cloudflare", "linode"]),
            "resolved": True
        }
    except Exception:
        return {
            "ip": ip,
            "hostname": None,
            "is_datacenter": False,
            "resolved": False
        }
