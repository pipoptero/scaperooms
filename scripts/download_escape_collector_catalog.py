#!/usr/bin/env python3
"""
Descarga el catálogo público de portadas de Escape Collector desde Firestore.

Guarda:
  images/ec-all/<room-id>.webp      Todas las portadas encontradas.
  image_sources.ec-all.csv          Auditoría nombre -> imagen local.

Si el nombre coincide con una sala local, copia también a:
  images/<slug-local>.webp
"""

import csv
import json
import re
import shutil
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "images"
CATALOG_DIR = IMAGES_DIR / "ec-all"
DATA_FILE = ROOT / "data.json"
AUDIT_FILE = ROOT / "image_sources.ec-all.csv"

API_KEY = "AIzaSyDdd9YI85mqWq32qbKeU9oeDgUEeTaq5B8"
PROJECT = "room-escapes"
BUCKET = "room-escapes.appspot.com"
PAGE_SIZE = 300
USER_AGENT = "scaperooms-escape-collector-catalog/1.0"


def slugify(text):
    text = str(text or "").strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "escape-room"


def norm(text):
    return slugify(text).replace("-", "")


def field_value(field):
    if not field:
        return ""
    for key in ["stringValue", "integerValue", "doubleValue", "booleanValue"]:
        if key in field:
            return field[key]
    return ""


def fetch_json(url):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_rooms():
    rooms = []
    page_token = ""
    while True:
        url = (
            f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)"
            f"/documents/rooms?pageSize={PAGE_SIZE}&key={API_KEY}"
        )
        if page_token:
            url += f"&pageToken={page_token}"
        payload = fetch_json(url)
        for doc in payload.get("documents", []):
            fields = doc.get("fields", {})
            room_id = doc["name"].split("/")[-1]
            name = field_value(fields.get("name")) or field_value(fields.get("n")) or room_id
            image = field_value(fields.get("image"))
            if image:
                rooms.append({"id": room_id, "name": name, "image": image})
        page_token = payload.get("nextPageToken", "")
        if not page_token:
            return rooms


def image_url(image_name):
    return f"https://firebasestorage.googleapis.com/v0/b/{BUCKET}/o/rooms%2F{quote(image_name)}?alt=media"


def download(url, dest):
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=45) as response:
        if not response.headers.get("Content-Type", "").startswith("image/"):
            raise ValueError("La respuesta no es una imagen")
        dest.write_bytes(response.read())


def local_room_slugs():
    if not DATA_FILE.exists():
        return {}
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    rooms = data.get("pendientes", []) + data.get("hechos", [])
    return {norm(room.get("nombre")): slugify(room.get("nombre")) for room in rooms}


def main():
    IMAGES_DIR.mkdir(exist_ok=True)
    CATALOG_DIR.mkdir(exist_ok=True)

    local_slugs = local_room_slugs()
    rooms = fetch_rooms()

    ok = 0
    failed = 0
    matched_local = 0
    audit_rows = []

    for room in rooms:
        dest = CATALOG_DIR / f"{slugify(room['id'])}.webp"
        url = image_url(room["image"])
        try:
            if not dest.exists() or dest.stat().st_size == 0:
                download(url, dest)
                time.sleep(0.08)
            ok += 1

            local_slug = local_slugs.get(norm(room["name"]))
            if local_slug:
                shutil.copyfile(dest, IMAGES_DIR / f"{local_slug}.webp")
                matched_local += 1

            audit_rows.append({
                "id": room["id"],
                "nombre": room["name"],
                "imagen": dest.relative_to(ROOT).as_posix(),
                "origen": url,
            })
            print(f"OK   {room['name']}: {dest.relative_to(ROOT).as_posix()}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {room['name']}: {exc}")

    with AUDIT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nombre", "imagen", "origen"])
        writer.writeheader()
        writer.writerows(audit_rows)

    print(f"Catálogo: {ok} imágenes OK, {failed} fallos, {matched_local} vinculadas a salas locales.")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
