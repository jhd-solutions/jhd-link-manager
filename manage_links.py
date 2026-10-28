#!/usr/bin/env python3
"""Administration des liens JHD via un workflow GitHub authentifie."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from build import validate_alias, validate_url

LINKS = Path(__file__).with_name("links.json")


def main() -> None:
    operation = os.environ.get("LINK_ACTION", "").strip()
    alias = os.environ.get("LINK_ALIAS", "").strip()
    destination = os.environ.get("LINK_DESTINATION", "").strip()
    title = os.environ.get("LINK_TITLE", "").strip()
    if operation not in {"set", "delete"}:
        raise ValueError("Action non reconnue")
    validate_alias(alias)
    data = json.loads(LINKS.read_text(encoding="utf-8"))
    if operation == "delete":
        if alias not in data:
            raise ValueError("Ce code court n'existe pas : " + alias)
        del data[alias]
        print("Lien desactive : " + alias)
    else:
        if not destination:
            raise ValueError("L'adresse de destination est obligatoire.")
        validate_url(destination)
        if title and len(title) > 120:
            raise ValueError("Le titre est limite a 120 caracteres.")
        existed = alias in data
        old = data.get(alias, {})
        old_title = old.get("title", alias) if isinstance(old, dict) else alias
        data[alias] = {"destination": destination, "title": title or old_title}
        print(("Lien mis a jour" if existed else "Lien cree") + " : " + alias)
    LINKS.write_text(
        json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print("Erreur de configuration :", exc, file=sys.stderr)
        raise SystemExit(1)
