"""
Simplexo Data - End-to-End ETL Runner for Receita Federal
Usage:
    python -m etl.run_etl --download --load
    python -m etl.run_etl --list
"""

import sys
import argparse
import os
from etl.receita_federal.downloader import list_available_files, download_all
from etl.receita_federal.loader import run_full_load

def main():
    parser = argparse.ArgumentParser(description="Simplexo Data ETL Orchestrator")
    parser.add_argument("--list", action="store_true", help="List files available for download at RFB")
    parser.add_argument("--download", action="store_true", help="Download all monthly RFB zip files")
    parser.add_argument("--categories", nargs="+", help="Filter categories e.g. Empresas Estabelecimentos Socios")
    parser.add_argument("--load", action="store_true", help="Load downloaded zip files into PostgreSQL")
    parser.add_argument("--data-dir", default="/data/rfb_raw", help="Target directory for raw files")
    
    args = parser.parse_args()

    if args.list:
        meta = list_available_files()
        print(f"\n[RFB WebDAV] Month: {meta['month']} (Total: {len(meta['files'])} files)")
        for f in meta['files']:
            print(f" - {f}")
        return

    if args.download:
        print(f"[ETL] Starting download to {args.data_dir}...")
        download_all(args.data_dir, categories=args.categories)

    if args.load:
        print(f"[ETL] Starting PostgreSQL bulk load from {args.data_dir}...")
        run_full_load(args.data_dir)

    if not (args.list or args.download or args.load):
        parser.print_help()

if __name__ == "__main__":
    main()
