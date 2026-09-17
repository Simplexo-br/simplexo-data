const API_BASE = 'http://8.234.211.34:8000';
let currentCompany = null;

document.addEventListener('DOMContentLoaded', async () => {
  const searchInput = document.getElementById('copilot-search-input');
  const btnLoadDetected = document.getElementById('btn-load-detected');
  const btnExportCrm = document.getElementById('btn-export-crm');
  const btnOpenStation = document.getElementById('btn-open-station');

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const q = searchInput.value.trim();
      if (q) performLookup(q);
    }
  });

  if (btnLoadDetected) {
    btnLoadDetected.addEventListener('click', () => {
      const target = btnLoadDetected.getAttribute('data-target');
      if (target) performLookup(target);
    });
  }

  if (btnExportCrm) {
    btnExportCrm.addEventListener('click', async () => {
      if (!currentCompany) return;
      btnExportCrm.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Enviando...';
      try {
        const res = await fetch(`${API_BASE}/api/v1/export/crm/direct`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ leads: [currentCompany] })
        });
        const d = await res.json();
        if (res.ok) {
          btnExportCrm.innerHTML = '<i class="fa-solid fa-check"></i> Lead Enviado com Sucesso!';
          btnExportCrm.style.background = '#059669';
        }
      } catch (err) {
        btnExportCrm.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Erro ao exportar';
      }
    });
  }

  if (btnOpenStation) {
    btnOpenStation.addEventListener('click', () => {
      if (!currentCompany) return;
      const url = `${API_BASE}/?search=${encodeURIComponent(currentCompany.cnpj || currentCompany.company_name)}`;
      chrome.tabs.create({ url: url });
    });
  }

  // Check active tab content
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.id) {
      chrome.tabs.sendMessage(tab.id, { action: 'GET_PAGE_ENTITIES' }, (response) => {
        if (chrome.runtime.lastError) return;
        if (response && response.detectedEntity) {
          const banner = document.getElementById('active-page-banner');
          const nameEl = document.getElementById('detected-entity-name');
          nameEl.innerText = `${response.detectedType}: ${response.detectedEntity}`;
          btnLoadDetected.setAttribute('data-target', response.detectedEntity);
          banner.classList.remove('hidden');
        }
      });
    }
  } catch (e) {
    console.log('Tab query info:', e);
  }
});

async function performLookup(query) {
  const loading = document.getElementById('loading-state');
  const card = document.getElementById('company-card');
  const welcome = document.getElementById('welcome-state');

  loading.classList.remove('hidden');
  card.classList.add('hidden');
  welcome.classList.add('hidden');

  try {
    const res = await fetch(`${API_BASE}/api/v1/extension/copilot/lookup?q=${encodeURIComponent(query)}`);
    const data = await res.json();

    loading.classList.add('hidden');
    if (res.ok && data.success && data.company) {
      renderCompany(data.company);
    } else {
      welcome.innerHTML = `<i class="fa-solid fa-magnifying-glass" style="font-size: 28px; color: #ef4444; margin-bottom: 8px;"></i><h4 style="color:#991b1b;">Nenhum registro encontrado</h4><p style="font-size:11px;">Tente buscar pelo CNPJ completo ou Razão Social exata.</p>`;
      welcome.classList.remove('hidden');
    }
  } catch (err) {
    loading.classList.add('hidden');
    welcome.innerHTML = `<i class="fa-solid fa-triangle-exclamation" style="font-size: 28px; color: #f59e0b; margin-bottom: 8px;"></i><h4 style="color:#b45309;">Erro de Conexão com Gateway</h4><p style="font-size:11px;">Verifique se o Simplexo Data Station está ativo em ${API_BASE}.</p>`;
    welcome.classList.remove('hidden');
  }
}

function renderCompany(c) {
  currentCompany = c;
  const card = document.getElementById('company-card');
  document.getElementById('comp-name').innerText = c.company_name || c.trade_name || 'Razão Social';
  document.getElementById('comp-cnpj').innerText = c.cnpj || '00.000.000/0000-00';
  document.getElementById('comp-status').innerText = c.status || 'ATIVA';
  document.getElementById('comp-porte').innerText = `Porte: ${c.size || 'Demais'}`;
  document.getElementById('comp-fat').innerText = c.estimated_revenue || 'R$ 5M - 20M';
  document.getElementById('comp-cnae').innerText = c.cnae_main ? `${c.cnae_main.slice(0,25)}...` : 'Atividade Comercial';
  document.getElementById('comp-location').innerText = `${c.city || 'São Paulo'} - ${c.state || 'SP'}`;

  // WhatsApp wa.me
  const rawPhone = (c.phone || '11999999999').replace(/\D/g, '');
  const cleanPhone = rawPhone.length === 10 || rawPhone.length === 11 ? '55' + rawPhone : rawPhone;
  const btnWa = document.getElementById('btn-direct-wa');
  btnWa.href = `https://wa.me/${cleanPhone}?text=${encodeURIComponent('Olá, gostaria de falar com a diretoria da ' + (c.company_name || 'empresa'))}`;

  // E-mail
  document.getElementById('comp-email-tag').innerHTML = `<i class="fa-solid fa-envelope"></i> ${c.email || 'contato@' + (c.domain || 'empresa.com.br')}`;

  // Partners / QSA
  const partnersContainer = document.getElementById('partners-list');
  partnersContainer.innerHTML = '';
  const partners = c.partners || [{ name: 'Sócio / Administrador', role: 'Diretor Geral' }];
  partners.slice(0, 3).forEach(p => {
    const pName = p.name || 'Sócio Administrador';
    const pRole = p.role || 'Sócio';
    const linkedinUrl = `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(pName + ' ' + (c.company_name || ''))}`;
    
    const pDiv = document.createElement('div');
    pDiv.className = 'partner-item';
    pDiv.innerHTML = `
      <div>
        <div style="font-weight:700; color:#1e293b;">${pName}</div>
        <div style="font-size:10px; color:#64748b;">${pRole}</div>
      </div>
      <a href="${linkedinUrl}" target="_blank" class="btn-linkedin"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
    `;
    partnersContainer.appendChild(pDiv);
  });

  card.classList.remove('hidden');
}
