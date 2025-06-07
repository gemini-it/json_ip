#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour résoudre les adresses IP des sites web
Lit une liste de sites depuis un fichier txt et génère un JSON avec les IPs
"""

import socket
import json
import sys
import argparse
from typing import Dict, List, Optional


def resolve_domain_ips(domain: str) -> List[str]:
    """
    Résout toutes les adresses IP d'un domaine
    
    Args:
        domain (str): Le nom de domaine à résoudre
        
    Returns:
        List[str]: Liste des adresses IP trouvées
    """
    ips = []
    try:
        # Nettoyer le domaine (enlever http/https et www si présent)
        clean_domain = domain.strip()
        if clean_domain.startswith(('http://', 'https://')):
            clean_domain = clean_domain.split('://', 1)[1]
        if clean_domain.startswith('www.'):
            clean_domain = clean_domain[4:]
        
        # Enlever le chemin s'il y en a un
        clean_domain = clean_domain.split('/')[0]
        
        # Résoudre les adresses IP
        result = socket.getaddrinfo(clean_domain, None)
        for addr_info in result:
            ip = addr_info[4][0]
            if ip not in ips:
                ips.append(ip)
                
    except socket.gaierror as e:
        print(f"Erreur lors de la résolution de {domain}: {e}")
    except Exception as e:
        print(f"Erreur inattendue pour {domain}: {e}")
    
    return ips


def read_domains_from_file(file_path: str) -> List[str]:
    """
    Lit la liste des domaines depuis un fichier txt
    
    Args:
        file_path (str): Chemin vers le fichier contenant les domaines
        
    Returns:
        List[str]: Liste des domaines
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            # Séparer par les virgules et nettoyer les espaces
            domains = [domain.strip() for domain in content.split(',') if domain.strip()]
            return domains
    except FileNotFoundError:
        print(f"Erreur: Le fichier {file_path} n'existe pas.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        sys.exit(1)


def save_results_to_json(results: Dict[str, List[str]], output_file: str):
    """
    Sauvegarde les résultats dans un fichier JSON
    
    Args:
        results (Dict[str, List[str]]): Dictionnaire domaine -> liste d'IPs
        output_file (str): Chemin du fichier de sortie JSON
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(results, file, indent=2, ensure_ascii=False)
        print(f"Résultats sauvegardés dans {output_file}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        sys.exit(1)


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Résout les adresses IP des sites web depuis un fichier txt"
    )
    parser.add_argument(
        'input_file',
        help="Fichier txt contenant les sites web séparés par des virgules"
    )
    parser.add_argument(
        '-o', '--output',
        default='ip_results.json',
        help="Fichier de sortie JSON (défaut: ip_results.json)"
    )
    
    args = parser.parse_args()
    
    print(f"Lecture des domaines depuis {args.input_file}...")
    domains = read_domains_from_file(args.input_file)
    
    if not domains:
        print("Aucun domaine trouvé dans le fichier.")
        sys.exit(1)
    
    print(f"Résolution des adresses IP pour {len(domains)} domaine(s)...")
    
    results = {}
    for i, domain in enumerate(domains, 1):
        print(f"[{i}/{len(domains)}] Résolution de {domain}...")
        ips = resolve_domain_ips(domain)
        results[domain] = ips
        
        if ips:
            print(f"  → {len(ips)} adresse(s) IP trouvée(s): {', '.join(ips)}")
        else:
            print(f"  → Aucune adresse IP trouvée")
    
    print(f"\nSauvegarde des résultats...")
    save_results_to_json(results, args.output)
    
    # Afficher un résumé
    total_ips = sum(len(ips) for ips in results.values())
    domains_with_ips = sum(1 for ips in results.values() if ips)
    
    print(f"\n=== RÉSUMÉ ===")
    print(f"Domaines traités: {len(domains)}")
    print(f"Domaines résolus: {domains_with_ips}")
    print(f"Total d'adresses IP: {total_ips}")


if __name__ == "__main__":
    main()