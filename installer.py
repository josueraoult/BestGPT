#!/usr/bin/env python3
# Installateur BestGPT Ultra

import os
import subprocess
import sys

def run_command(cmd):
    """Exécute une commande shell"""
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 INSTALLATION BESTGPT ULTRA")
    print("=" * 50)
    
    # Vérifier Python
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ requis")
        sys.exit(1)
    
    # Installer requests
    print("📦 Installation des dépendances...")
    if not run_command(f"{sys.executable} -m pip install requests"):
        print("❌ Échec installation requests")
        sys.exit(1)
    
    print("✅ Installation terminée!")
    print("\n🎯 **UTILISATION:**")
    print("Mode interactif: python3 bestgpt_ultra.py")
    print("Question directe: python3 bestgpt_ultra.py 'Votre question'")
    print("\n📚 Repo: https://github.com/josueraoult/BestGPT")
    print("👨💻 Créateur: Josué Raoult Drogba")

if __name__ == "__main__":
    main()
