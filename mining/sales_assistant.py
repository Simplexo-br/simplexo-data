"""
Simplexo Data - AI Sales Assistant & Commercial Copilot
Generates contextualized B2B pitches, WhatsApp icebreakers, cold call scripts, and objection handling based on Company 360 intelligence.
"""

from typing import Dict, Any, List, Optional

SECTOR_HOOKS = {
    "saude": {
        "pain": "Redução de glosas, conformidade regulatória e otimização de suprimentos hospitalares/farmacêuticos.",
        "pitch": "Ajudamos empresas do setor de saúde a mitigar riscos operacionais e acelerar a escala de distribuição com conformidade total."
    },
    "construcao": {
        "pain": "Gestão de suprimentos na obra, cumprimento de cronogramas e redução de custos logísticos de materiais pesados.",
        "pitch": "Conectamos construtoras e incorporadoras a soluções que reduzem desperdício de insumos em até 18% no canteiro de obras."
    },
    "tecnologia": {
        "pain": "Aceleração de pipeline B2B, redução de CAC e integração com ERPs legados.",
        "pitch": "Aumentamos a taxa de conversão comercial de empresas de tecnologia conectando inteligência de dados a fluxos automatizados de vendas."
    },
    "comercio": {
        "pain": "Aumento do ticket médio, gestão de rupturas de estoque e expansão multicanal (físico + digital).",
        "pitch": "Otimizamos a cadeia de fornecimento e o alcance comercial de redes varejistas com inteligência preditiva de demanda."
    },
    "industria": {
        "pain": "Eficiência energética, manutenção preditiva e redução do tempo de parada de maquinário fabril.",
        "pitch": "Elevamos a produtividade fabril e a previsibilidade de compras industriais com diagnóstico analítico em tempo real."
    }
}

def detect_sector_context(cnae_desc: str, company_name: str) -> Dict[str, str]:
    text = (cnae_desc + " " + company_name).lower()
    if any(k in text for k in ["farmac", "saude", "medic", "hospital", "clinica", "drogaria"]):
        return SECTOR_HOOKS["saude"]
    if any(k in text for k in ["constru", "obra", "engenharia", "incorpor", "edific"]):
        return SECTOR_HOOKS["construcao"]
    if any(k in text for k in ["software", "tecnolog", "sistemas", "internet", "dados", "computador"]):
        return SECTOR_HOOKS["tecnologia"]
    if any(k in text for k in ["comercio", "varejo", "loja", "distribuidora", "mercado"]):
        return SECTOR_HOOKS["comercio"]
    return SECTOR_HOOKS["industria"]

