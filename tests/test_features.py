"""
Unit tests for all new Simplexo Data modules:
- Technographics
- Estimator (Revenue and Employees)
- Email MX Validator
- Decisors Profiler
"""

from mining.technographics import detect_technologies
from mining.estimator import estimate_company_metrics
from mining.email_validator import validate_corporate_email
from mining.decisors import profile_decisors

def test_all():
    print("=== Testing Technographics ===")
    sample_html = """
    <html>
        <head>
            <script src="https://io.vtex.com.br/vtex.js"></script>
            <script src="https://d335luupugsy2.cloudfront.net/rdstation.js"></script>
        </head>
        <body>
            <div class="totvs-protheus-footer">Sistema TOTVS</div>
        </body>
    </html>
    """
    techs = detect_technologies(sample_html)
    print("Detected Techs:", techs)
    assert "ecommerce" in techs and "VTEX" in techs["ecommerce"]
    assert "marketing_crm" in techs and "RD Station" in techs["marketing_crm"]
    assert "erp" in techs and "TOTVS" in techs["erp"]
    print("[OK] Technographics passed!")

    print("\n=== Testing Estimator ===")
    est_me = estimate_company_metrics(company_size="ME", share_capital=50000, is_mei=False, is_simples=True)
    print("ME Estimate:", est_me)
    assert est_me["revenue_bracket"] == "ATE_360K"

    est_enterprise = estimate_company_metrics(company_size="DEMAIS", share_capital=60000000)
    print("Enterprise Estimate:", est_enterprise)
    assert est_enterprise["revenue_bracket"] == "ACIMA_90M"
    print("[OK] Estimator passed!")

    print("\n=== Testing Email Validator ===")
    res_corp = validate_corporate_email("comercial@simplexo.com.br")
    print("Corp Email Val:", res_corp)
    assert res_corp["is_corporate"] is True
    assert res_corp["is_valid"] is True

    res_free = validate_corporate_email("user@gmail.com")
    print("Free Email Val:", res_free)
    assert res_free["is_corporate"] is False
    print("[OK] Email Validator passed!")

    print("\n=== Testing Decisors Profiler ===")
    sample_partners = [
        {"partner_name": "CARLOS EDUARDO SILVA", "qualification_desc": "49-Sócio-Administrador"},
        {"partner_name": "ANA PAULA SOUZA", "qualification_desc": "22-Sócio"}
    ]
    decisors = profile_decisors(sample_partners, domain="simplexo.com.br")
    print("Decisors:", decisors)
    assert len(decisors) == 2
    assert decisors[0]["seniority"] == "C-Level / Sócio"
    assert len(decisors[0]["inferred_emails"]) > 0
    print("[OK] Decisors Profiler passed!")

    print("\n*** ALL UNIT TESTS PASSED SUCCESSFULLY! ***")

if __name__ == "__main__":
    test_all()
