#!/bin/bash

# =============================================
# BESTGPT ULTRA - Intelligence Supérieure
# Version: 3.0 | Créateur: Josué Raoult Drogba
# =============================================

# Configuration des couleurs
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# APIs AVEC PARAMÈTRES CORRECTS
declare -A APIs=(
    ["gemini-image"]="https://aryanapi.up.railway.app/api/geminii?prompt="
    ["gemini-proxy"]="https://aryanapi.up.railway.app/api/gemini-proxy2?prompt="
    ["deepseek"]="https://aryanapi.up.railway.app/api/deepseek3?prompt="
    ["gemini"]="https://aryanapi.up.railway.app/api/gemini?prompt="
    ["brave"]="https://aryanapi.up.railway.app/api/brave?prompt="
    ["llama"]="https://aryanapi.up.railway.app/api/llama-4-maverick-17b-128e-instruct?uid=123&prompt="
    ["gpt3"]="https://aryanapi.up.railway.app/api/gpt-3.5-turbo?uid=123&prompt="
    ["powerbrain"]="https://aryanapi.up.railway.app/api/powerbrain?uid=1&prompt="
)

# Fichiers de travail
CACHE_DIR="/data/data/com.termux/files/home/bestgpt_cache"
LOG_FILE="$CACHE_DIR/ultra.log"

# Initialisation système
init_system() {
    mkdir -p "$CACHE_DIR"
    touch "$LOG_FILE"
    echo -e "${GREEN}[✓] Système BestGPT Ultra initialisé${NC}"
}

# Encodage URL amélioré
url_encode() {
    echo -n "$1" | python3 -c "
import sys, urllib.parse
print(urllib.parse.quote(sys.stdin.read()))
"
}

# Extraction intelligente du résultat JSON
extract_result() {
    local response="$1"
    
    # Multiple extraction methods
    if echo "$response" | grep -q '"result"'; then
        echo "$response" | python3 -c "
import json, sys
try:
    data = json.loads(sys.stdin.read())
    if 'result' in data:
        print(data['result'])
    elif 'response' in data:
        print(data['response'])
    elif 'answer' in data:
        print(data['answer'])
    else:
        print(''.join(str(v) for v in data.values() if v))
except:
    print(sys.stdin.read().strip())
"
    else
        echo "$response" | sed 's/{"status":true,*//g' | sed 's/{"response":"*//g' | tr -d '"{}' | sed 's/,$//'
    fi
}