def generate_sales_briefing(company_data: Dict[str, Any], target_decisor: Optional[str] = None) -> Dict[str, Any]:
    profile = company_data.get("profile", {})
    trade_name = profile.get("trade_name") or profile.get("legal_name", "a empresa")
    legal_name = profile.get("legal_name", "")
    city = profile.get("city_name", "sua região")
    uf = profile.get("state_code", "")
    cnae_desc = profile.get("cnae_main_desc", "sua área de atuação")
    revenue_est = company_data.get("financial_estimation", {}).get("estimated_revenue_bracket", "porte empresarial consolidado")
    
    # Decisors
    decisors = company_data.get("decisors", [])
    selected_decisor = target_decisor
    if not selected_decisor and decisors:
        selected_decisor = decisors[0].get("display_name") or decisors[0].get("name")
    if not selected_decisor:
        selected_decisor = "Diretoria"

    decisor_first_name = selected_decisor.split()[0].title() if selected_decisor else "Diretor(a)"
    
    # Signals
    tech = company_data.get("digital_footprint", {})
    comex = company_data.get("comex_operations", {})
    cno = company_data.get("cno_construction", {})
    contracts = company_data.get("public_contracts", {})
    
    sector = detect_sector_context(cnae_desc, trade_name)
    
    # Tech signals
    tech_highlights = []
    if tech.get("has_ecommerce"):
        tech_highlights.append("operação de E-commerce ativa")
    if tech.get("detected_erp"):
        tech_highlights.append(f"infraestrutura ERP ({tech.get('detected_erp')})")
    if comex.get("is_exporter"):
        tech_highlights.append("operações de comércio exterior e exportação")
    if cno.get("active_sites_count", 0) > 0:
        tech_highlights.append(f"{cno.get('active_sites_count')} obras CNO ativas")
    
    signals_str = ", ".join(tech_highlights) if tech_highlights else f"atuação destacada em {city}/{uf}"

    # 1. WhatsApp Icebreaker
    whatsapp_pitch = (
        f"Olá, {decisor_first_name}! Tudo bem?\n\n"
        f"Acompanho o crescimento da *{trade_name}* no setor de {cnae_desc.lower()} e notei sua {signals_str}.\n\n"
        f"{sector['pitch']}\n\n"
        f"Teria 10 minutinhos nesta quinta-feira para trocar uma ideia rápida sobre como podemos gerar valor imediato para a sua operação?"
    )

    # 2. Cold Call Script
    cold_call_script = {
        "abertura": f"Olá {decisor_first_name}, tudo bem? Sou o [Seu Nome] da Simplexo. Sei que seu tempo é valioso, tenho apenas 30 segundos para te explicar o motivo da minha ligação para a {trade_name}.",
        "gancho_de_valor": f"Identificamos que a {trade_name} é referência em {city}/{uf}. Empresas do seu porte ({revenue_est}) frequentemente enfrentam o desafio de {sector['pain'].lower()}",
        "pergunta_de_qualificacao": f"Hoje na {trade_name}, vocês já possuem uma estratégia definida para otimizar esse gargalo ou isso ainda impacta a margem de vocês?",
        "fechamento_cta": "Podemos alinhar uma breve conversa técnica de 15 minutos com nosso especialista nesta semana para te mostrar esse comparativo de mercado?"
    }

    # 3. Executive Email Pitch
    email_pitch = {
        "subject": f"Oportunidade de ganho de eficiência comercial para a {trade_name}",
        "body": (
            f"Prezado(a) {selected_decisor},\n\n"
            f"Espero que este e-mail o(a) encontre bem.\n\n"
            f"Entro em contato porque analisamos a presença de mercado da {trade_name} em {city}/{uf} e identificamos um potencial significativo de otimização na sua operação de {cnae_desc.lower()}.\n\n"
            f"Atualmente, ajudamos líderes e diretores de empresas líderes a resolver o desafio de {sector['pain'].lower()}, proporcionando previsibilidade e escala com ROI comprovado.\n\n"
            f"Você teria disponibilidade para um café virtual rápido de 15 minutos na próxima terça-feira às 10h?\n\n"
            f"Atenciosamente,\n"
            f"[Seu Nome]\n"
            f"[Seu Cargo] | Simplexo Intelligence"
        )
    }

    # 4. Objection Handling
    objections = [
        {
            "objecao": "Já temos fornecedor atual.",
            "resposta": f"Excelente, {decisor_first_name}! Nosso objetivo não é substituir o que já funciona bem na {trade_name}, mas sim apresentar um benchmarking complementar que tem gerado até 20% mais eficiência em operações similares."
        },
        {
            "objecao": "Não temos orçamento/budget no momento.",
            "resposta": "Entendo perfeitamente. Por isso mesmo nosso modelo é desenhado para se pagar no primeiro trimestre com a economia gerada. Vale a pena conhecer o modelo para o seu planejamento futuro."
        },
        {
            "objecao": "Me envie uma apresentação por e-mail.",
            "resposta": "Com certeza! Para te enviar apenas os cases relevantes para o setor de {trade_name}, qual é a sua principal prioridade operacional neste trimestre?"
        }
    ]

    return {
        "company_name": trade_name,
        "decisor_targeted": selected_decisor,
        "sector_context": sector,
        "signals_detected": tech_highlights,
        "whatsapp_icebreaker": whatsapp_pitch,
        "cold_call_script": cold_call_script,
        "executive_email": email_pitch,
        "objection_matrix": objections
    }
