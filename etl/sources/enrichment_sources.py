"""
Simplexo Data - Multi-Source B2B Data Enrichment Engine
Handles CNO (Obras), PGFN (Dívida Ativa), Comex Stat, PNCP, ANTT & Technographics.
"""

import os
import random
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://simplexo:simplexo_secure_pass_2026@localhost:5432/simplexo_data")

def get_db():
    return psycopg2.connect(DATABASE_URL)

def seed_cno_construction_sites():
    """Seeds realistic high-value CNO construction sites."""
    cno_samples = [
        {
            "cno": "90.012.34567/89",
            "name": "Edifício Residencial Horizonte Sul - Torre A e B",
            "type": "Edificação Residencial",
            "responsible": "CYRELA BRAZIL REALTY S.A. EMPREENDIMENTOS",
            "doc": "73178600000118",
            "area_m2": 24500.00,
            "investment": 48500000.00,
            "street": "Av. Morumbi, 4500",
            "neighborhood": "Morumbi",
            "city": "SAO PAULO",
            "state": "SP",
            "zip": "05650000",
            "status": "EM_ANDAMENTO",
            "start_date": "2025-08-15"
        },
        {
            "cno": "90.012.88991/12",
            "name": "Centro Logístico Industrial Barueri Tech Park",
            "type": "Reforma Industrial",
            "responsible": "LOG COMMERCIAL PROPERTIES E PARTICIPACOES",
            "doc": "09041168000110",
            "area_m2": 58000.00,
            "investment": 92000000.00,
            "street": "Alameda Rio Negro, 1200",
            "neighborhood": "Alphaville Industrial",
            "city": "BARUERI",
            "state": "SP",
            "zip": "06454000",
            "status": "EM_ANDAMENTO",
            "start_date": "2026-01-10"
        },
        {
            "cno": "90.013.44123/45",
            "name": "Complexo Hospitalar Integrado Unimed",
            "type": "Edificação Comercial",
            "responsible": "CONSTRUTORA ANDRADE GUTIERREZ S.A.",
            "doc": "17262212000194",
            "area_m2": 18200.00,
            "investment": 35000000.00,
            "street": "Rua das Américas, 850",
            "neighborhood": "Barra da Tijuca",
            "city": "RIO DE JANEIRO",
            "state": "RJ",
            "zip": "22640100",
            "status": "EM_ANDAMENTO",
            "start_date": "2025-11-20"
        },
        {
            "cno": "90.014.77654/33",
            "name": "Ampliação Usina Fotovoltaica Solar Minas V",
            "type": "Obra de Infraestrutura",
            "responsible": "ENGIE BRASIL ENERGIA S.A.",
            "doc": "02474103000119",
            "area_m2": 120000.00,
            "investment": 145000000.00,
            "street": "Rodovia BR-040, Km 125",
            "neighborhood": "Zona Rural",
            "city": "BELO HORIZONTE",
            "state": "MG",
            "zip": "30110000",
            "status": "EM_ANDAMENTO",
            "start_date": "2026-02-01"
        },
        {
            "cno": "90.015.99221/04",
            "name": "Condomínio Residencial Jardim das Palmeiras",
            "type": "Edificação Residencial",
            "responsible": "MRV ENGENHARIA E PARTICIPACOES S.A.",
            "doc": "08343492000120",
            "area_m2": 32000.00,
            "investment": 62000000.00,
            "street": "Av. Beira Mar, 2100",
            "neighborhood": "Meireles",
            "city": "FORTALEZA",
            "state": "CE",
            "zip": "60165121",
            "status": "EM_ANDAMENTO",
            "start_date": "2025-09-01"
        },
        {
            "cno": "90.016.11223/99",
            "name": "Fábrica e Armazém Logístico Cacau Show II",
            "type": "Reforma Industrial",
            "responsible": "I.B.A.C. INDUSTRIA BRASILEIRA DE ALIMENTOS E CHOCOLATES LTDA.",
            "doc": "61472205000164",
            "area_m2": 28000.00,
            "investment": 55000000.00,
            "street": "Estrada Antiga de Itu, 140",
            "neighborhood": "Estância São Francisco",
            "city": "ITAPEVI",
            "state": "SP",
            "zip": "06695000",
            "status": "EM_ANDAMENTO",
            "start_date": "2025-10-15"
        }
    ]

    conn = get_db()
    cur = conn.cursor()
    try:
        for c in cno_samples:
            cur.execute("""
                INSERT INTO data_mining.construction_sites_cno (
                    cno_number, site_name, site_type, responsible_name, responsible_doc,
                    area_m2, estimated_investment, street, neighborhood, city_name,
                    state_code, zip_code, status, start_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cno_number) DO UPDATE SET
                    site_name = EXCLUDED.site_name,
                    area_m2 = EXCLUDED.area_m2,
                    estimated_investment = EXCLUDED.estimated_investment,
                    updated_at = CURRENT_TIMESTAMP;
            """, (
                c["cno"], c["name"], c["type"], c["responsible"], c["doc"],
                c["area_m2"], c["investment"], c["street"], c["neighborhood"],
                c["city"], c["state"], c["zip"], c["status"], c["start_date"]
            ))
        conn.commit()
        print(f"[CNO] Successfully seeded {len(cno_samples)} construction sites.")
    except Exception as e:
        conn.rollback()
        print(f"[CNO] Error seeding sites: {e}")
    finally:
        cur.close()
        conn.close()

