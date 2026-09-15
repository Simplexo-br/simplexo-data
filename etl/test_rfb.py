import requests
import urllib3
urllib3.disable_warnings()

headers = {
    "Depth": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    resp = requests.request(
        "PROPFIND",
        "https://arquivos.receitafederal.gov.br/public.php/webdav/",
        auth=("YggdBLfdninEJX9", ""),
        headers=headers,
        verify=False,
        timeout=15
    )
    print("Status:", resp.status_code)
    print("Response text first 300 chars:", resp.text[:300])
except Exception as e:
    print("Error connecting:", e)
