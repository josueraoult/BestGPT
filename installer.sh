#!/bin/bash

echo -e "\033[1;36m"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   INSTALLATION DE BESTGPT                   ║"
echo "║         Orchestrateur Intelligent d'APIs IA                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Vérification des dépendances
echo -e "\033[1;33m[+] Vérification des dépendances...\033[0m"

if ! command -v curl &> /dev/null; then
    echo -e "\033[1;31m[!] Installation de curl...\033[0m"
    pkg install curl -y
fi

if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;31m[!] Installation de python3...\033[0m"
    pkg install python -y
fi

# Donner les permissions d'exécution
chmod +x bestGPT.sh

echo -e "\033[1;32m"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   INSTALLATION RÉUSSIE                      ║"
echo "║                                                              ║"
echo "║  Usage: ./bestGPT.sh (mode interactif)                      ║"
echo "║         ./bestGPT.sh \"Votre question\" (mode ligne de cmd)  ║"
echo "║                                                              ║"
echo "║  Créateur: Josué Raoult Drogba                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"
