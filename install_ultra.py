#!/usr/bin/env python3
# Installation automatique BestGPT Ultra

import os
import sys
import subprocess

def check_dependencies():
    """Vérification et installation des dépendances"""
    try:
        import requests
        print("✅ requests déjà installé")
    except ImportError:
        print("📦 Installation de requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    
    print("✅ Toutes les dépendances sont satisfaites")

def main():
    print("🚀 INSTALLATION BESTGPT ULTRA")
    print("=" * 40)
    
    check_dependencies()
    
    # Vérifier que le script principal existe
    if not os.path.exists("bestgpt_ultra.py"):
        print("❌ bestgpt_ultra.py non trouvé!")
        print("📁 Téléchargez le fichier depuis GitHub")
        return
    
    # Rendre exécutable
    os.chmod("bestgpt_ultra.py", 0o755)
    
    print("\n✅ **INSTALLATION TERMINÉE**")
    print("\n🎯 **UTILISATION:**")
    print("Mode interactif: python3 bestgpt_ultra.py")
    print("Question directe: python3 bestgpt_ultra.py 'Votre question'")
    print("\n👨💻 **Crédit:** Josué Raoult Drogba")

if __name__ == "__main__":
    main()
