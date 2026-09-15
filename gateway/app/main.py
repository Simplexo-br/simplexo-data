"""
Simplexo Data - FastAPI REST Gateway & Intelligence Plane
Exposes advanced search, Company 360, batch enrichment, technographics, decisors, and Reveal tracking.
"""

import os
import io
import csv
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException, Depends, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from mining.estimator import estimate_company_metrics
from mining.decisors import profile_decisors
from mining.email_validator import validate_corporate_email
from mining.technographics import detect_technologies
from fastapi.responses import HTMLResponse
from gateway.app.reveal import PIXEL_JS, resolve_ip_to_host
from etl.receita_federal.live_lookup import fetch_and_ingest_cnpj, search_and_ingest_by_name

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://simplexo:simplexo_secure_pass_2026@localhost:5432/simplexo_data")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html")

app = FastAPI(
    title="Simplexo Data Gateway API",
    description="API Soberana de Inteligência B2B: Prospecção, Enriquecimento em Lote, Technographics, Decisores e Simplexo Reveal.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
def serve_web_station():
    """Serves the interactive Simplexo Data Station B2B web application."""
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Simplexo Data Station 2.0</h1><p>Template not found.</p>")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "simplexo-data-gateway", "version": "2.0.0"}

@app.get("/api/v1/stats")
def get_platform_stats():
    """Returns overall platform statistics for dashboards."""
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) as total_establishments FROM data_core.establishments;")
            total_est = cur.fetchone()["total_establishments"]
            
            cur.execute("SELECT COUNT(*) as total_simples, COUNT(*) FILTER (WHERE is_mei = true) as total_mei FROM data_core.simples_nacional;")
            simples_stat = cur.fetchone()
            
            cur.execute("SELECT COUNT(*) as total_scores FROM data_mining.commercial_scores;")
            total_scores = cur.fetchone()["total_scores"]
            
            cur.execute("SELECT COUNT(*) as valid_whatsapps FROM data_mining.commercial_scores WHERE has_valid_whatsapp = TRUE;")
            valid_whats = cur.fetchone()["valid_whatsapps"]
            
            cur.execute("SELECT COUNT(*) as valid_emails FROM data_mining.commercial_scores WHERE has_valid_email = TRUE;")
            valid_emails = cur.fetchone()["valid_emails"]

            return {
                "total_companies": total_est,
                "total_simples_nacional": simples_stat["total_simples"],
                "total_meis": simples_stat["total_mei"],
                "enriched_companies": total_scores,
                "valid_whatsapps": valid_whats,
                "valid_emails": valid_emails
            }

