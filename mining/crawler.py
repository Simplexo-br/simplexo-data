"""
Simplexo Data - Web Crawler & Contact Mining Engine
Visits corporate websites and extracts phones, WhatsApps, emails, social networks, and software stack (Technographics).
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Set, Optional
from mining.technographics import detect_technologies

# Regex Patterns for Brazilian Contacts
RE_EMAIL = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
RE_PHONE_BR = re.compile(r'(?:\+?55\s?)?(?:\(?([1-9]{2})\)?\s?)?(?:(9\d{4})|(\d{4}))[-\s]?(\d{4})')
RE_WHATSAPP_LINK = re.compile(r'(?:api\.whatsapp\.com/send\?phone=|wa\.me/)(\+?\d+)')
RE_SOCIAL = {
    'linkedin': re.compile(r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[a-zA-Z0-9_-]+'),
    'instagram': re.compile(r'https?://(?:www\.)?instagram\.com/[a-zA-Z0-9_.-]+'),
    'facebook': re.compile(r'https?://(?:www\.)?facebook\.com/[a-zA-Z0-9_.-]+')
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 SimplexoBot/1.0'
}

def clean_phone(phone_str: str) -> str:
    """Normalize phone string into numeric E.164-like Brazilian format."""
    digits = re.sub(r'\D', '', phone_str)
    if digits.startswith('55') and len(digits) >= 12:
        return digits
    elif len(digits) in (10, 11):
        return f"55{digits}"
    return digits

def crawl_company_website(url: str, max_depth: int = 2) -> Dict:
    """
    Crawls the homepage and key pages (contato, sobre, quem-somos) of a company website.
    Extracts contacts, social networks and detects technographic stack.
    """
    if not url.startswith('http'):
        url = 'https://' + url

    domain = urlparse(url).netloc
    visited_urls: Set[str] = set()
    to_visit: List[str] = [url]
    
    extracted = {
        'website': url,
        'domain': domain,
        'phones': set(),
        'whatsapps': set(),
        'emails': set(),
        'socials': {},
        'technologies': {}
    }

    subpages_patterns = ['contato', 'fale-conosco', 'sobre', 'empresa', 'quem-somos', 'contact', 'about', 'equipe']

    try:
        while to_visit and len(visited_urls) < 5:
            current_url = to_visit.pop(0)
            if current_url in visited_urls:
                continue
            visited_urls.add(current_url)

            try:
                resp = requests.get(current_url, headers=HEADERS, timeout=10, allow_redirects=True)
                if resp.status_code != 200:
                    continue
            except Exception:
                continue

            # Detect technologies on homepage or pages visited
            page_tech = detect_technologies(resp.text, dict(resp.headers))
            for cat, techs in page_tech.items():
                if cat not in extracted['technologies']:
                    extracted['technologies'][cat] = []
                for t in techs:
                    if t not in extracted['technologies'][cat]:
                        extracted['technologies'][cat].append(t)

            soup = BeautifulSoup(resp.text, 'html.parser')
            text_content = soup.get_text(separator=' ')

            # 1. Extract Emails
            for email in RE_EMAIL.findall(text_content):
                clean_em = email.lower()
                if not any(clean_em.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']) and 'example' not in clean_em:
                    extracted['emails'].add(clean_em)

            # 2. Extract WhatsApp from links (href="https://wa.me/...")
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                wa_match = RE_WHATSAPP_LINK.search(href)
                if wa_match:
                    num = clean_phone(wa_match.group(1))
                    if len(num) in (12, 13):
                        extracted['whatsapps'].add(num)

                # Social profiles
                for network, reg in RE_SOCIAL.items():
                    if network not in extracted['socials']:
                        soc_match = reg.search(href)
                        if soc_match:
                            extracted['socials'][network] = soc_match.group(0)

                # Find internal subpages for deeper crawling
                for sub in subpages_patterns:
                    if sub in href.lower():
                        full_sub_url = urljoin(url, href)
                        if urlparse(full_sub_url).netloc == domain and full_sub_url not in visited_urls:
                            to_visit.append(full_sub_url)

            # 3. Extract Phones from text
            for phone_match in RE_PHONE_BR.finditer(text_content):
                raw_phone = phone_match.group(0)
                norm = clean_phone(raw_phone)
                if len(norm) in (12, 13): # 55 + DDD + 8/9 digits
                    if len(norm) == 13 and norm[4] == '9':
                        extracted['whatsapps'].add(norm)
                    else:
                        extracted['phones'].add(norm)

    except Exception as e:
        print(f"[Crawler] Error crawling {url}: {e}")

    return {
        'website': extracted['website'],
        'domain': extracted['domain'],
        'phones': sorted(list(extracted['phones'])),
        'whatsapps': sorted(list(extracted['whatsapps'])),
        'emails': sorted(list(extracted['emails'])),
        'socials': extracted['socials'],
        'technologies': extracted['technologies']
    }

if __name__ == "__main__":
    test_result = crawl_company_website("https://simplexo.com.br")
    print("Crawl result:", test_result)
