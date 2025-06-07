# Résolveur d'adresses IP

Ce script Python permet de résoudre les adresses IP de sites web à partir d'une liste fournie dans un fichier texte.

## Installation

1. Créer et activer l'environnement virtuel :
```bash
python -m venv venv
venv\Scripts\activate.bat  # Windows
```

2. Le script utilise uniquement des modules Python standard, aucune installation supplémentaire n'est nécessaire.

## Utilisation

### Syntaxe de base
```bash
python resolve_ips.py <fichier_sites.txt> [-o fichier_sortie.json]
```

### Exemples
```bash
# Utiliser le fichier d'exemple fourni
python resolve_ips.py sites_exemple.txt

# Spécifier un fichier de sortie personnalisé
python resolve_ips.py sites_exemple.txt -o mes_resultats.json

# Afficher l'aide
python resolve_ips.py -h
```

## Format du fichier d'entrée

Le fichier d'entrée doit contenir les sites web séparés par des virgules. Exemple :
```
google.com, github.com, stackoverflow.com, python.org
```

Le script accepte différents formats :
- `google.com`
- `www.google.com`
- `https://google.com`
- `http://www.google.com/path`

## Format de sortie

Le script génère un fichier JSON avec la structure suivante :
```json
{
  "google.com": ["142.250.185.78", "2a00:1450:4007:80c::200e"],
  "github.com": ["140.82.121.4"],
  "python.org": ["151.101.193.223", "151.101.1.223"]
}
```

## Fonctionnalités

- ✅ Résolution DNS automatique
- ✅ Support IPv4 et IPv6
- ✅ Nettoyage automatique des URLs (suppression de http/https, www, chemins)
- ✅ Gestion des erreurs de résolution
- ✅ Affichage du progrès en temps réel
- ✅ Résumé des résultats
- ✅ Sortie JSON formatée

## Fichiers

- `resolve_ips.py` : Script principal
- `sites_exemple.txt` : Fichier d'exemple avec des sites web populaires
- `ip_results.json` : Fichier de sortie par défaut (généré après exécution)
- `README.md` : Ce fichier de documentation