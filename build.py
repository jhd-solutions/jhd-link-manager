#!/usr/bin/env python3
"""Generate static redirects for GitHub Pages from links.json; no dependencies."""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).parent
OUTPUT = BASE / "_site"
RESERVED = {"index", "404", "assets", "admin", "links", "api", "robots", "favicon", "about", "privacy", "manager"}


def validate_alias(alias: str) -> None:
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,30}[a-z0-9])?", alias):
        raise ValueError(f"Alias invalide: {alias!r}; 1-32 caractères minuscules, chiffres ou tirets")
    if alias in RESERVED:
        raise ValueError(f"Alias réservé: {alias!r}")


def validate_url(value: str) -> None:
    parsed = urlsplit(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f"URL de destination non acceptée: {value!r}")
    if any(ord(x) < 32 for x in value):
        raise ValueError("URL contenant un caractère de contrôle")


def make_redirect(destination: str, name: str) -> str:
    dest_attr = html.escape(destination, quote=True)
    label = html.escape(name, quote=True)
    dest_js = json.dumps(destination, ensure_ascii=True).replace("<", "\\u003c")
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0;url={dest_attr}">
<title>Redirection — {label} · JHD Solutions</title>
<link rel="icon" href="data:,">
<style>body{{font:16px/1.6 system-ui,sans-serif;max-width:44rem;margin:12vh auto;padding:0 1.25rem;color:#26344c}}a{{color:#245bd1;overflow-wrap:anywhere}}</style>
</head>
<body>
<h1>Redirection en cours…</h1>
<p>Si la redirection ne fonctionne pas, <a href="{dest_attr}" rel="noreferrer">ouvrez ce lien</a>.</p>
<script>window.location.replace({dest_js});</script>
</body>
</html>
'''


def main() -> None:
    data = json.loads((BASE / "links.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("links.json doit contenir un objet JSON {alias:destination}.")
    for alias, record in data.items():
        validate_alias(alias)
        if isinstance(record, str):
            destination = record
        elif isinstance(record, dict) and isinstance(record.get("destination"), str):
            destination = record["destination"]
        else:
            raise ValueError(f"Destination manquante pour {alias!r}")
        validate_url(destination)

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT / "index.html").write_text('''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>JHD Link Manager</title><style>body{font:16px/1.6 system-ui,sans-serif;max-width:40rem;margin:14vh auto;padding:0 1.2rem;color:#26344c}h1{color:#1553a8}</style></head><body><h1>JHD Link Manager</h1><p>Service de redirection géré par JHD Solutions.</p><p>Pour accéder à un lien court, utilisez son adresse complète, avec son code final.</p><p><a href="./manager/">Consulter les liens publiés</a></p></body></html>''', encoding="utf-8")
    (OUTPUT / "404.html").write_text('''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Lien introuvable</title></head><body style="font:16px system-ui;max-width:35rem;margin:15vh auto;padding:1rem"><h1>Lien introuvable</h1><p>Ce lien court n'existe pas ou n'est plus actif.</p></body></html>''', encoding="utf-8")
    shutil.copyfile(BASE / "links.json", OUTPUT / "links.json")
    (OUTPUT / "manager").mkdir()
    shutil.copyfile(BASE / "manager.html", OUTPUT / "manager" / "index.html")
    for alias, record in data.items():
        destination = record if isinstance(record, str) else record["destination"]
        name = alias if isinstance(record, str) else record.get("title", alias)
        folder = OUTPUT / alias
        folder.mkdir()
        (folder / "index.html").write_text(make_redirect(destination, str(name)), encoding="utf-8")
    print(f"{len(data)} redirection(s) générée(s) dans {OUTPUT}")


if __name__ == "__main__":
    main()
