"""
Simplexo Data - Receita Federal Monthly Dataset Downloader
Queries Receita Federal's WebDAV API to discover and download the latest monthly ZIP files.
"""

import os
import re
import requests
from xml.etree import ElementTree
from typing import List, Dict
from tqdm import tqdm

DAV_NS = {"d": "DAV:"}
BASE_WEBDAV_URL = "https://arquivos.receitafederal.gov.br/public.php/webdav"
DEFAULT_SHARE_TOKEN = "YggdBLfdninEJX9"

def list_available_files(share_token: str = DEFAULT_SHARE_TOKEN) -> Dict:
    """
    Discovers the latest available month and all ZIP dataset files from Receita Federal WebDAV.
    """
    url = f"{BASE_WEBDAV_URL}/"
    headers = {"Depth": "1"}
    
    print(f"[Downloader] Connecting to WebDAV at {url}...")
    response = requests.request("PROPFIND", url, auth=(share_token, ""), headers=headers, timeout=30)
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
      raise RuntimeError(
          "No monthly directories found in Receita Federal WebDAV."
      )

    latest_month = sorted(directories)[-1]
    print(
        f"[Downloader] Discovered latest dataset month: {latest_month}"
        f" (Available: {directories})"
    )

    # Fetch files for latest month
    month_url = f"{url}{latest_month}/"
    resp_files = requests.request(
        "PROPFIND", month_url, auth=(share_token, ""), headers=headers, timeout=30
    )
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

    if os.path.exists(target_path):
        print(f"[Downloader] File already exists: {target_path} (Skipping)")
        return target_path

    print(f"[Downloader] Downloading {file_name} -> {target_path}...")
    response = requests.get(download_url, auth=(share_token, ""), stream=True, timeout=60)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024 * 1024  # 1MB chunk

    with open(target_path, "wb") as f, tqdm(
        total=total_size, unit="B", unit_scale=True, desc=file_name
    ) as pbar:
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    return target_path

def download_all(output_dir: str = "/data/rfb_raw", categories: List[str] = None):
    """
    Downloads all monthly files for the specified categories (or all if None).
    """
    meta = list_available_files()
    files = meta["files"]
    base_url = meta["base_download_url"]

    print(f"[Downloader] Downloading {len(files)} files for month {meta['month']}...")
    for f in files:
        if categories:
            if not any(c.lower() in f.lower() for c in categories):
                continue
        file_url = f"{base_url}{f}"
        download_file(f, file_url, output_dir)
