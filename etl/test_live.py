import os
import requests
from etl.receita_federal.live_lookup import fetch_and_ingest_cnpj, search_and_ingest_by_name

print("=== Testing Ingestion of Aberama Brasil (45301834000175) ===")
res = fetch_and_ingest_cnpj('45301834000175')
print("Direct Ingest Result:", res is not None)

print("\n=== Testing Search Ingest by Name ===")
res2 = search_and_ingest_by_name('aberama brasil')
print("Search Ingest Result count:", len(res2))
