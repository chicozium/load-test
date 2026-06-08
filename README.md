# Load Test

Test de charge avec Locust — crawl automatique des URLs du site via sitemap et HTML.

## Prérequis

- Python 3.11+
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

L'URL cible se configure via la variable d'environnement `TARGET_URL`.
Par défaut : `https://www.greatcom-dz.com`

## Lancer en local

### Avec interface web

```bash
TARGET_URL=https://ton-site.com /usr/local/opt/python@3.11/bin/python3.11 -m locust -f locustfile.py
```

Ouvre **http://localhost:8089** et configure :
- **Number of users** — ex: `500`
- **Spawn rate** — ex: `50`
- **Host** — ton URL

### Sans interface (headless)

```bash
TARGET_URL=https://ton-site.com /usr/local/opt/python@3.11/bin/python3.11 -m locust -f locustfile.py \
  --headless \
  --users 500 \
  --spawn-rate 50 \
  --run-time 3m
```

## Lancer depuis GitHub Actions

1. Va sur **Actions** → **Load Test** → **Run workflow**
2. Configure les paramètres :
   - `URL cible` — ex: `https://ton-site.com`
   - `Nombre d'users par worker` — défaut: `2000`
   - `Durée du test` — défaut: `10m`
3. Clique **Run workflow**

Le test lance **10 workers en parallèle** depuis des IPs différentes → **20 000 users simultanés** au total.

## Paramètres

| Paramètre | Description | Défaut |
|---|---|---|
| `--users` | Nombre d'utilisateurs simultanés | 2000 |
| `--spawn-rate` | Utilisateurs ajoutés par seconde | 200 |
| `--run-time` | Durée du test | 10m |

## Métriques à surveiller

- **RPS** — requêtes par seconde
- **Response time** — temps de réponse moyen
- **Failures/s** — requêtes échouées → indique la saturation du serveur
