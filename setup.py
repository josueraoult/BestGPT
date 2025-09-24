#!/usr/bin/env python3
# Installation silencieuse

import subprocess
import sys

def main():
    print("🔧 Configuration du système...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✅ Système prêt.")
        print("\n💡 Utilisation: python3 stealthgpt.py")
        print("   Ou mode direct: python3 stealthgpt.py 'votre question'")
    except:
        print("❌ Installation échouée. Installez 'requests' manuellement.")

if __name__ == "__main__":
    main()
