// Simplexo Web Copilot Content Script
const CNPJ_REGEX = /\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b/;

function detectPageEntity() {
  const url = window.location.href;
  const text = document.body.innerText || '';

  // 1. Check for CNPJ formatted string in page
  const match = text.match(CNPJ_REGEX);
  if (match) {
    return { detectedEntity: match[0], detectedType: 'CNPJ' };
  }

  // 2. Check LinkedIn Company Page
  if (url.includes('linkedin.com/company/')) {
    const h1 = document.querySelector('h1');
    if (h1 && h1.innerText.trim()) {
      return { detectedEntity: h1.innerText.trim(), detectedType: 'LinkedIn Empresa' };
    }
  }

  // 3. Domain fallback
  const host = window.location.hostname.replace(/^www\./, '');
  if (host && !host.includes('google.') && !host.includes('linkedin.')) {
    return { detectedEntity: host, detectedType: 'Domínio Web' };
  }

  return null;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'GET_PAGE_ENTITIES') {
    const entity = detectPageEntity();
    sendResponse(entity || {});
  }
});
