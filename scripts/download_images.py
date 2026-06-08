#!/usr/bin/env python3
"""
Descarga portadas autorizadas a images/<slug>.<ext>.

Uso:
  python scripts/download_images.py image_sources.csv

CSV esperado:
  nombre,imagen
  Cybercity 2049,https://...
"""

import csv
import mimetypes
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "images"
USER_AGENT = "scaperooms-image-fetcher/1.0"


def slugify(text):
    text = str(text or "").strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "escape-room"


def ext_from_response(url, content_type):
    guessed = mimetypes.guess_extension((content_type or "").split(";")[0].strip())
    if guessed in [".jpg", ".jpeg", ".png", ".webp", ".avif"]:
        return ".jpg" if guessed == ".jpeg" else guessed

    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in [".jpg", ".jpeg", ".png", ".webp", ".avif"]:
        return ".jpg" if suffix == ".jpeg" else suffix

    return ".jpg"


def download(nombre, url):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as response:
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise ValueError(f"No parece una imagen: {content_type}")
        ext = ext_from_response(url, content_type)
        dest = IMAGES_DIR / f"{slugify(nombre)}{ext}"
        data = response.read()
        dest.write_bytes(data)
        return dest.relative_to(ROOT).as_posix(), len(data)


def main():
    if len(sys.argv) != 2:
        print("Uso: python scripts/download_images.py image_sources.csv")
        return 1

    source = Path(sys.argv[1])
    if not source.exists():
        print(f"No existe: {source}")
        return 1

    IMAGES_DIR.mkdir(exist_ok=True)
    ok = 0
    failed = 0

    with source.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            nombre = (row.get("nombre") or row.get("Nombre") or "").strip()
            url = (row.get("imagen") or row.get("Imagen") or row.get("url") or "").strip()
            if not nombre or not url:
                continue
            if not url.lower().startswith(("http://", "https://")):
                print(f"SKIP {nombre}: URL no remota")
                continue
            try:
                path, size = download(nombre, url)
                print(f"OK   {nombre}: {path} ({size} bytes)")
                ok += 1
                time.sleep(0.25)
            except Exception as exc:
                print(f"FAIL {nombre}: {exc}")
                failed += 1

    print(f"Descarga finalizada: {ok} OK, {failed} fallos")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
