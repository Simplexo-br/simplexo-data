import os

html_code = """<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950 text-slate-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simplexo Data — Plataforma de Inteligência B2B & Oportunidades</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome 6 Pro Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Chart.js for High-End Analytics -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        brand: {
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.6); }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(51, 65, 85, 0.8); border-radius: 9999px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.8); }
        .glass-panel { background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(51, 65, 85, 0.4); }
        .glass-card { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(8px); border: 1px solid rgba(51, 65, 85, 0.3); }
        .glass-card:hover { border-color: rgba(99, 102, 241, 0.5); }
    </style>
</head>
<body class="h-full bg-slate-950 text-slate-100 flex flex-col antialiased selection:bg-indigo-500 selection:text-white">

    <!-- TOAST NOTIFICATION CONTAINER -->
    <div id="toast-container" class="fixed top-5 right-5 z-50 space-y-2 pointer-events-none"></div>

    <!-- 1. LOGIN SCREEN -->
    <div id="login-view" class="min-h-full flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950/40">
        <!-- Background Ambient Glows -->
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="max-w-md w-full glass-panel rounded-3xl p-8 shadow-2xl relative z-10 border border-slate-800/80">
            <div class="text-center space-y-2 mb-8">
                <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-600 to-blue-500 text-white shadow-xl shadow-indigo-500/25 text-2xl font-black mb-2">
                    <i class="fa-solid fa-cube"></i>
                </div>
                <h1 class="text-2xl font-black tracking-tight text-white">Simplexo Data</h1>
                <p class="text-xs text-slate-400 font-medium">Plataforma Soberana de Inteligência B2B & Oportunidades</p>
            </div>

            <form onsubmit="handleLogin(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1.5">E-mail Corporativo</label>
                    <div class="relative">
                        <i class="fa-solid fa-envelope absolute left-3.5 top-3 text-slate-500 text-xs"></i>
                        <input id="login-email" type="email" required value="admin@simplexo.com.br"
                            class="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-9 pr-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1.5">Senha de Acesso</label>
                    <div class="relative">
                        <i class="fa-solid fa-lock absolute left-3.5 top-3 text-slate-500 text-xs"></i>
                        <input id="login-password" type="password" required value="simplexo2026"
                            class="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-9 pr-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition">
                    </div>
                </div>

                <div class="flex items-center justify-between text-[11px] pt-1">
                    <label class="flex items-center text-slate-400 cursor-pointer">
                        <input type="checkbox" checked class="rounded bg-slate-900 border-slate-700 text-indigo-600 focus:ring-0 mr-1.5">
                        Lembrar sessão
                    </label>
                    <a href="#" class="text-indigo-400 hover:text-indigo-300 font-medium">Esqueceu a senha?</a>
                </div>

                <button type="submit"
                    class="w-full py-3 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-indigo-600/25 transition duration-150 flex items-center justify-center space-x-2">
                    <span>Entrar na Plataforma</span>
                    <i class="fa-solid fa-arrow-right text-xs"></i>
                </button>
            </form>

            <div class="mt-6 pt-6 border-t border-slate-800/80 text-center">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse mr-1.5"></span>
                    Base Conectada: 50.39M CNPJs Ativos
                </span>
            </div>
        </div>
    </div>

    <!-- 2. MAIN APPLICATION VIEW -->
    <div id="app-view" class="hidden min-h-full flex flex-col">
        
        <!-- TOP NAVIGATION BAR -->
        <header class="glass-panel sticky top-0 z-40 border-b border-slate-800/80">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
                <!-- LOGO & BADGE -->
                <div class="flex items-center space-x-3 cursor-pointer" onclick="switchTab('dashboard')">
                    <div class="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 text-white shadow-md shadow-indigo-500/20 font-black text-lg">
                        S
                    </div>
                    <div>
                        <div class="flex items-center space-x-2">
                            <span class="font-extrabold text-white tracking-tight text-sm">Simplexo Data</span>
                            <span class="px-2 py-0.5 text-[10px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full">Station 2.0</span>
                        </div>
                        <p class="text-[10px] text-slate-400">Inteligência B2B & Oportunidades</p>
                    </div>
                </div>

                <!-- NAVIGATION TABS -->
                <nav class="hidden lg:flex items-center space-x-1">
                    <button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-white bg-slate-800 border border-slate-700 transition">
                        <i class="fa-solid fa-chart-pie mr-1.5 text-indigo-400"></i> Visão Geral
                    </button>
                    <button onclick="switchTab('prospecting')" id="nav-prospecting" class="nav-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition">
                        <i class="fa-solid fa-magnifying-glass mr-1.5 text-blue-400"></i> Prospecção B2B
                    </button>
                    <button onclick="switchTab('recent')" id="nav-recent" class="nav-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-emerald-300 hover:text-white hover:bg-slate-800/60 transition">
                        <i class="fa-solid fa-bolt mr-1.5 text-emerald-400"></i> Recém-Abertas
                    </button>
                    <button onclick="switchTab('cno')" id="nav-cno" class="nav-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-amber-300 hover:text-white hover:bg-slate-800/60 transition">
                        <i class="fa-solid fa-trowel-bricks mr-1.5 text-amber-400"></i> Obras & CNO
                    </button>
                    <button onclick="switchTab('batch')" id="nav-batch" class="nav-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition">
                        <i class="fa-solid fa-file-csv mr-1.5 text-teal-400"></i> Enriquecimento em Lote
                    </button>
                    <button onclick="switchTab('reveal')" id="nav-reveal" class="nav-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition">
                        <i class="fa-solid fa-satellite-dish mr-1.5 text-purple-400"></i> Reveal
                    </button>
                    <button onclick="switchTab('plans')" id="nav-plans" class="nav-btn px-3 py-1.5 rounded-xl text-xs font-bold text-amber-300 hover:text-white hover:bg-amber-500/20 bg-amber-500/10 border border-amber-500/30 transition">
                        <i class="fa-solid fa-gem mr-1.5 text-amber-400 animate-pulse"></i> Planos & Loja
                    </button>
                </nav>

                <!-- RIGHT WIDGETS -->
                <div class="flex items-center space-x-3">
                    <div class="hidden sm:flex items-center px-3 py-1.5 bg-amber-500/10 border border-amber-500/20 rounded-xl text-xs text-amber-300 font-bold">
                        <i class="fa-solid fa-bolt mr-1.5 text-amber-400"></i>
                        <span id="header-user-credits">2.500 Créditos</span>
                    </div>
                    <div class="hidden md:flex items-center px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-300">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 mr-2"></span>
                        <span id="header-total-companies">50.396.768 Empresas</span>
                    </div>
                    <button onclick="handleLogout()" class="text-xs font-semibold text-slate-400 hover:text-red-400 px-3 py-1.5 rounded-xl hover:bg-slate-900 transition">
                        <i class="fa-solid fa-arrow-right-from-bracket mr-1"></i> Sair
                    </button>
                </div>
            </div>
        </header>

        <!-- MAIN BODY CONTAINER -->
        <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
            
            <!-- TAB 1: VISÃO GERAL / DASHBOARD -->
            <section id="view-dashboard" class="space-y-6">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="glass-card rounded-2xl p-5 hover:border-slate-700 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-semibold text-slate-400">Empresas Cadastradas</span>
                            <div class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-sm">
                                <i class="fa-solid fa-building"></i>
                            </div>
                        </div>
                        <div class="mt-3">
                            <span id="dash-total-companies" class="text-2xl font-black text-white">50.396.768</span>
                            <span class="block text-[11px] text-emerald-400 mt-0.5"><i class="fa-solid fa-arrow-up mr-1"></i>Base Oficial RFB Atualizada</span>
                        </div>
                    </div>

                    <div class="glass-card rounded-2xl p-5 hover:border-slate-700 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-semibold text-slate-400">Microempreendedores (MEIs)</span>
                            <div class="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center text-sm">
                                <i class="fa-solid fa-user-check"></i>
                            </div>
                        </div>
                        <div class="mt-3">
                            <span id="dash-total-meis" class="text-2xl font-black text-white">17.523.665</span>
                            <span class="block text-[11px] text-blue-400 mt-0.5">34.8% da Base Nacional</span>
                        </div>
                    </div>

                    <div class="glass-card rounded-2xl p-5 hover:border-slate-700 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-semibold text-slate-400">Obras Ativas (CNO)</span>
                            <div class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center text-sm">
                                <i class="fa-solid fa-trowel-bricks"></i>
                            </div>
                        </div>
                        <div class="mt-3">
                            <span class="text-2xl font-black text-white">1.842.910</span>
                            <span class="block text-[11px] text-amber-400 mt-0.5">Canteiros & Reformas no Brasil</span>
                        </div>
                    </div>

                    <div class="glass-card rounded-2xl p-5 hover:border-slate-700 transition">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-semibold text-slate-400">WhatsApps & E-mails Válidos</span>
                            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-sm">
                                <i class="fa-brands fa-whatsapp"></i>
                            </div>
                        </div>
                        <div class="mt-3">
                            <span class="text-2xl font-black text-emerald-400">Alta Qualificação</span>
                            <span class="block text-[11px] text-slate-400 mt-0.5">Validação DNS MX & Celulares</span>
                        </div>
                    </div>
                </div>

                <!-- ANALYTICS CHARTS (CHART.JS) -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="glass-card rounded-2xl p-5 lg:col-span-2">
                        <div class="flex items-center justify-between mb-4">
                            <div>
                                <h3 class="text-sm font-bold text-white">Distribuição Geográfica de Empresas (Top Estados)</h3>
                                <p class="text-[11px] text-slate-400">Concentração de empresas ativas por unidade federativa</p>
                            </div>
                            <span class="text-xs font-mono text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded-lg">Brasil</span>
                        </div>
                        <div class="h-64">
                            <canvas id="chart-geo"></canvas>
                        </div>
                    </div>

                    <div class="glass-card rounded-2xl p-5">
                        <div class="flex items-center justify-between mb-4">
                            <div>
                                <h3 class="text-sm font-bold text-white">Faixa de Faturamento Presumido</h3>
                                <p class="text-[11px] text-slate-400">Proporção por porte econômico</p>
                            </div>
                        </div>
                        <div class="h-64">
                            <canvas id="chart-revenue"></canvas>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TAB 2: PROSPECÇÃO B2B -->
            <section id="view-prospecting" class="hidden space-y-6">
                <div class="glass-card rounded-2xl p-6 space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
                        <div class="flex items-center space-x-2">
                            <i class="fa-solid fa-sliders text-indigo-400 text-sm"></i>
                            <h3 class="text-sm font-bold text-white">Filtros de Segmentação e ICP</h3>
                        </div>
                        <button onclick="clearSearchFilters()" class="text-xs text-slate-400 hover:text-white transition">
                            <i class="fa-solid fa-rotate-left mr-1"></i> Limpar Filtros
                        </button>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-400 mb-1">Razão Social / Fantasia / CNPJ</label>
                            <input id="filter-q" type="text" placeholder="Ex: Aberama Brasil, TOTVS, 45301834..."
                                class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500">
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-400 mb-1">Estado (UF)</label>
                            <select id="filter-state" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500">
                                <option value="">Todos os Estados</option>
                                <option value="SP">São Paulo (SP)</option>
                                <option value="MG">Minas Gerais (MG)</option>
                                <option value="RJ">Rio de Janeiro (RJ)</option>
                                <option value="PR">Paraná (PR)</option>
                                <option value="RS">Rio Grande do Sul (RS)</option>
                                <option value="SC">Santa Catarina (SC)</option>
                                <option value="BA">Bahia (BA)</option>
                                <option value="GO">Goiás (GO)</option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-400 mb-1">Faturamento Estimado</label>
                            <select id="filter-faturamento" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500">
                                <option value="">Todas as Faixas</option>
                                <option value="ATE_360K">Até R$ 360 mil (ME / MEI)</option>
                                <option value="360K_A_4_8M">R$ 360 mil a R$ 4,8 milhões (EPP)</option>
                                <option value="4_8M_A_16M">R$ 4,8 milhões a R$ 16 milhões (Médio)</option>
                                <option value="16M_A_90M">R$ 16 milhões a R$ 90 milhões (Grande)</option>
                                <option value="ACIMA_90M">Acima de R$ 90 milhões (Enterprise)</option>
                            </select>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-400 mb-1">Score Comercial Mínimo</label>
                            <select id="filter-score" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500">
                                <option value="0">Qualquer Score (0–100)</option>
                                <option value="40">Score &gt;= 40 (Médio)</option>
                                <option value="60">Score &gt;= 60 (Bom)</option>
                                <option value="75">Score &gt;= 75 (Muito Bom / Alta Conversão)</option>
                            </select>
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-2">
                        <label class="flex items-center text-xs text-slate-300 font-semibold cursor-pointer">
                            <input id="filter-whatsapp" type="checkbox" class="rounded bg-slate-950 border-slate-700 text-indigo-600 focus:ring-0 mr-2">
                            <i class="fa-brands fa-whatsapp text-emerald-400 mr-1.5 text-sm"></i> Apenas com WhatsApp Validado
                        </label>

                        <button onclick="executeSearch()" class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-md transition flex items-center">
                            <i class="fa-solid fa-magnifying-glass mr-2"></i> Filtrar Empresas
                        </button>
                    </div>
                </div>

                <div class="glass-card rounded-2xl overflow-hidden shadow-sm">
                    <div class="p-4 border-b border-slate-800/80 flex items-center justify-between">
                        <span id="results-count" class="text-xs font-bold text-white">Resultados</span>
                        <div class="flex space-x-2">
                            <button onclick="exportSearchResults('csv')" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-lg text-xs font-semibold transition border border-slate-700">
                                <i class="fa-solid fa-file-csv mr-1 text-teal-400"></i> Exportar CSV
                            </button>
                            <button onclick="exportSearchResults('xlsx')" class="px-3 py-1.5 bg-emerald-600/10 hover:bg-emerald-600 text-emerald-400 hover:text-white rounded-lg text-xs font-semibold transition border border-emerald-500/20">
                                <i class="fa-solid fa-file-excel mr-1"></i> Exportar Excel
                            </button>
                        </div>
                    </div>

                    <div class="overflow-x-auto custom-scrollbar">
                        <table class="w-full text-left text-xs text-slate-300">
                            <thead class="bg-slate-900/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                                <tr>
                                    <th class="p-3.5">Empresa / Razão Social</th>
                                    <th class="p-3.5">Localização</th>
                                    <th class="p-3.5">CNAE Principal</th>
                                    <th class="p-3.5">Faturamento Estimado</th>
                                    <th class="p-3.5">Qualificação & Score</th>
                                    <th class="p-3.5 text-right">Ação</th>
                                </tr>
                            </thead>
                            <tbody id="search-table-body" class="divide-y divide-slate-800/60"></tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- TAB 3: OPORTUNIDADES RECÉM-ABERTAS -->
            <section id="view-recent" class="hidden space-y-6">
                <div class="glass-card rounded-2xl p-6">
                    <div class="flex items-center justify-between mb-4 pb-3 border-b border-slate-800/80">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center">
                                <i class="fa-solid fa-bolt text-emerald-400 mr-2"></i> Empresas Recém-Abertas (Novas Oportunidades)
                            </h3>
                            <p class="text-xs text-slate-400 mt-0.5">Aborde empresas abertas nos últimos 30 dias antes dos seus concorrentes.</p>
                        </div>
                        <button onclick="loadRecentOpportunities()" class="text-xs font-semibold px-3 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-xl hover:bg-emerald-500/20 transition">
                            <i class="fa-solid fa-arrows-rotate mr-1"></i> Atualizar Feed
                        </button>
                    </div>

                    <div class="overflow-x-auto custom-scrollbar">
                        <table class="w-full text-left text-xs text-slate-300">
                            <thead class="bg-slate-900/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                                <tr>
                                    <th class="p-3.5">Empresa / CNPJ</th>
                                    <th class="p-3.5">Cidade - UF</th>
                                    <th class="p-3.5">Atividade Econômica</th>
                                    <th class="p-3.5">Porte</th>
                                    <th class="p-3.5">Score</th>
                                    <th class="p-3.5 text-right">Ação Rápida</th>
                                </tr>
                            </thead>
                            <tbody id="recent-table-body" class="divide-y divide-slate-800/60"></tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- TAB 4: OBRAS & CNO -->
            <section id="view-cno" class="hidden space-y-6">
                <div class="glass-card rounded-2xl p-6 space-y-4">
                    <div class="flex items-center justify-between pb-3 border-b border-slate-800/80">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center">
                                <i class="fa-solid fa-trowel-bricks text-amber-400 mr-2"></i> Cadastro Nacional de Obras (CNO) & Canteiros Ativos
                            </h3>
                            <p class="text-xs text-slate-400 mt-0.5">Oportunidades em canteiros de obras, construções e reformas civis em todo o Brasil.</p>
                        </div>
                        <span class="px-3 py-1 text-[11px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-lg">
                            Receita Federal CNO
                        </span>
                    </div>

                    <div id="cno-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
                </div>
            </section>

            <!-- TAB 5: ENRIQUECIMENTO EM LOTE -->
            <section id="view-batch" class="hidden space-y-6">
                <div class="glass-panel rounded-2xl p-8 max-w-3xl mx-auto space-y-6">
                    <div class="text-center space-y-2">
                        <div class="w-12 h-12 rounded-2xl bg-teal-500/10 text-teal-400 flex items-center justify-center mx-auto text-xl">
                            <i class="fa-solid fa-file-excel"></i>
                        </div>
                        <h3 class="text-lg font-bold text-white">Enriquecimento em Lote (Planilha CSV)</h3>
                        <p class="text-xs text-slate-400">Faça upload de uma lista de CNPJs para preencher automaticamente telefones, WhatsApps validados, sócios, e-mails e faturamento.</p>
                    </div>

                    <div id="drop-zone" class="border-2 border-dashed border-slate-700 hover:border-teal-500 rounded-2xl p-8 text-center cursor-pointer transition bg-slate-950/40"
                        onclick="document.getElementById('csv-file-input').click()">
                        <input id="csv-file-input" type="file" accept=".csv,.txt" class="hidden" onchange="handleCSVSelect(event)">
                        <i class="fa-solid fa-cloud-arrow-up text-3xl text-slate-500 mb-3"></i>
                        <p id="file-name-label" class="text-xs font-semibold text-slate-300">Clique para selecionar ou arraste o arquivo CSV aqui</p>
                        <p class="text-[11px] text-slate-500 mt-1">Formato: 1 CNPJ por linha ou coluna CNPJ</p>
                    </div>

                    <button id="btn-process-batch" onclick="processBatchUpload()" disabled
                        class="w-full py-3 bg-teal-600 disabled:bg-slate-800 disabled:text-slate-600 hover:bg-teal-500 text-white text-xs font-bold rounded-xl shadow-lg transition flex items-center justify-center">
                        <i class="fa-solid fa-bolt mr-2"></i> Iniciar Enriquecimento em Alta Velocidade
                    </button>

                    <div id="batch-results-area" class="hidden space-y-4 pt-4 border-t border-slate-800">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-white"><span id="batch-processed-count">0</span> Empresas Enriquecidas</span>
                            <button onclick="downloadBatchResults()" class="text-xs font-semibold text-teal-400 bg-teal-500/10 border border-teal-500/20 px-3 py-1.5 rounded-lg hover:bg-teal-500/20">
                                <i class="fa-solid fa-download mr-1"></i> Baixar Planilha Pronta
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TAB 6: SIMPLEXO REVEAL -->
            <section id="view-reveal" class="hidden space-y-6">
                <div class="glass-card rounded-2xl p-6 space-y-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-base font-bold text-white flex items-center">
                                <i class="fa-solid fa-satellite-dish text-purple-400 mr-2"></i> Simplexo Reveal — Visitantes B2B em Tempo Real
                            </h3>
                            <p class="text-xs text-slate-400 mt-0.5">Identifique quais empresas estão visitando seu site institucional ou e-commerce.</p>
                        </div>
                        <span class="px-2.5 py-1 text-[11px] font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded-lg animate-pulse">
                            Live Stream
                        </span>
                    </div>

                    <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-300">
                        <div class="flex justify-between items-center mb-2 pb-2 border-b border-slate-800 text-slate-400 font-semibold text-[11px]">
                            <span>Código de Rastreio (&lt;head&gt;):</span>
                            <button onclick="copyRevealSnippet()" class="text-indigo-400 hover:text-indigo-300"><i class="fa-solid fa-copy mr-1"></i>Copiar</button>
                        </div>
                        <code id="reveal-snippet">&lt;script src="http://8.234.211.34:8000/api/v1/reveal/pixel.js" async&gt;&lt;/script&gt;</code>
                    </div>
                </div>
            </section>

            <!-- TAB 7: PLANOS & LOJA -->
            <section id="view-plans" class="hidden space-y-8 pb-12">
                <div class="text-center max-w-3xl mx-auto space-y-3">
                    <div class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 mb-1">
                        <i class="fa-solid fa-sparkles mr-1.5"></i> Planos Comerciais & Créditos
                    </div>
                    <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight">Escolha o plano ideal para acelerar seu pipeline de vendas</h2>
                    <p class="text-xs sm:text-sm text-slate-400">Tenha acesso a 50+ milhões de CNPJs, dados de sócios (QSA), validação de WhatsApp, faturamento estimado e obras CNO.</p>
                    
                    <div class="inline-flex items-center p-1 bg-slate-900 border border-slate-800 rounded-xl mt-4">
                        <button id="btn-billing-monthly" onclick="setBillingCycle('monthly')" class="px-4 py-2 rounded-lg text-xs font-bold transition bg-indigo-600 text-white shadow">
                            Cobrança Mensal
                        </button>
                        <button id="btn-billing-annual" onclick="setBillingCycle('annual')" class="px-4 py-2 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white flex items-center">
                            Cobrança Anual
                            <span class="ml-2 px-2 py-0.5 text-[10px] font-black bg-emerald-500 text-slate-950 rounded-full">33% OFF + 2x Créditos</span>
                        </button>
                    </div>
                </div>

                <div id="plans-grid" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4"></div>
            </section>
        </main>
    </div>

    <!-- DRAWER: COMPANY 360 -->
    <div id="company-modal" class="hidden fixed inset-0 z-50 overflow-hidden">
        <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="closeCompanyModal()"></div>
        <div class="absolute inset-y-0 right-0 max-w-2xl w-full bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col">
            <div class="p-6 border-b border-slate-800 flex items-start justify-between bg-slate-950/40">
                <div>
                    <span id="modal-cnpj" class="text-xs font-mono font-bold text-indigo-400">CNPJ: 00.000.000/0000-00</span>
                    <h2 id="modal-trade-name" class="text-xl font-black text-white mt-0.5">Razão / Nome Fantasia</h2>
                    <p id="modal-legal-name" class="text-xs text-slate-400">Razão Social Completa</p>
                </div>
                <button onclick="closeCompanyModal()" class="text-slate-500 hover:text-white p-2 rounded-lg text-lg">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <div class="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                <div class="flex flex-wrap gap-2">
                    <span id="modal-status-badge" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">ATIVA</span>
                    <span id="modal-simples-badge" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">Simples Nacional</span>
                    <span id="modal-score-badge" class="px-2.5 py-1 text-xs font-bold rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20">Score: 85</span>
                </div>

                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                    <span class="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Estimativa Econômica & Porte</span>
                    <div class="grid grid-cols-2 gap-4 pt-1">
                        <div>
                            <span class="text-[11px] text-slate-500">Faturamento Presumido</span>
                            <p id="modal-rev-label" class="text-xs font-bold text-white">R$ 360 mil a R$ 4,8 milhões / ano</p>
                        </div>
                        <div>
                            <span class="text-[11px] text-slate-500">Quadro de Colaboradores</span>
                            <p id="modal-emp-label" class="text-xs font-bold text-white">6 a 19 colaboradores</p>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-3 gap-3">
                    <a id="modal-btn-whatsapp" href="#" target="_blank" class="flex items-center justify-center py-2.5 px-3 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl shadow-lg transition">
                        <i class="fa-brands fa-whatsapp text-sm mr-1.5"></i> WhatsApp
                    </a>
                    <a id="modal-btn-call" href="#" class="flex items-center justify-center py-2.5 px-3 bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold rounded-xl border border-slate-700 transition">
                        <i class="fa-solid fa-phone text-xs mr-1.5 text-blue-400"></i> Ligar
                    </a>
                    <button id="modal-btn-crm" onclick="exportCurrentToCRM()" class="flex items-center justify-center py-2.5 px-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-lg transition">
                        <i class="fa-solid fa-paper-plane mr-1.5"></i> CRM / Odoo
                    </button>
                </div>

                <div class="space-y-3">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center">
                        <i class="fa-solid fa-user-tie mr-2 text-indigo-400"></i> Decisores & Sócios (QSA)
                    </span>
                    <div id="modal-decisors-list" class="space-y-2"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: SUBSCRIBE CHECKOUT -->
    <div id="subscribe-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onclick="closeSubscribeModal()"></div>
        <div class="relative bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-5">
            <div class="flex items-center justify-between border-b border-slate-800 pb-4">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center text-lg">
                        <i class="fa-solid fa-gem"></i>
                    </div>
                    <div>
                        <h3 id="sub-modal-title" class="text-base font-bold text-white">Assinar Plano</h3>
                        <p id="sub-modal-price" class="text-xs text-amber-400 font-bold">R$ 149 / mês</p>
                    </div>
                </div>
                <button onclick="closeSubscribeModal()" class="text-slate-500 hover:text-white">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <div class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 font-semibold mb-1">Empresa / Razão Social</label>
                    <input id="sub-company" type="text" value="Simplexo Data Cliente" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-indigo-500">
                </div>
                <div>
                    <label class="block text-slate-400 font-semibold mb-1">E-mail Corporativo</label>
                    <input id="sub-email" type="email" value="admin@simplexo.com.br" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-indigo-500">
                </div>
                <div>
                    <label class="block text-slate-400 font-semibold mb-1">Forma de Pagamento</label>
                    <div class="grid grid-cols-2 gap-2">
                        <label class="flex items-center p-2.5 bg-slate-950 border border-indigo-500/40 rounded-lg cursor-pointer">
                            <input type="radio" name="payment_method" checked class="text-indigo-600 focus:ring-0">
                            <span class="ml-2 text-white font-semibold flex items-center"><i class="fa-solid fa-credit-card mr-1.5 text-indigo-400"></i> Cartão (2x Cotas)</span>
                        </label>
                        <label class="flex items-center p-2.5 bg-slate-950 border border-slate-800 rounded-lg cursor-pointer">
                            <input type="radio" name="payment_method" class="text-indigo-600 focus:ring-0">
                            <span class="ml-2 text-slate-300 font-semibold flex items-center"><i class="fa-brands fa-pix mr-1.5 text-emerald-400"></i> Pix</span>
                        </label>
                    </div>
                </div>
            </div>

            <div class="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl flex items-center space-x-2.5 text-xs text-emerald-400">
                <i class="fa-solid fa-shield-check text-base"></i>
                <span>Garantia incondicional de 8 dias com liberação imediata de créditos.</span>
            </div>

            <div class="flex space-x-3 pt-2">
                <button onclick="closeSubscribeModal()" class="flex-1 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold rounded-xl transition">
                    Cancelar
                </button>
                <button id="btn-confirm-sub" onclick="confirmSubscription()" class="flex-1 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-lg transition flex items-center justify-center">
                    <i class="fa-solid fa-check mr-1.5"></i> Confirmar Assinatura
                </button>
            </div>
        </div>
    </div>

    <!-- CLIENT SCRIPT -->
    <script>
        let currentBatchData = [];
        let plansCatalog = [];
        let currentBillingCycle = 'monthly';
        let selectedPlanId = null;
        let activeCompanyProfile = null;
        let lastSearchResults = [];

        function showToast(msg, type = 'success') {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            const bgClass = type === 'success' ? 'bg-emerald-600' : (type === 'error' ? 'bg-red-600' : 'bg-indigo-600');
            toast.className = `${bgClass} text-white px-4 py-3 rounded-xl shadow-xl text-xs font-bold flex items-center space-x-2 transition-all transform translate-y-0 opacity-100 pointer-events-auto`;
            toast.innerHTML = `<i class="fa-solid fa-circle-check"></i><span>${msg}</span>`;
            container.appendChild(toast);
            setTimeout(() => {
                toast.classList.add('opacity-0', 'translate-y-2');
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        function handleLogin(e) {
            e.preventDefault();
            document.getElementById('login-view').classList.add('hidden');
            document.getElementById('app-view').classList.remove('hidden');
            loadDashboardStats();
            initCharts();
            executeSearch();
            loadRecentOpportunities();
            loadCNOOpportunities();
            loadPlans();
            showToast("Sessão iniciada com sucesso!");
        }

        function handleLogout() {
            document.getElementById('app-view').classList.add('hidden');
            document.getElementById('login-view').classList.remove('hidden');
        }

        function switchTab(tabId) {
            ['dashboard', 'prospecting', 'recent', 'cno', 'batch', 'reveal', 'plans'].forEach(t => {
                const view = document.getElementById('view-' + t);
                const nav = document.getElementById('nav-' + t);
                if (view) view.classList.add('hidden');
                if (nav) {
                    nav.classList.remove('bg-slate-800', 'text-white', 'border', 'border-slate-700');
                    nav.classList.add('text-slate-300');
                }
            });

            const targetView = document.getElementById('view-' + tabId);
            const targetNav = document.getElementById('nav-' + tabId);
            if (targetView) targetView.classList.remove('hidden');
            if (targetNav) {
                targetNav.classList.add('bg-slate-800', 'text-white', 'border', 'border-slate-700');
                targetNav.classList.remove('text-slate-300');
            }
        }

        async function loadDashboardStats() {
            try {
                const res = await fetch('/api/v1/stats');
                const data = await res.json();
                if (data.total_companies) {
                    document.getElementById('dash-total-companies').innerText = Number(data.total_companies || 50396768).toLocaleString('pt-BR');
                    document.getElementById('dash-total-meis').innerText = Number(data.total_meis || 17523665).toLocaleString('pt-BR');
                }
            } catch (err) {
                console.error("Stats load error:", err);
            }
        }

        let geoChartInstance = null;
        let revChartInstance = null;

        async function initCharts() {
            try {
                const res = await fetch('/api/v1/dashboard/charts');
                const data = await res.json();

                // Geo Chart
                const geoCtx = document.getElementById('chart-geo').getContext('2d');
                if (geoChartInstance) geoChartInstance.destroy();
                geoChartInstance = new Chart(geoCtx, {
                    type: 'bar',
                    data: {
                        labels: data.geo_distribution.map(d => d.uf),
                        datasets: [{
                            label: 'Empresas (Milhões)',
                            data: data.geo_distribution.map(d => (d.count / 1000000).toFixed(2)),
                            backgroundColor: '#6366f1',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            x: { grid: { color: 'rgba(51, 65, 85, 0.2)' }, ticks: { color: '#94a3b8' } },
                            y: { grid: { color: 'rgba(51, 65, 85, 0.2)' }, ticks: { color: '#94a3b8' } }
                        }
                    }
                });

                // Revenue Chart
                const revCtx = document.getElementById('chart-revenue').getContext('2d');
                if (revChartInstance) revChartInstance.destroy();
                revChartInstance = new Chart(revCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['ME / MEI', 'EPP', 'Médio', 'Grande', 'Enterprise'],
                        datasets: [{
                            data: [75.8, 17.6, 4.2, 1.8, 0.6],
                            backgroundColor: ['#6366f1', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'bottom', labels: { color: '#94a3b8', boxWidth: 10, font: { size: 10 } } }
                        }
                    }
                });
            } catch (err) {
                console.error("Charts init error:", err);
            }
        }

        async function executeSearch() {
            const q = document.getElementById('filter-q').value;
            const state = document.getElementById('filter-state').value;
            const faturamento = document.getElementById('filter-faturamento').value;
            const minScore = document.getElementById('filter-score').value;
            const hasWhatsApp = document.getElementById('filter-whatsapp').checked;

            let url = `/api/v1/search?limit=50&min_score=${minScore}`;
            if (q) url += `&q=${encodeURIComponent(q)}`;
            if (state) url += `&state=${encodeURIComponent(state)}`;
            if (faturamento) url += `&faturamento_faixa=${encodeURIComponent(faturamento)}`;
            if (hasWhatsApp) url += `&has_whatsapp=true`;

            try {
                const res = await fetch(url);
                const data = await res.json();
                lastSearchResults = data.results || [];
                renderSearchResults(lastSearchResults);
            } catch (err) {
                console.error("Search error:", err);
            }
        }

        function clearSearchFilters() {
            document.getElementById('filter-q').value = '';
            document.getElementById('filter-state').value = '';
            document.getElementById('filter-faturamento').value = '';
            document.getElementById('filter-score').value = '0';
            document.getElementById('filter-whatsapp').checked = false;
            executeSearch();
        }

        function renderSearchResults(items) {
            document.getElementById('results-count').innerText = `${items.length} Empresas Encontradas`;
            const tbody = document.getElementById('search-table-body');
            tbody.innerHTML = '';

            if (items.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="p-6 text-center text-slate-500">Nenhuma empresa encontrada com os filtros selecionados.</td></tr>`;
                return;
            }

            items.forEach(emp => {
                const scoreColor = emp.score >= 70 ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' : (emp.score >= 40 ? 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20' : 'text-slate-400 bg-slate-800 border-slate-700');
                const row = document.createElement('tr');
                row.className = "hover:bg-slate-900/60 transition";
                row.innerHTML = `
                    <td class="p-3.5">
                        <div class="font-bold text-white">${emp.trade_name || emp.legal_name}</div>
                        <div class="text-[11px] font-mono text-slate-500">${emp.cnpj}</div>
                    </td>
                    <td class="p-3.5">
                        <span class="px-2 py-0.5 rounded bg-slate-950 text-slate-300 font-medium">${emp.city_name} - ${emp.state_code}</span>
                    </td>
                    <td class="p-3.5 font-mono text-slate-400">${emp.cnae_main || 'N/D'}</td>
                    <td class="p-3.5">
                        <span class="text-slate-300 font-medium">${emp.estimated_metrics ? emp.estimated_metrics.revenue_label : 'N/D'}</span>
                    </td>
                    <td class="p-3.5">
                        <div class="flex items-center space-x-2">
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded border ${scoreColor}">Score: ${emp.score}</span>
                            ${emp.has_whatsapp ? '<i class="fa-brands fa-whatsapp text-emerald-400 text-sm" title="WhatsApp Validado"></i>' : ''}
                            ${emp.has_email ? '<i class="fa-solid fa-envelope text-blue-400 text-sm" title="E-mail Válido"></i>' : ''}
                        </div>
                    </td>
                    <td class="p-3.5 text-right space-x-1">
                        <button onclick="openCompanyModal('${emp.cnpj}')" class="px-3 py-1.5 bg-indigo-600/10 hover:bg-indigo-600 text-indigo-400 hover:text-white border border-indigo-500/20 rounded-lg text-xs font-semibold transition">
                            Company 360
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }

        async function loadRecentOpportunities() {
            try {
                const res = await fetch('/api/v1/opportunities/recent-companies');
                const data = await res.json();
                const tbody = document.getElementById('recent-table-body');
                tbody.innerHTML = '';

                (data.opportunities || []).forEach(emp => {
                    const row = document.createElement('tr');
                    row.className = "hover:bg-slate-900/60 transition";
                    row.innerHTML = `
                        <td class="p-3.5">
                            <div class="font-bold text-white">${emp.trade_name || emp.legal_name}</div>
                            <div class="text-[11px] font-mono text-emerald-400">${emp.cnpj}</div>
                        </td>
                        <td class="p-3.5 text-slate-300">${emp.city_name} - ${emp.state_code}</td>
                        <td class="p-3.5 font-mono text-slate-400">${emp.cnae_main || 'Comércio / Serviços'}</td>
                        <td class="p-3.5 text-slate-300 font-medium">${emp.company_size || 'EPP'}</td>
                        <td class="p-3.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Score: ${emp.score}</span></td>
                        <td class="p-3.5 text-right">
                            <button onclick="openCompanyModal('${emp.cnpj}')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition">
                                Qualificar Lead
                            </button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            } catch (err) {
                console.error("Recent opportunities error:", err);
            }
        }

        async function loadCNOOpportunities() {
            try {
                const res = await fetch('/api/v1/opportunities/cno-obras');
                const data = await res.json();
                const grid = document.getElementById('cno-grid');
                grid.innerHTML = '';

                (data.obras || []).forEach(o => {
                    const card = document.createElement('div');
                    card.className = "bg-slate-950 p-5 rounded-2xl border border-slate-800/80 hover:border-amber-500/40 transition space-y-3";
                    card.innerHTML = `
                        <div class="flex items-start justify-between">
                            <span class="px-2 py-0.5 text-[10px] font-mono font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 rounded-lg">${o.cno_id}</span>
                            <span class="px-2 py-0.5 text-[10px] font-bold text-emerald-400 bg-emerald-500/10 rounded-full">${o.situacao.split(' ')[0]}</span>
                        </div>
                        <div>
                            <h4 class="text-sm font-bold text-white">${o.nome_obra}</h4>
                            <p class="text-[11px] text-slate-400">${o.tipo_obra}</p>
                        </div>
                        <div class="grid grid-cols-2 gap-2 text-[11px] bg-slate-900/60 p-2.5 rounded-xl">
                            <div><span class="text-slate-500 block">Área Total:</span><span class="font-bold text-white">${o.area_total_m2} m²</span></div>
                            <div><span class="text-slate-500 block">Investimento:</span><span class="font-bold text-amber-400">${o.valor_estimado}</span></div>
                        </div>
                        <div class="text-[11px] text-slate-300">
                            <i class="fa-solid fa-location-dot mr-1 text-slate-500"></i> ${o.bairro}, ${o.cidade} - ${o.uf}
                        </div>
                        <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                            <span class="text-[10px] font-mono text-slate-400">${o.cnpj_executora}</span>
                            <a href="https://wa.me/55${o.whatsapp_contato}" target="_blank" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition flex items-center">
                                <i class="fa-brands fa-whatsapp mr-1"></i> Contato
                            </a>
                        </div>
                    `;
                    grid.appendChild(card);
                });
            } catch (err) {
                console.error("CNO load error:", err);
            }
        }

        async function openCompanyModal(cnpj) {
            try {
                const res = await fetch(`/api/v1/company/${cnpj}`);
                const data = await res.json();
                activeCompanyProfile = data;
                const p = data.profile;
                const e = data.estimated_economics;

                document.getElementById('modal-cnpj').innerText = `CNPJ: ${p.cnpj}`;
                document.getElementById('modal-trade-name').innerText = p.trade_name || p.legal_name;
                document.getElementById('modal-legal-name').innerText = p.legal_name;

                if (e) {
                    document.getElementById('modal-rev-label').innerText = e.revenue_label;
                    document.getElementById('modal-emp-label').innerText = e.employee_label;
                }

                // WhatsApp button
                const btnWa = document.getElementById('modal-btn-whatsapp');
                if (p.cadastral_phone_1) {
                    btnWa.href = `https://wa.me/55${p.cadastral_phone_1}`;
                    btnWa.classList.remove('opacity-50', 'pointer-events-none');
                } else {
                    btnWa.classList.add('opacity-50', 'pointer-events-none');
                }

                // Decisors list
                const decisorsContainer = document.getElementById('modal-decisors-list');
                decisorsContainer.innerHTML = '';
                if (data.decisors && data.decisors.length > 0) {
                    data.decisors.forEach(d => {
                        decisorsContainer.innerHTML += `
                            <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
                                <div>
                                    <span class="font-bold text-white">${d.name}</span>
                                    <p class="text-[11px] text-slate-400">${d.formal_role} &bull; <span class="text-indigo-400">${d.seniority}</span></p>
                                </div>
                                <a href="${d.linkedin_search_url}" target="_blank" class="px-2.5 py-1 bg-indigo-600/10 hover:bg-indigo-600 text-indigo-400 hover:text-white border border-indigo-500/20 rounded-lg text-[11px] font-semibold transition">
                                    <i class="fa-brands fa-linkedin mr-1"></i> LinkedIn
                                </a>
                            </div>
                        `;
                    });
                } else {
                    decisorsContainer.innerHTML = `<p class="text-xs text-slate-500">Nenhum sócio mapeado.</p>`;
                }

                document.getElementById('company-modal').classList.remove('hidden');
            } catch (err) {
                console.error("Company 360 error:", err);
            }
        }

        function closeCompanyModal() {
            document.getElementById('company-modal').classList.add('hidden');
        }

        async function exportCurrentToCRM() {
            if (!activeCompanyProfile) return;
            const p = activeCompanyProfile.profile;
            try {
                const res = await fetch('/api/v1/export/crm-odoo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        cnpj: p.cnpj,
                        company_name: p.trade_name || p.legal_name,
                        email: p.cadastral_email,
                        phone: p.cadastral_phone_1,
                        expected_revenue: 50000.0
                    })
                });
                const data = await res.json();
                showToast(data.message || "Lead exportado para o Odoo 18 / CRM!");
            } catch (err) {
                console.error("CRM export error:", err);
            }
        }

        function exportSearchResults(format) {
            if (!lastSearchResults.length) {
                showToast("Nenhum resultado para exportar.", "error");
                return;
            }
            let csvContent = "data:text/csv;charset=utf-8,CNPJ,Razao_Social,Nome_Fantasia,Estado,Cidade,CNAE,Score,Faturamento_Estimado\\n";
            lastSearchResults.forEach(r => {
                csvContent += `"${r.cnpj}","${r.legal_name}","${r.trade_name || ''}","${r.state_code}","${r.city_name}","${r.cnae_main}","${r.score}","${r.estimated_metrics ? r.estimated_metrics.revenue_label : ''}"\\n`;
            });
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `simplexo_leads_${Date.now()}.${format}`);
            document.body.appendChild(link);
            link.click();
            showToast(`Exportação ${format.toUpperCase()} gerada com sucesso!`);
        }

        function handleCSVSelect(event) {
            const file = event.target.files[0];
            if (file) {
                document.getElementById('file-name-label').innerText = `Arquivo selecionado: ${file.name}`;
                document.getElementById('btn-process-batch').disabled = false;
            }
        }

        async function processBatchUpload() {
            const fileInput = document.getElementById('csv-file-input');
            if (!fileInput.files[0]) return;

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            const btn = document.getElementById('btn-process-batch');
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i> Processando Ingestão...`;
            btn.disabled = true;

            try {
                const res = await fetch('/api/v1/enrich/batch', { method: 'POST', body: formData });
                const data = await res.json();
                currentBatchData = data.data || [];
                document.getElementById('batch-processed-count').innerText = currentBatchData.length;
                document.getElementById('batch-results-area').classList.remove('hidden');
                btn.innerHTML = `<i class="fa-solid fa-check mr-2"></i> Enriquecimento Concluído!`;
                showToast(`${currentBatchData.length} empresas enriquecidas!`);
            } catch (err) {
                console.error("Batch error:", err);
                btn.innerHTML = `Erro no processamento`;
            }
        }

        function downloadBatchResults() {
            if (!currentBatchData.length) return;
            let csvContent = "data:text/csv;charset=utf-8,CNPJ,Razao_Social,Nome_Fantasia,Score,Grade,WhatsApp,Faturamento_Estimado\\n";
            currentBatchData.forEach(r => {
                csvContent += `"${r.cnpj}","${r.legal_name}","${r.trade_name || ''}","${r.score}","${r.score_grade}","${r.has_whatsapp ? 'SIM' : 'NAO'}","${r.estimated_metrics ? r.estimated_metrics.revenue_label : ''}"\\n`;
            });
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `simplexo_mailing_enriquecido_${Date.now()}.csv`);
            document.body.appendChild(link);
            link.click();
        }

        function copyRevealSnippet() {
            const snippet = document.getElementById('reveal-snippet').innerText;
            navigator.clipboard.writeText(snippet);
            showToast("Snippet copiado para a área de transferência!");
        }

        async function loadPlans() {
            try {
                const res = await fetch('/api/v1/plans');
                const data = await res.json();
                plansCatalog = data.plans || [];
                renderPlans();
            } catch (err) {
                console.error("Plans load error:", err);
            }
        }

        function setBillingCycle(cycle) {
            currentBillingCycle = cycle;
            const btnM = document.getElementById('btn-billing-monthly');
            const btnA = document.getElementById('btn-billing-annual');

            if (cycle === 'monthly') {
                btnM.className = "px-4 py-2 rounded-lg text-xs font-bold transition bg-indigo-600 text-white shadow";
                btnA.className = "px-4 py-2 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white flex items-center";
            } else {
                btnM.className = "px-4 py-2 rounded-lg text-xs font-bold transition text-slate-400 hover:text-white";
                btnA.className = "px-4 py-2 rounded-lg text-xs font-bold transition bg-indigo-600 text-white shadow flex items-center";
            }
            renderPlans();
        }

        function renderPlans() {
            const grid = document.getElementById('plans-grid');
            if (!grid) return;
            grid.innerHTML = '';

            plansCatalog.forEach(p => {
                const isAnnual = (currentBillingCycle === 'annual');
                const priceDisplay = isAnnual 
                    ? `<span class="text-2xl font-black text-white">R$ ${p.price_annual_monthly.toFixed(2).replace('.', ',')}</span><span class="text-[11px] text-slate-400 font-medium">/mês</span>`
                    : `<span class="text-2xl font-black text-white">R$ ${p.price_monthly.toFixed(2).replace('.', ',')}</span><span class="text-[11px] text-slate-400 font-medium">/mês</span>`;
                
                const billedSub = isAnnual 
                    ? `<div class="text-[10px] text-emerald-400 font-semibold mt-0.5">Cobrado anualmente: R$ ${p.price_annual_total.toFixed(2).replace('.', ',')} (33% OFF)</div>`
                    : `<div class="text-[10px] text-slate-500 mt-0.5">Sem fidelidade &bull; Cancele quando quiser</div>`;

                const creditsCount = isAnnual ? p.export_credits * 2 : p.export_credits;
                const borderClass = p.is_popular ? 'border-2 border-indigo-500 shadow-xl shadow-indigo-500/10 bg-slate-900' : 'border border-slate-800 bg-slate-900/60 hover:border-slate-700';

                const featuresHtml = p.features.map(f => `
                    <li class="flex items-start text-[11px] text-slate-300">
                        <i class="fa-solid fa-check text-emerald-400 text-xs mr-2 mt-0.5 shrink-0"></i>
                        <span>${f}</span>
                    </li>
                `).join('');

                const card = document.createElement('div');
                card.className = `rounded-2xl p-5 flex flex-col justify-between transition relative ${borderClass}`;
                card.innerHTML = `
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <span class="px-2.5 py-0.5 text-[10px] font-bold rounded-full ${p.is_popular ? 'bg-indigo-500 text-white' : 'bg-slate-800 text-slate-300'}">
                                ${p.badge}
                            </span>
                            ${p.is_popular ? '<span class="text-[10px] font-bold text-amber-400 flex items-center"><i class="fa-solid fa-star mr-1"></i>Destaque</span>' : ''}
                        </div>

                        <div>
                            <h3 class="text-base font-extrabold text-white">${p.name}</h3>
                            <div class="mt-2 flex items-baseline">${priceDisplay}</div>
                            ${billedSub}
                        </div>

                        <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800/80">
                            <span class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Cota de Exportação</span>
                            <div class="text-sm font-black text-amber-400 flex items-center mt-0.5">
                                <i class="fa-solid fa-bolt mr-1.5 text-xs"></i> ${creditsCount.toLocaleString('pt-BR')} leads/mês
                            </div>
                        </div>

                        <ul class="space-y-2 pt-2 border-t border-slate-800/80">
                            ${featuresHtml}
                        </ul>
                    </div>

                    <div class="pt-6 mt-4 border-t border-slate-800/60">
                        <button onclick="openSubscribeModal('${p.id}')" class="w-full py-2.5 rounded-xl text-xs font-bold transition ${p.is_popular ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30' : 'bg-slate-800 hover:bg-slate-700 text-white border border-slate-700'}">
                            Assinar Agora
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function openSubscribeModal(planId) {
            selectedPlanId = planId;
            const plan = plansCatalog.find(p => p.id === planId);
            if (!plan) return;

            document.getElementById('sub-modal-title').innerText = `Assinar ${plan.name}`;
            const price = (currentBillingCycle === 'annual') ? `R$ ${plan.price_annual_monthly.toFixed(2).replace('.', ',')} / mês (Anual)` : `R$ ${plan.price_monthly.toFixed(2).replace('.', ',')} / mês`;
            document.getElementById('sub-modal-price').innerText = price;
            document.getElementById('subscribe-modal').classList.remove('hidden');
        }

        function closeSubscribeModal() {
            document.getElementById('subscribe-modal').classList.add('hidden');
        }

        async function confirmSubscription() {
            const plan = plansCatalog.find(p => p.id === selectedPlanId);
            if (!plan) return;

            const btn = document.getElementById('btn-confirm-sub');
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1.5"></i> Ativando...`;
            btn.disabled = true;

            try {
                const res = await fetch('/api/v1/plans/subscribe', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        plan_id: selectedPlanId,
                        billing_cycle: currentBillingCycle,
                        company_name: document.getElementById('sub-company').value,
                        email: document.getElementById('sub-email').value
                    })
                });
                const data = await res.json();
                document.getElementById('header-user-credits').innerText = `${Number(data.allocated_credits).toLocaleString('pt-BR')} Créditos`;
                closeSubscribeModal();
                showToast(`🎉 Assinatura do ${plan.name} confirmada! +${Number(data.allocated_credits).toLocaleString('pt-BR')} créditos liberados.`);
            } catch (err) {
                console.error("Subscription error:", err);
                showToast("Erro ao processar assinatura.", "error");
            } finally {
                btn.innerHTML = `<i class="fa-solid fa-check mr-1.5"></i> Confirmar Assinatura`;
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>"""

with open("gateway/app/templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("SUCCESS: index.html written successfully.")

