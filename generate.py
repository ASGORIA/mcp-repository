#!/usr/bin/env python3
"""Génère un registre MCP statique (spécification v0.1) pour GitHub Pages.

Source : servers.json (liste des serveurs autorisés).
Sortie : dossier v0.1/ à publier tel quel avec GitHub Pages.

Usage : python3 generate.py
"""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "servers.json"
OUT = ROOT / "v0.1"

# Schéma du format "server.json". En cas de rejet, vérifier la valeur actuelle
# dans https://registry.modelcontextprotocol.io/v0.1/servers?limit=1
SCHEMA = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_entry(s: dict, now: str) -> dict:
    for key in ("name", "description", "version", "url"):
        if not s.get(key):
            raise SystemExit(f"Champ '{key}' manquant pour le serveur : {s}")
    if "/" not in s["name"]:
        raise SystemExit(f"Le nom doit être au format 'domaine.inverse/nom' : {s['name']}")

    server = {
        "$schema": SCHEMA,
        "name": s["name"],
        "description": s["description"],
        "version": s["version"],
        "remotes": [{"type": s.get("transport", "streamable-http"), "url": s["url"]}],
    }
    if s.get("title"):
        server["title"] = s["title"]

    return {
        "server": server,
        "_meta": {
            "io.modelcontextprotocol.registry/official": {
                "status": "active",
                "publishedAt": now,
                "updatedAt": now,
                "isLatest": True,
            }
        },
    }


def main() -> None:
    servers = json.loads(SOURCE.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = [build_entry(s, now) for s in servers]

    if OUT.exists():
        shutil.rmtree(OUT)

    # GET /v0.1/servers -> GitHub Pages sert v0.1/servers/index.html
    listing = {"servers": entries, "metadata": {"count": len(entries)}}
    write_json(OUT / "servers" / "index.html", listing)

    for e in entries:
        name = e["server"]["name"]
        version = e["server"]["version"]
        # GET /v0.1/servers/{name}/versions/latest et /versions/{version}
        # Le nom contient un "/" (envoyé en %2F dans l'URL). Selon que GitHub Pages
        # décode ou non ce caractère, c'est l'un ou l'autre dossier qui sera lu :
        # on génère les deux pour être sûr.
        for folder in (name, name.replace("/", "%2F")):
            base = OUT / "servers" / folder / "versions"
            for v in ("latest", version):
                write_json(base / v / "index.html", e)

    (ROOT / ".nojekyll").touch()
    print(f"{len(entries)} serveur(s) généré(s) dans {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
