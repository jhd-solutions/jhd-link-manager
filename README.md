# JHD Link Manager — v1.0

Gestionnaire de liens courts pour JHD Solutions. Un fichier JSON décrit les liens ; GitHub Actions construit des pages HTML de redirection. Ce dépôt est indépendant du site BabyShow.

## Installation
1. Dans **Settings → Pages → Build and deployment → Source**, sélectionner **GitHub Actions**.
2. Dans **Actions**, consulter le workflow **Publier JHD Link Manager** et éventuellement lancer **Run workflow**.
3. Quand le site est publié, tester **https://jhd-solutions.github.io/jhd-link-manager/demo/** (redirection de démonstration vers https://example.org/).

## Ajouter, modifier ou retirer un lien
Éditer `links.json` depuis GitHub puis valider avec **Commit changes** sur la branche `main`.

Exemple :

```json
{
  "demo": {
    "destination": "https://example.org/",
    "title": "Lien de démonstration"
  },
  "b26": {
    "destination": "https://www.gaelle-accompagnante-parentale.fr/",
    "title": "Salon Baby"
  }
}
```

Chaque entrée produit une adresse `/alias/` sous le site GitHub Pages. Pour conserver une URL imprimée tout en changeant sa cible, garder l'alias et modifier uniquement `destination`.

- Alias : 1 à 32 caractères minuscules, chiffres et tirets ; certains noms sont réservés.
- Destination : URL `https://` ou `http://`.
- Un alias retiré de `links.json` cesse d'être publié après le prochain déploiement et renvoie une erreur 404.

## Limites et sécurité
- Le dépôt est **public** : les alias et destinations sont visibles. Ne jamais y stocker de données privées ou de jetons.
- Ces redirections sont effectuées **dans le navigateur** (JavaScript + meta refresh), pas par une vraie réponse HTTP 301 ou 302.
- La gestion se fait depuis GitHub ; il n'y a pas de tableau de bord d'administration public.
- Sans domaine personnalisé court, les liens `jhd-solutions.github.io/jhd-link-manager/…` restent assez longs pour un QR imprimé.
- Une URL déjà imprimée ne fonctionne que tant que le domaine, le site et la configuration restent actifs.
- **Ne pas modifier** le dépôt `jhd-solutions.github.io` de BabyShow.

## Test local
Exécuter `python build.py` avec Python 3.10+. Les fichiers générés se trouvent dans `_site/`, qui ne doit pas être commité.
