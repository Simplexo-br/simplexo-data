"""
Simplexo Data - Receita Federal Monthly Dataset Downloader
Queries Receita Federal's WebDAV API to discover and download the latest monthly ZIP files with resilient retries.
"""

import os
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from xml.etree import ElementTree
from typing import List, Dict
from tqdm import tqdm

DAV_NS = {"d": "DAV:"}
BASE_WEBDAV_URL = "https://arquivos.receitafederal.gov.br/public.php/webdav"
DEFAULT_SHARE_TOKEN = "YggdBLfdninEJX9"

def get_resilient_session(share_token: str = DEFAULT_SHARE_TOKEN) -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.auth = (share_token, "")
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Depth': '1'
    })
    return session

def list_available_files(share_token: str = DEFAULT_SHARE_TOKEN) -> Dict:
    """
    Discovers the latest available month and all ZIP dataset files from Receita Federal WebDAV.
    """
    url = f"{BASE_WEBDAV_URL}/"
    session = get_resilient_session(share_token)
    
    print(f"[Downloader] Connecting to WebDAV at {url}...")
    response = session.request("PROPFIND", url, timeout=45)
    response.raise_for_status()

    root = ElementTree.fromstring(response.content)
    directories = []
    for resp_elem in root.findall("d:response", DAV_NS):
        href_elem = resp_elem.find("d:href", DAV_NS)
        if href_elem is not None and href_elem.text:
            match = re.search(r"(\d{4}-\d{2})/?$", href_elem.text)
            if match:
                directories.append(match.group(1))

    if not directories:
        raise RuntimeError("No monthly directories found in Receita Federal WebDAV.")

    latest_month = sorted(directories)[-1]
    print(f"[Downloader] Discovered latest dataset month: {latest_month} (Available: {len(directories)} months)")

    # Fetch files for latest month
    month_url = f"{url}{latest_month}/"
    resp_files = session.request("PROPFIND", month_url, timeout=45)
    resp_files.raise_for_status()

    root_files = ElementTree.fromstring(resp_files.content)
    files = []
    for resp_elem in root_files.findall("d:response", DAV_NS):
        href_elem = resp_elem.find("d:href", DAV_NS)
        if href_elem is not None and href_elem.text:
            match = re.search(r"/([^/]+\.zip)$", href_elem.text, re.IGNORECASE)
            if match:
                files.append(match.group(1))

    base_download_url = f"https://arquivos.receitafederal.gov.br/public.php/dav/files/{share_token}/{latest_month}/"

    return {
        "month": latest_month,
        "base_download_url": base_download_url,
        "files": files,
        "all_months": directories,
    }

def download_file(file_name: str, download_url: str, output_dir: str, share_token: str = DEFAULT_SHARE_TOKEN):
    """
    Downloads a single file from WebDAV with streaming and progress bar.
    """
    os.makedirs(output_dir, exist_ok=True)
    target_path = os.path.join(output_dir, file_name)

    if os.path.exists(target_path) and os.path.getsize(target_path) > 1024:
        print(f"[Downloader] File already exists: {target_path} (Skipping)")
        return target_path

    print(f"[Downloader] Downloading {file_name} -> {target_path}...")
    session = get_resilient_session(share_token)
    response = session.get(download_url, stream=True, timeout=120)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    block_size = 2 * 1024 * 1024  # 2MB chunks

    with open(target_path, "wb") as f, tqdm(
        total=total_size, unit="B", unit_scale=True, desc=file_name
    ) as pbar:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    print(f"[Downloader] Completed: {target_path}")
    return target_path

def download_all(output_dir: str = "/data/rfb_raw", categories: List[str] = None):
    """
    Downloads all monthly files for the specified categories (or all if None).
    """
    meta = list_available_files()
    files = meta["files"]
    base_url = meta["base_download_url"]

    print(f"[Downloader] Found {len(files)} files for month {meta['month']}...")
    for f in files:
        if categories:
            if not any(c.lower() in f.lower() for c in categories):
                continue
        file_url = f"{base_url}{f}"
        download_file(f, file_url, output_dir)
