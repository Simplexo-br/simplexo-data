"""
Simplexo Data - Background Mining & Enrichment Worker
Listens to enrichment jobs or crawls un-enriched active establishments.
"""

import time
import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from mining.crawler import crawl_company_website
from mining.scorer import calculate_commercial_score
from mining.email_validator import validate_corporate_email

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://simplexo:simplexo_secure_pass_2026@localhost:5432/simplexo_data")

def get_db():
    return psycopg2.connect(DATABASE_URL)

def run_worker_loop():
    print("[Worker] Starting Simplexo Data Mining Worker 2.0...")
    while True:
        try:
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Fetch establishments that need enrichment
            cursor.execute("""
                SELECT e.id, e.cnpj, e.trade_name, e.city_name, e.state_code, e.cadastral_email, e.cadastral_phone_1
                FROM data_core.establishments e
                LEFT JOIN data_mining.commercial_scores s ON s.establishment_id = e.id
                WHERE s.id IS NULL AND e.registration_status = 'ATIVA'
                LIMIT 5;
            """)
            rows = cursor.fetchall()

            if not rows:
                time.sleep(10)
                cursor.close()
                conn.close()
                continue

            for row in rows:
                est_id = row['id']
                print(f"[Worker] Processing establishment: {row['trade_name'] or row['cnpj']} ({est_id})")
                
                # Discovery website from cadastral email
                website = None
                domain = None
                if row['cadastral_email'] and '@' in row['cadastral_email']:
                    domain = row['cadastral_email'].split('@')[1]
                    if domain not in ('gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'bol.com.br'):
                        website = f"https://www.{domain}"

                extracted = {'phones': [], 'whatsapps': [], 'emails': [], 'socials': {}, 'technologies': {}}
                if website:
                    extracted = crawl_company_website(website)

                # Add cadastral contacts if present
                if row['cadastral_email']:
                    extracted['emails'].append(row['cadastral_email'])
                if row['cadastral_phone_1']:
                    extracted['phones'].append(row['cadastral_phone_1'])

                # Validate Emails MX
                has_valid_email = any(validate_corporate_email(em)["is_valid"] for em in extracted['emails']) if extracted['emails'] else False

                # Calculate Commercial Score
                score_res = calculate_commercial_score({
                    'whatsapps': extracted.get('whatsapps', []),
                    'phones': extracted.get('phones', []),
                    'emails': extracted.get('emails', []),
                    'website': website,
                    'has_decision_maker': False,
                    'is_fresh': True
                })

                # Insert Commercial Score
                cursor.execute("""
                    INSERT INTO data_mining.commercial_scores (
                        establishment_id, total_score, score_grade, has_valid_whatsapp,
                        has_valid_phone, has_valid_email, has_website, has_decision_maker,
                        score_breakdown
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (establishment_id) DO UPDATE SET
                        total_score = EXCLUDED.total_score,
                        score_grade = EXCLUDED.score_grade,
                        has_valid_whatsapp = EXCLUDED.has_valid_whatsapp,
                        has_valid_phone = EXCLUDED.has_valid_phone,
                        has_valid_email = EXCLUDED.has_valid_email,
                        has_website = EXCLUDED.has_website,
                        score_breakdown = EXCLUDED.score_breakdown,
                        calculated_at = CURRENT_TIMESTAMP;
                """, (
                    est_id, score_res['total_score'], score_res['score_grade'],
                    score_res['has_valid_whatsapp'], score_res['has_valid_phone'],
                    has_valid_email, bool(website),
                    score_res['has_decision_maker'],
                    json.dumps(extracted.get('technologies', {}))
                ))

                # Insert / Update Digital Footprint
                if website or domain:
                    cursor.execute("""
                        INSERT INTO data_mining.digital_footprint (
                            establishment_id, website_url, domain_name, detected_technologies,
                            social_profiles, last_crawled_at
                        ) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        ON CONFLICT (establishment_id) DO UPDATE SET
                            website_url = EXCLUDED.website_url,
                            detected_technologies = EXCLUDED.detected_technologies,
                            social_profiles = EXCLUDED.social_profiles,
                            last_crawled_at = CURRENT_TIMESTAMP;
                    """, (
                        est_id, website, domain,
                        json.dumps(extracted.get('technologies', {})),
                        json.dumps(extracted.get('socials', {}))
                    ))

                conn.commit()
                print(f"[Worker] Updated Score and Technographics for {est_id}: {score_res['total_score']} ({score_res['score_grade']})")

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"[Worker] Error in worker loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_worker_loop()
