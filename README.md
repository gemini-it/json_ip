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
# Utiliser le fichier d'exemple fourni (avec push Git automatique)
python resolve_ips.py sites_exemple.txt

# Spécifier un fichier de sortie personnalisé
python resolve_ips.py sites_exemple.txt -o mes_resultats.json

# Désactiver le push Git automatique
python resolve_ips.py sites_exemple.txt --no-git

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

Le script génère plusieurs fichiers :

### Fichier de sortie principal (format détaillé)
```json
{
  "google.com": ["142.250.185.78", "2a00:1450:4007:80c::200e"],
  "github.com": ["140.82.121.4"],
  "python.org": ["151.101.193.223", "151.101.1.223"]
}
```

### Fichiers automatiquement poussés vers Git
- **iplist.json** (format OPNsense) :
```json
[
  "142.250.185.78",
  "140.82.121.4",
  "151.101.193.223"
]
```

- **iplist.txt** (format texte, une IP par ligne) :
```
142.250.185.78
140.82.121.4
151.101.193.223
```

## Fonctionnalités

- ✅ Résolution DNS automatique
- ✅ Support IPv4 et IPv6
- ✅ Nettoyage automatique des URLs (suppression de http/https, www, chemins)
- ✅ Gestion des erreurs de résolution
- ✅ Affichage du progrès en temps réel
- ✅ Résumé des résultats
- ✅ Sortie JSON formatée
- ✅ **Push automatique vers Git** après chaque exécution
- ✅ Option pour désactiver le push Git (--no-git)
- ✅ **Génération automatique de iplist.json et iplist.txt** pour intégration OPNsense

## Utilisation avec OPNsense

Ce script est conçu pour alimenter automatiquement des alias OPNsense. Après chaque exécution, les fichiers suivants sont disponibles sur GitHub :

### Configuration d'alias OPNsense
1. **Firewall → Aliases → Add**
2. **Type** : `URL Table in JSON format (IPs)`
3. **URL** : `https://raw.githubusercontent.com/gemini-it/json_ip/master/iplist.json`
4. **Fréquence de rafraîchissement** : selon vos besoins (ex: toutes les heures)

### Alternative format texte
Pour d'autres usages, le format texte est également disponible :
- **URL** : `https://raw.githubusercontent.com/gemini-it/json_ip/master/iplist.txt`

## Fichiers

- `resolve_ips.py` : Script principal
- `sites_exemple.txt` : Fichier d'exemple avec des sites web populaires
- `ip_results.json` : Fichier de sortie par défaut (généré après exécution)
- `README.md` : Ce fichier de documentation