# Appel API avec gestion d'erreur avancée
call_ultra_api() {
    local api_name="$1"
    local prompt="$2"
    local encoded_prompt=$(url_encode "$prompt")
    local base_url="${APIs[$api_name]}"
    local full_url="${base_url}${encoded_prompt}"
    
    echo -e "${YELLOW}[→] Interrogation de $api_name...${NC}"
    
    # Timeout court pour performance
    response=$(timeout 20 curl -s -k \
        -H "User-Agent: BestGPT-Ultra/3.0" \
        -H "Accept: */*" \
        "$full_url" 2>/dev/null)
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ] && [ -n "$response" ]; then
        local clean_response=$(extract_result "$response")
        
        if [ -n "$clean_response" ] && [ ${#clean_response} -gt 5 ]; then
            echo -e "${GREEN}[✓] $api_name réussi (${#clean_response} chars)${NC}"
            echo "$clean_response"
            return 0
        fi
    fi
    
    echo -e "${RED}[✗] $api_name échec${NC}"
    return 1
}

# Algorithme de scoring ULTRA avancé
ultra_score() {
    local response="$1"
    local score=0
    
    # Score basé sur la qualité du contenu
    local length=${#response}
    
    # Score de longueur (optimisé)
    if [ $length -gt 100 ]; then score=$((score + 3))
    elif [ $length -gt 50 ]; then score=$((score + 2))
    elif [ $length -gt 20 ]; then score=$((score + 1))
    fi
    
    # Score de structure
    if [[ "$response" =~ \. ]]; then score=$((score + 2)); fi
    if [[ "$response" =~ \? ]]; then score=$((score + 1)); fi
    if [[ "$response" =~ \! ]]; then score=$((score + 1)); fi
    if [[ "$response" =~ \, ]]; then score=$((score + 1)); fi
    
    # Score de contenu
    if [[ "$response" =~ [0-9] ]]; then score=$((score + 1)); fi
    if [[ "$response" =~ (http|www\.) ]]; then score=$((score + 2)); fi
    if [[ "$response" =~ (AI|intelligence|machine learning|deep learning) ]]; then score=$((score + 1)); fi
    
    # Bonus pour les réponses structurées
    if [[ "$response" =~ (premièrement|deuxièmement|en conclusion) ]]; then score=$((score + 2)); fi
    if [[ "$response" =~ (exemple|explication|détaillé) ]]; then score=$((score + 2)); fi
    
    echo $score
}

# Orchestration multi-niveaux ULTRA
ultra_orchestration() {
    local prompt="$1"
    declare -A responses=()
    declare -A scores=()
    
    echo -e "${PURPLE}[🧠] Lancement de l'intelligence supérieure...${NC}"
    
    # Phase 1: Appel parallèle de toutes les APIs
    for api in "${!APIs[@]}"; do
        (
            response=$(call_ultra_api "$api" "$prompt")
            if [ $? -eq 0 ]; then
                responses["$api"]="$response"
                scores["$api"]=$(ultra_score "$response")
            else
                scores["$api"]=0
            fi
        ) &
    done
    
    wait
    
    # Phase 2: Analyse intelligente
    echo -e "${CYAN}[📊] Analyse avancée des réponses...${NC}"
    
    local best_api=""
    local best_score=-1
    local valid_responses=0
    
    for api in "${!scores[@]}"; do
        if [ ${scores[$api]} -gt 0 ]; then
            echo -e "${GREEN}    ${api}: Score ${scores[$api]}${NC}"
            valid_responses=$((valid_responses + 1))
            
            if [ ${scores[$api]} -gt $best_score ]; then
                best_score=${scores[$api]}
                best_api="$api"
            fi
        else
            echo -e "${RED}    ${api}: Aucune réponse valide${NC}"
        fi
    done
    
    # Phase 3: Stratégie de fusion intelligente
    if [ $valid_responses -eq 0 ]; then
        echo -e "${RED}[💥] Aucune API n'a répondu - Vérifiez la connexion${NC}"
        echo "Je suis désolé, aucune intelligence n'est actuellement disponible. Vérifiez votre connexion internet."
        return 1
    elif [ $valid_responses -eq 1 ]; then
        echo -e "${YELLOW}[🎯] Utilisation de la seule réponse disponible: $best_api${NC}"
        echo "${responses[$best_api]}"
    else
        echo -e "${GREEN}[🌟] Fusion de $valid_responses intelligences...${NC}"
        
        # Fusion intelligente (priorité aux meilleures réponses)
        local final_response=""
        local added_apis=0
        
        # Trier les APIs par score
        for api in $(for key in "${!scores[@]}"; do echo "$key:${scores[$key]}"; done | sort -t: -k2 -nr | cut -d: -f1); do
            if [ ${scores[$api]} -gt 2 ] && [ $added_apis -lt 3 ]; then
                if [ $added_apis -gt 0 ]; then
                    final_response+="\n\n─── 🔍 Perspective de ${api} ───\n"
                else
                    final_response+="─── 🧠 Analyse de ${api} ───\n"
                fi
                final_response+="${responses[$api]}"
                added_apis=$((added_apis + 1))
            fi
        done
        
        # Ajouter un résumé synthétique
        if [ $added_apis -gt 1 ]; then
            final_response+="\n\n─── 💫 Synthèse BestGPT Ultra ───\n"
            final_response+="J'ai fusionné les analyses de $added_apis intelligences différentes pour vous offrir la réponse la plus complète possible."
        fi
        
        echo -e "$final_response"
    fi
}

# Interface utilisateur améliorée
show_ultra_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   BESTGPT ULTRA - INTELLIGENCE SUPÉRIEURE   ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  🚀 Algorithme de Fusion Multi-Niveaux                     ║"
    echo "║  🧠 8 APIs IA Synchronisées                                ║"
    echo "║  💫 Scoring Intelligent Avancé                             ║"
    echo "║  🏆 Conçu pour surpasser les IA populaires                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${GREEN}APIs Actives:${NC} Gemini(x3), DeepSeek, Brave, Llama, GPT-3.5, PowerBrain"
    echo -e "${PURPLE}=======================================================${NC}"
}

# Mode conversationnel ultra
ultra_interactive() {
    show_ultra_banner
    
    while true; do
        echo -e "${YELLOW}"
        read -p "💬 Posez votre question (ou 'quit'): " user_prompt
        echo -e "${NC}"
        
        case "$user_prompt" in
            quit|exit|q)
                echo -e "${GREEN}[👋] Au revoir !${NC}"
                break
                ;;
            "")
                echo -e "${YELLOW}[ℹ] Veuillez poser une question${NC}"
                continue
                ;;
            *)
                echo -e "${BLUE}[⚡] Traitement par l'intelligence supérieure...${NC}"
                response=$(ultra_orchestration "$user_prompt")
                
                echo -e "${GREEN}"
                echo "╔══════════════════════════════════════════════════════════════╗"
                echo "║                      RÉPONSE ULTRA                         ║"
                echo "╠══════════════════════════════════════════════════════════════╣"
                echo -e "$response"
                echo "╚══════════════════════════════════════════════════════════════╝"
                echo -e "${NC}"
                ;;
        esac
    done
}

# Point d'entrée principal
main() {
    init_system
    
    if [ $# -ge 1 ]; then
        echo -e "${CYAN}[→] Question: $*${NC}"
        ultra_orchestration "$*"
    else
        ultra_interactive
    fi
}

# Gestion des interruptions
trap 'echo -e "${RED}[!] Arrêt de BestGPT Ultra${NC}"; exit 1' INT TERM

# Lancement
main "$@"