def seed_all_multisource_enrichments():
    """Enriches known establishments with PGFN, Comex, PNCP, ANTT and Digital Footprint."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT id, cnpj, trade_name, city_name, state_code FROM data_core.establishments;")
        establishments = cur.fetchall()

        for est in establishments:
            est_id = est["id"]
            cnpj = est["cnpj"]

            # 1. PGFN Regularidade Fiscal
            has_debt = (cnpj in ["45301834000175"]) # Example sample
            cur.execute("""
                INSERT INTO data_mining.fiscal_compliance (
                    establishment_id, cnpj, has_federal_debt, total_debt_amount, debt_count, regularity_status
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    has_federal_debt = EXCLUDED.has_federal_debt,
                    total_debt_amount = EXCLUDED.total_debt_amount,
                    regularity_status = EXCLUDED.regularity_status;
            """, (
                est_id,
                cnpj,
                has_debt,
                42500.00 if has_debt else 0.00,
                1 if has_debt else 0,
                'INSCRITO_DIVIDA_ATIVA' if has_debt else 'REGULAR'
            ))

            # 2. Comex Stat (Importação / Exportação)
            is_exp = cnpj in ["61472205000164", "12821486000108"]
            is_imp = cnpj in ["61472205000164", "59069914000151"]
            cur.execute("""
                INSERT INTO data_mining.comex_operations (
                    establishment_id, cnpj, is_exporter, is_importer, export_bracket, import_bracket
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    is_exporter = EXCLUDED.is_exporter,
                    is_importer = EXCLUDED.is_importer;
            """, (
                est_id,
                cnpj,
                is_exp,
                is_imp,
                'US$ 10M a 50M' if is_exp else None,
                'US$ 1M a 10M' if is_imp else None
            ))

            # 3. PNCP / Compras Públicas
            is_gov = cnpj in ["59069914000151", "12821486000108"]
            cur.execute("""
                INSERT INTO data_mining.public_contracts (
                    establishment_id, cnpj, is_public_supplier, total_contract_count, total_contract_value
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    is_public_supplier = EXCLUDED.is_public_supplier,
                    total_contract_count = EXCLUDED.total_contract_count,
                    total_contract_value = EXCLUDED.total_contract_value;
            """, (
                est_id,
                cnpj,
                is_gov,
                4 if is_gov else 0,
                3850000.00 if is_gov else 0.00
            ))

            # 4. ANTT / Frotas
            has_fleet = cnpj in ["61472205000164"]
            cur.execute("""
                INSERT INTO data_mining.transport_fleets (
                    establishment_id, cnpj, rntrc_number, rntrc_status, carrier_type, registered_vehicles_count, fleet_category
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO UPDATE SET
                    rntrc_status = EXCLUDED.rntrc_status,
                    registered_vehicles_count = EXCLUDED.registered_vehicles_count;
            """, (
                est_id,
                cnpj,
                "RNTRC-89214712" if has_fleet else None,
                "ATIVO" if has_fleet else "INATIVO",
                "ETC" if has_fleet else None,
                45 if has_fleet else 0,
                "Pesado / Carreta" if has_fleet else None
            ))

            # 5. Digital Footprint & Technographics
            cur.execute("""
                INSERT INTO data_mining.digital_footprint (
                    establishment_id, website_url, domain_name, has_corporate_email,
                    has_ecommerce, detected_cms, detected_crm, detected_erp,
                    google_rating, google_review_count, latitude, longitude
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (establishment_id) DO UPDATE SET
                    has_corporate_email = EXCLUDED.has_corporate_email,
                    has_ecommerce = EXCLUDED.has_ecommerce,
                    detected_cms = EXCLUDED.detected_cms,
                    detected_crm = EXCLUDED.detected_crm,
                    detected_erp = EXCLUDED.detected_erp,
                    google_rating = EXCLUDED.google_rating,
                    latitude = EXCLUDED.latitude,
                    longitude = EXCLUDED.longitude;
            """, (
                est_id,
                f"https://www.{cnpj[:8]}.com.br",
                f"{cnpj[:8]}.com.br",
                True,
                cnpj in ["61472205000164"], # Cacau Show has e-commerce
                "VTEX" if cnpj == "61472205000164" else "WordPress",
                "HubSpot" if cnpj in ["59069914000151", "12821486000108"] else "RD Station",
                "SAP" if cnpj == "61472205000164" else "TOTVS",
                4.8 if cnpj == "61472205000164" else 4.6,
                1420 if cnpj == "61472205000164" else 350,
                -23.5489, # SP Coordinates
                -46.6388
            ))

        conn.commit()
        print(f"[Enrichment] Successfully populated multi-source enrichments for {len(establishments)} establishments.")
    except Exception as e:
        conn.rollback()
        print(f"[Enrichment] Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed_cno_construction_sites()
    seed_all_multisource_enrichments()
