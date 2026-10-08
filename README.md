# Feedback API

API Flask + PostgreSQL qui collecte les avis des visiteurs d'un portfolio (note de 1 à 5 + commentaire) et un dashboard protégé affichant les statistiques (note moyenne, répartition des notes, avis par mois).

## Stack

- Python / Flask, gunicorn en production
- PostgreSQL, requêtes SQL brutes via psycopg2
- Architecture en couches : `Controllers` → `Services` → `Repositories` → `Config`
- Chart.js pour le dashboard

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/reviews` | Crée un avis. Corps JSON : `rating` (entier 1-5, requis), `comment` (500 car. max, requis), `name` (100 car. max, optionnel) |
| GET | `/api/reviews/stats` | Statistiques. Authentification Basic requise |
| GET | `/dashboard` | Dashboard avec graphiques. Authentification Basic requise |

Exemple de réponse de `/api/reviews/stats` :

```json
{
  "count": 12,
  "average": 4.25,
  "distribution": {"1": 0, "2": 1, "3": 2, "4": 4, "5": 5},
  "timeline": [{"month": "2026-09", "count": 7}, {"month": "2026-10", "count": 5}]
}
```

Le champ `website` dans le corps de `POST /api/reviews` est un piège à bots : s'il est rempli, la requête renvoie 201 sans rien enregistrer.

## Lancer en local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # puis renseigner les valeurs
```

Créer la table (sur une base PostgreSQL déjà existante, locale ou distante) :

```bash
python db/init_db.py
```

Démarrer le serveur :

```bash
python -m Controllers.review_controller
```

## Variables d'environnement

| Variable | Rôle |
|---|---|
| `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Connexion PostgreSQL |
| `DB_SSLMODE` | `prefer` par défaut (fonctionne en local et sur Render) ; mettre `require` si le serveur l'exige |
| `DASHBOARD_USER`, `DASHBOARD_PASSWORD` | Identifiants Basic Auth du dashboard et des stats |

## Déploiement (Render)

Le `Procfile` lance `gunicorn Controllers.review_controller:app`.

Render limite à une seule base PostgreSQL gratuite par compte : ce projet est pensé pour **réutiliser une base PostgreSQL Render existante** (ici celle de Banking API) plutôt que d'en créer une nouvelle. La table `reviews` est isolée des tables existantes (`db/schema.sql` ne fait qu'un `CREATE TABLE IF NOT EXISTS`).

1. Sur Render, ouvrir la base PostgreSQL existante → onglet **Connect** → noter les champs *Hostname*, *Database*, *Username*, *Password* :
   - **External** (host en `*.render.com`) pour s'y connecter depuis sa machine.
   - **Internal** (host en `*-a` interne, sans port public) pour la connexion depuis un service Render vers un autre.
2. En local, avec les valeurs **externes** dans `.env` : `python db/init_db.py` crée la table `reviews` sans toucher aux tables de Banking API.
3. Créer le Web Service Render relié à ce repo, avec les variables `DB_*` renseignées avec les valeurs **internes** (plus rapide, reste sur le réseau Render) et `DASHBOARD_USER`/`DASHBOARD_PASSWORD` au choix.
