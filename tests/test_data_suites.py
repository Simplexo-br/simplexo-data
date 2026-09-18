"""
Unit and Integration Tests for Simplexo Data Suite 3.0:
- Stone Station B2B & B2C
- DataFlow™ Waterfall Engine
- DatAService Batch Sanitizer & Assertiveness Score
- Simplexo Data Reveal Engine
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Unit and Integration Tests for Simplexo Data Suite 3.0
from mining.dataflow_waterfall import dataflow_engine
from gateway.app.dataservice import calculate_assertiveness_score, sanitize_and_enrich_batch
from gateway.app.reveal import calculate_intent_score, log_visitor_event, get_recent_identified_visitors, resolve_ip_to_host

def test_dataflow_waterfall():
    sample_company = {
        "cnpj": "33000167000101",
        "legal_name": "PETROLEO BRASILEIRO S A PETROBRAS",
        "trade_name": "PETROBRAS",
        "domain": "petrobras.com.br",
        "email": "contato@petrobras.com.br",
        "decisors": [{"name": "Magda Chambriard", "role": "Presidente"}]
    }
    enriched = dataflow_engine.enrich_company_waterfall("33000167000101", sample_company)
    assert "dataflow_waterfall" in enriched
    metadata = enriched["dataflow_waterfall"]
    assert metadata["engine"] == "DataFlow Waterfall 3.0"
    assert metadata["total_latency_ms"] >= 0
    assert len(metadata["providers_cascade"]) >= 4

def test_assertiveness_score_calculation():
    # Alta assertividade
    score_high = calculate_assertiveness_score(
        has_valid_cnpj=True,
        status_active=True,
        has_address=True,
        has_valid_phone=True,
        has_valid_email=True,
        has_decisors=True
    )
    assert score_high["score"] == 100
    assert score_high["badge"] == "ALTA_ASSERTIVIDADE"

    # Baixa assertividade
    score_low = calculate_assertiveness_score(
        has_valid_cnpj=True,
        status_active=False,
        has_address=False,
        has_valid_phone=False,
        has_valid_email=False,
        has_decisors=False
    )
    assert score_low["score"] == 15
    assert score_low["badge"] == "BAIXA_ASSERTIVIDADE"

def test_dataservice_batch_sanitizer():
    csv_raw = """cnpj,razao_social,email,telefone,endereco
33000167000101,PETROBRAS,contato@petrobras.com.br,2132244477,Av Republica do Chile 65
33.000.167/0001-01,PETROBRAS DUPLICADA,contato@petrobras.com.br,2132244477,Av Republica do Chile 65
53113791000122,TOTVS,suporte@totvs.com.br,1120997000,Av Braz Leme 1000
"""
    result = sanitize_and_enrich_batch(csv_raw)
    assert result["total_records_read"] == 3
    assert result["valid_unique_records"] == 2
    assert result["duplicates_removed"] == 1
    assert len(result["processed_records"]) == 2
    assert result["processed_records"][0]["assertiveness_score"] > 80

def test_reveal_intent_score_and_event_logging():
    intent = calculate_intent_score("https://datastone.com.br/precos", "https://br.linkedin.com/", 150)
    assert intent["intent_score"] >= 80
    assert intent["badge"] == "ALTA INTENÇÃO"

    ev = log_visitor_event(
        company_name="TEST COMPANY",
        cnpj="00000000000191",
        domain="test.com.br",
        location="São Paulo, SP",
        page_visited="/planos",
        referrer="Google",
        intent_score=90
    )
    assert ev["company_name"] == "TEST COMPANY"
    recent = get_recent_identified_visitors()
    assert any(v["cnpj"] == "00000000000191" for v in recent)

if __name__ == "__main__":
    test_dataflow_waterfall()
    test_assertiveness_score_calculation()
    test_dataservice_batch_sanitizer()
    test_reveal_intent_score_and_event_logging()
    print("ALL TESTS PASSED SUCCESSFULLY!")
