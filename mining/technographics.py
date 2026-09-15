"""
Simplexo Data - Technographics Detection Engine
Analyzes website HTML, scripts, meta tags, and headers to identify business software in use.
"""

import re
from typing import Dict, List, Set

TECH_SIGNATURES = {
    "erp": {
        "TOTVS": [r"totvs", r"protheus", r"datasul", r"rm\.", r"fluig"],
        "SAP": [r"sap-ui", r"sap\.com", r"sapui5", r"sap-client"],
        "Senior": [r"senior\.com\.br", r"senior-sistema", r"seniorx"],
        "Linx": [r"linx\.com\.br", r"linx-commerce", r"linximpulse"],
        "Sankhya": [r"sankhya", r"san-ui"],
        "Omie": [r"omie\.com\.br", r"app\.omie"],
        "Tiny ERP": [r"tiny\.com\.br"],
        "Bling": [r"bling\.com\.br"],
        "Odoo": [r"odoo", r"openerp", r"web\.assets_common", r"web\.assets_frontend"]
    },
    "ecommerce": {
        "VTEX": [r"vtex\.com", r"vteximg\.com\.br", r"vtex-store-header", r"vtex\.render"],
        "Shopify": [r"cdn\.shopify\.com", r"shopify\.com", r"Shopify\.theme"],
        "Nuvemshop": [r"nuvemshop\.com\.br", r"tiendanube\.com", r"d26lpennugtm8s\.cloudfront\.net"],
        "WooCommerce": [r"woocommerce", r"wc-blocks", r"wp-content/plugins/woocommerce"],
        "Magento": [r"magento", r"static/frontend/Magento", r"mage/cookies"],
        "Tray": [r"tray\.com\.br", r"images\.tcdn\.com\.br"],
        "Loja Integrada": [r"lojaintegrada\.com\.br", r"cdn\.awsli\.com\.br"],
        "Wake / Tray Corp": [r"fbits\.com\.br", r"wake\.tech"]
    },
    "marketing_crm": {
        "RD Station": [r"rdstation", r"d335luupugsy2\.cloudfront\.net", r"rd-marketing"],
        "HubSpot": [r"js\.hs-scripts\.com", r"hubspot\.com", r"hs-analytics"],
        "ActiveCampaign": [r"activecampaign\.com", r"trackcmp\.net"],
        "Leadster": [r"leadster\.com\.br", r"squidrf\.leadster"],
        "PipeRun": [r"piperun\.com"],
        "Salesforce": [r"salesforce\.com", r"force\.com", r"pardot\.com"]
    },
    "analytics_tracking": {
        "Google Analytics": [r"google-analytics\.com", r"googletagmanager\.com/gtag", r"ga\('create'"],
        "Google Tag Manager": [r"googletagmanager\.com/gtm\.js"],
        "Meta Pixel": [r"connect\.facebook\.net", r"fbq\('init'"],
        "Hotjar": [r"static\.hotjar\.com", r"hj\("],
        "Clarity": [r"clarity\.ms/tag"]
    },
    "payment_gateway": {
        "Mercado Pago": [r"mercadopago\.com", r"sdk\.mercadopago\.com"],
        "Pagar.me": [r"pagar\.me", r"assets\.pagar\.me"],
        "Asaas": [r"asaas\.com"],
        "Iugu": [r"iugu\.com", r"js\.iugu\.com"],
        "PagBank / PagSeguro": [r"pagseguro\.uol\.com\.br", r"pagbank\.com\.br"],
        "Stripe": [r"js\.stripe\.com"]
    }
}

def detect_technologies(html_content: str, headers: Dict[str, str] = None) -> Dict[str, List[str]]:
    """
    Scans HTML text and HTTP headers for signature footprints of business software.
    Returns categorized detected tools.
    """
    if not html_content:
        return {}
    
    detected: Dict[str, List[str]] = {}
    html_lower = html_content.lower()
    
    # Check server header if present
    header_str = ""
    if headers:
        header_str = " ".join(f"{k}:{v}" for k, v in headers.items()).lower()
    
    combined_content = html_lower + " " + header_str
    
    for category, software_dict in TECH_SIGNATURES.items():
        matched_software = []
        for name, patterns in software_dict.items():
            for pattern in patterns:
                if re.search(pattern, combined_content, re.IGNORECASE):
                    matched_software.append(name)
                    break
        if matched_software:
            detected[category] = matched_software

    return detected
