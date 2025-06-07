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
import subprocess
import datetime
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


def push_to_git(output_file: str, domains_count: int, ips_count: int):
    """
    Pousse le fichier JSON vers le repository Git
    
    Args:
        output_file (str): Nom du fichier JSON créé
        domains_count (int): Nombre de domaines traités
        ips_count (int): Nombre total d'IPs trouvées
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Résultats IP - {timestamp} - {domains_count} domaines, {ips_count} IPs"
        
        print(f"\nPush vers Git...")
        
        # Ajouter le fichier JSON
        subprocess.run(['git', 'add', output_file], check=True, capture_output=True)
        print(f"  → Fichier {output_file} ajouté")
        
        # Créer le commit
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)
        print(f"  → Commit créé: {commit_message}")
        
        # Pousser vers origin
        subprocess.run(['git', 'push', 'origin', 'master'], check=True, capture_output=True)
        print(f"  → Push vers GitHub réussi")
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur Git: {e}")
        print("Le fichier JSON a été sauvegardé localement mais n'a pas pu être poussé vers Git.")
    except Exception as e:
        print(f"Erreur inattendue lors du push Git: {e}")


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
    parser.add_argument(
        '--no-git',
        action='store_true',
        help="Ne pas pousser le résultat vers Git automatiquement"
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
    
    # Push vers Git si demandé
    if not args.no_git:
        push_to_git(args.output, len(domains), total_ips)
    else:
        print(f"\nPush Git désactivé (--no-git)")


if __name__ == "__main__":
    main()