@app.get("/api/v1/search")
def search_companies(
    q: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    cnae: Optional[str] = None,
    min_score: Optional[int] = 0,
    has_whatsapp: Optional[bool] = None,
    faturamento_faixa: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Search and segment companies by CNAE, Location, Commercial Score, Contact Availability, and Revenue Bracket.
    """
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            sql = """
                SELECT 
                    e.id, e.cnpj, e.trade_name, c.legal_name, e.cnae_main,
                    c.company_size, c.share_capital,
                    e.city_name, e.state_code, e.registration_status,
                    COALESCE(s.total_score, 0) as score,
                    COALESCE(s.score_grade, 'MUITO_BAIXO') as score_grade,
                    COALESCE(s.has_valid_whatsapp, FALSE) as has_whatsapp,
                    COALESCE(s.has_valid_phone, FALSE) as has_phone,
                    COALESCE(s.has_valid_email, FALSE) as has_email,
                    COALESCE(sn.is_simples, FALSE) as is_simples,
                    COALESCE(sn.is_mei, FALSE) as is_mei
                FROM data_core.establishments e
                JOIN data_core.companies c ON c.id = e.company_id
                LEFT JOIN data_core.simples_nacional sn ON sn.cnpj_base = c.cnpj_base
                LEFT JOIN data_mining.commercial_scores s ON s.establishment_id = e.id
                WHERE 1=1
            """
            params = []

            if q:
                sql += " AND (c.legal_name ILIKE %s OR e.trade_name ILIKE %s OR e.cnpj LIKE %s)"
                term = f"%{q}%"
                params.extend([term, term, f"{q}%"])

            if state:
                sql += " AND e.state_code = %s"
                params.append(state.upper())

            if city:
                sql += " AND e.city_name ILIKE %s"
                params.append(f"%{city}%")

            if cnae:
                sql += " AND e.cnae_main LIKE %s"
                params.append(f"{cnae}%")

            if min_score > 0:
                sql += " AND COALESCE(s.total_score, 0) >= %s"
                params.append(min_score)

            if has_whatsapp is True:
                sql += " AND s.has_valid_whatsapp = TRUE"

            sql += " ORDER BY score DESC, e.updated_at DESC LIMIT %s OFFSET %s;"
            params.extend([limit, offset])

            cur.execute(sql, tuple(params))
            raw_results = cur.fetchall()

            # If no results found locally and a query was provided, trigger on-demand live lookup
            if not raw_results and q:
                search_and_ingest_by_name(q)
                cur.execute(sql, tuple(params))
                raw_results = cur.fetchall()
            
            # Enrich each result with Revenue & Employee Estimation
            formatted_results = []
            for row in raw_results:
                est_metrics = estimate_company_metrics(
                    company_size=row["company_size"],
                    share_capital=float(row["share_capital"] or 0),
                    is_mei=row["is_mei"],
                    is_simples=row["is_simples"],
                    cnae_main=row["cnae_main"]
                )
                
                # Apply optional filter by revenue bracket in memory
                if faturamento_faixa and est_metrics["revenue_bracket"] != faturamento_faixa:
                    continue
                    
                row["estimated_metrics"] = est_metrics
                formatted_results.append(row)

            return {"count": len(formatted_results), "limit": limit, "offset": offset, "results": formatted_results}

@app.get("/api/v1/company/{cnpj}")
def get_company_360(cnpj: str):
    """
    Returns full Company 360 profile with cadastral data, Simples Nacional status, estimated revenue,
    QSA decisors with corporate email validation, enriched contacts and software stack.
    """
    clean_cnpj = "".join(filter(str.isalnum, cnpj))
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Establishment & Company Core
            query_sql = """
                SELECT 
                    e.*, c.legal_name, c.legal_nature_code, c.share_capital, c.company_size,
                    s.total_score, s.score_grade, s.score_breakdown,
                    COALESCE(sn.is_simples, FALSE) as is_simples,
                    COALESCE(sn.is_mei, FALSE) as is_mei,
                    sn.simples_opt_date, sn.mei_opt_date
                FROM data_core.establishments e
                JOIN data_core.companies c ON c.id = e.company_id
                LEFT JOIN data_core.simples_nacional sn ON sn.cnpj_base = c.cnpj_base
                LEFT JOIN data_mining.commercial_scores s ON s.establishment_id = e.id
                WHERE e.cnpj = %s;
            """
            cur.execute(query_sql, (clean_cnpj,))
            est = cur.fetchone()
            
            # If not in local database, fetch on-demand from RFB live endpoint
            if not est:
                fetch_and_ingest_cnpj(clean_cnpj)
                cur.execute(query_sql, (clean_cnpj,))
                est = cur.fetchone()

            if not est:
                raise HTTPException(status_code=404, detail="Empresa / CNPJ não encontrado.")

            # Estimated Economics
            est_metrics = estimate_company_metrics(
                company_size=est["company_size"],
                share_capital=float(est["share_capital"] or 0),
                is_mei=est["is_mei"],
                is_simples=est["is_simples"],
                cnae_main=est["cnae_main"]
            )

            # Partners / QSA
            cur.execute("SELECT * FROM data_core.partners_qsa WHERE company_id = %s;", (est["company_id"],))
            partners = cur.fetchall()

            # Enriched Contacts
            cur.execute("SELECT * FROM data_mining.contacts WHERE establishment_id = %s;", (est["id"],))
            contacts = cur.fetchall()

            # Identify Domain & Decisors
            domain = ""
            for ct in contacts:
                if ct["contact_type"] == "website":
                    domain = ct["contact_value"].replace("https://", "").replace("http://", "").split("/")[0]
                    break
            
            decisors = profile_decisors(partners, domain=domain)

            return {
                "profile": est,
                "estimated_economics": est_metrics,
                "decisors": decisors,
                "partners_qsa": partners,
                "contacts": contacts
            }

@app.post("/api/v1/enrich/batch")
async def batch_enrich_companies(file: UploadFile = File(...)):
    """
    Enriches a batch of companies from an uploaded CSV file containing CNPJs.
    Returns qualified contacts, scores, and estimated economics.
    """
    contents = await file.read()
    decoded = contents.decode("latin-1", errors="ignore")
    reader = csv.reader(io.StringIO(decoded), delimiter=';' if ';' in decoded else ',')
    
    cnpjs = []
    for row in reader:
        if row:
            clean = "".join(filter(str.isalnum, row[0]))
            if len(clean) == 14:
                cnpjs.append(clean)
            elif len(clean) == 8: # CNPJ Base, find headquarters
                cnpjs.append(f"{clean}000100")

    if not cnpjs:
        raise HTTPException(status_code=400, detail="Nenhum CNPJ válido encontrado no arquivo CSV.")

    enriched_records = []
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for cnpj in cnpjs[:100]: # Batch size limit per request
                query_batch = """
                    SELECT 
                        e.cnpj, e.trade_name, c.legal_name, e.cnae_main,
                        c.company_size, c.share_capital, e.city_name, e.state_code,
                        COALESCE(s.total_score, 0) as score,
                        COALESCE(s.score_grade, 'MUITO_BAIXO') as score_grade,
                        COALESCE(s.has_valid_whatsapp, FALSE) as has_whatsapp,
                        COALESCE(sn.is_simples, FALSE) as is_simples,
                        COALESCE(sn.is_mei, FALSE) as is_mei
                    FROM data_core.establishments e
                    JOIN data_core.companies c ON c.id = e.company_id
                    LEFT JOIN data_core.simples_nacional sn ON sn.cnpj_base = c.cnpj_base
                    LEFT JOIN data_mining.commercial_scores s ON s.establishment_id = e.id
                    WHERE e.cnpj = %s;
                """
                cur.execute(query_batch, (cnpj,))
                row = cur.fetchone()
                if not row:
                    fetch_and_ingest_cnpj(cnpj)
                    cur.execute(query_batch, (cnpj,))
                    row = cur.fetchone()

                if row:
                    row["estimated_metrics"] = estimate_company_metrics(
                        company_size=row["company_size"],
                        share_capital=float(row["share_capital"] or 0),
                        is_mei=row["is_mei"],
                        is_simples=row["is_simples"],
                        cnae_main=row["cnae_main"]
                    )
                    enriched_records.append(row)

    return {
        "status": "success",
        "processed_count": len(enriched_records),
        "data": enriched_records
    }

# ==========================================================
# SIMPLEXO REVEAL (B2B Website De-anonymization)
# ==========================================================

@app.get("/api/v1/reveal/pixel.js")
def get_reveal_pixel():
    """Serves the tracking javascript pixel for Simplexo websites."""
    return Response(content=PIXEL_JS, media_type="application/javascript")

class RevealPayload(BaseModel):
    url: str
    referrer: Optional[str] = ""
    title: Optional[str] = ""
    screen: Optional[str] = ""
    timestamp: Optional[str] = ""

@app.post("/api/v1/reveal/identify")
def identify_visitor(payload: RevealPayload):
    """
    Identifies the visiting company from network metadata.
    """
    # IP lookup placeholder
    resolution = resolve_ip_to_host("8.234.211.34")
    return {
        "status": "identified",
        "visitor_metadata": payload.dict(),
        "network": resolution
    }
