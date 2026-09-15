"""
Simplexo Data - Revenue & Employee Estimator Engine
Calculates deterministic estimated annual revenue and employee brackets based on RFB size, capital social, CNAE and Simples Nacional status.
"""

from decimal import Decimal
from typing import Dict, Any, Optional

REVENUE_BRACKETS = {
    "ATE_360K": {"label": "Até R$ 360 mil (Microempresa / MEI)", "min": 0, "max": 360000},
    "360K_A_4_8M": {"label": "R$ 360 mil a R$ 4,8 milhões (Pequena Empresa / EPP)", "min": 360000, "max": 4800000},
    "4_8M_A_16M": {"label": "R$ 4,8 milhões a R$ 16 milhões (Médio Porte Inicial)", "min": 4800000, "max": 16000000},
    "16M_A_90M": {"label": "R$ 16 milhões a R$ 90 milhões (Médio Porte Consolidado)", "min": 16000000, "max": 90000000},
    "ACIMA_90M": {"label": "Acima de R$ 90 milhões (Grande Porte / Enterprise)", "min": 90000000, "max": 999999999999}
}

EMPLOYEE_BRACKETS = {
    "1_A_5": "1 a 5 colaboradores",
    "6_A_19": "6 a 19 colaboradores",
    "20_A_49": "20 a 49 colaboradores",
    "50_A_99": "50 a 99 colaboradores",
    "100_A_499": "100 a 499 colaboradores",
    "500_MAIS": "Mais de 500 colaboradores"
}

def estimate_company_metrics(
    company_size: str,
    share_capital: float,
    is_mei: bool = False,
    is_simples: bool = False,
    cnae_main: str = ""
) -> Dict[str, Any]:
    """
    Infers revenue bracket and employee count based on legal and economic attributes.
    """
    capital = float(share_capital or 0)
    
    # MEI case
    if is_mei:
        return {
            "revenue_bracket": "ATE_360K",
            "revenue_label": REVENUE_BRACKETS["ATE_360K"]["label"],
            "estimated_annual_revenue": min(81000.0, max(capital * 3, 40000.0)),
            "employee_bracket": "1_A_5",
            "employee_label": EMPLOYEE_BRACKETS["1_A_5"]
        }
    
    # ME (Microempresa)
    if company_size == "ME" or is_simples:
        if capital < 100000:
            rev_bracket = "ATE_360K"
            est_rev = max(capital * 2.5, 120000.0)
            emp_bracket = "1_A_5"
        else:
            rev_bracket = "360K_A_4_8M"
            est_rev = min(max(capital * 2.0, 400000.0), 4800000.0)
            emp_bracket = "6_A_19"
        
        return {
            "revenue_bracket": rev_bracket,
            "revenue_label": REVENUE_BRACKETS[rev_bracket]["label"],
            "estimated_annual_revenue": est_rev,
            "employee_bracket": emp_bracket,
            "employee_label": EMPLOYEE_BRACKETS[emp_bracket]
        }
    
    # EPP (Empresa de Pequeno Porte)
    if company_size == "EPP":
        if capital < 500000:
            est_rev = 1500000.0
            emp_bracket = "6_A_19"
        else:
            est_rev = min(max(capital * 1.8, 2000000.0), 4800000.0)
            emp_bracket = "20_A_49"
            
        return {
            "revenue_bracket": "360K_A_4_8M",
            "revenue_label": REVENUE_BRACKETS["360K_A_4_8M"]["label"],
            "estimated_annual_revenue": est_rev,
            "employee_bracket": emp_bracket,
            "employee_label": EMPLOYEE_BRACKETS[emp_bracket]
        }
    
    # DEMAIS (Lucro Presumido / Real / Médio / Grande Porte)
    if capital >= 50000000:
        rev_bracket = "ACIMA_90M"
        emp_bracket = "500_MAIS"
        est_rev = max(capital * 1.5, 120000000.0)
    elif capital >= 10000000:
        rev_bracket = "16M_A_90M"
        emp_bracket = "100_A_499"
        est_rev = max(capital * 1.8, 30000000.0)
    elif capital >= 2000000:
        rev_bracket = "4_8M_A_16M"
        emp_bracket = "50_A_99"
        est_rev = max(capital * 2.0, 8000000.0)
    else:
        rev_bracket = "360K_A_4_8M"
        emp_bracket = "20_A_49"
        est_rev = max(capital * 2.5, 2500000.0)

    return {
        "revenue_bracket": rev_bracket,
        "revenue_label": REVENUE_BRACKETS[rev_bracket]["label"],
        "estimated_annual_revenue": est_rev,
        "employee_bracket": emp_bracket,
        "employee_label": EMPLOYEE_BRACKETS[emp_bracket]
    }
