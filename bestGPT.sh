#!/bin/bash

# =============================================
# BESTGPT - Orchestrateur Intelligent d'APIs IA
# Version: 2.0 | Créateur: Josué Raoult Drogba
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

# APIs disponibles avec leurs endpoints
declare -A APIs=(
    ["gemini"]="https://aryanapi.up.railway.app/api/geminii?prompt="
    ["gemini-proxy"]="https://aryanapi.up.railway.app/api/gemini-proxy2?prompt="
    ["deepseek"]="https://aryanapi.up.railway.app/api/deepseek3?prompt="
    ["brave"]="https://aryanapi.up.railway.app/api/brave?prompt="
    ["llama"]="https://aryanapi.up.railway.app/api/llama-4-maverick-17b-128e-instruct?uid=123&prompt="
    ["gpt3"]="https://aryanapi.up.railway.app/api/gpt-3.5-turbo?prompt="
    ["powerbrain"]="https://aryanapi.up.railway.app/api/powerbrain?uid=1&prompt="
)

# Fichiers de log et cache
CACHE_DIR="cache"
LOG_FILE="bestgpt.log"
CONFIG_FILE="config.conf"

# Fonction d'initialisation
initialize_system() {
    mkdir -p "$CACHE_DIR"
    touch "$LOG_FILE"
    
    echo -e "${GREEN}[+] Initialisation du système BestGPT...${NC}"
    echo -e "${CYAN}[+] Cache: $CACHE_DIR${NC}"
    echo -e "${CYAN}[+] Log: $LOG_FILE${NC}"
}

# Fonction de logging
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Fonction pour encoder les URLs
urlencode() {
    python3 -c "import urllib.parse; print(urllib.parse.quote('$1'))"
}

# Algorithme intelligent de call API
call_ai_api() {
    local api_name=$1
    local prompt=$2
    local endpoint="${APIs[$api_name]}"
    local encoded_prompt=$(urlencode "$prompt")
    local full_url="${endpoint}${encoded_prompt}"
    
    echo -e "${YELLOW}[→] Interrogation de $api_name...${NC}"
    
    # Utilisation de timeout pour éviter les blocages
    response=$(timeout 30 curl -s -H "User-Agent: BestGPT-Orchestrator/2.0" \
        -H "Accept: application/json" \
        -H "Cache-Control: no-cache" \
        "$full_url" 2>/dev/null)
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ] && [ -n "$response" ]; then
        echo -e "${GREEN}[✓] $api_name a répondu (${#response} caractères)${NC}"
        echo "$response"
        log_message "SUCCESS: $api_name - Taille: ${#response}"
    else
        echo -e "${RED}[✗] $api_name a échoué (Timeout ou réponse vide)${NC}"
        log_message "FAILED: $api_name - Code: $exit_code"
        echo "ERROR"
    fi
}

# Algorithme de scoring des réponses
score_response() {
    local response=$1
    local score=0
    
    # Critères de qualité
    if [ ${#response} -gt 50 ]; then ((score+=2)); fi
    if [[ $response =~ \. ]]; then ((score+=1)); fi
    if [[ $response =~ \? ]]; then ((score+=1)); fi
    if [[ $response =~ [0-9] ]]; then ((score+=1)); fi
    if [[ $response =~ (http|https):// ]]; then ((score+=2)); fi
    
    # Pénalité pour les erreurs
    if [[ $response =~ (error|fail|timeout) ]]; then ((score-=3)); fi
    
    echo $score
}

# Algorithme de fusion intelligente
merge_responses() {
    declare -A responses=()
    declare -A scores=()
    
    local prompt=$1
    echo -e "${PURPLE}[🧠] Début de l'orchestration multi-IA...${NC}"
    
    # Appel parallèle des APIs
    for api in "${!APIs[@]}"; do
        response=$(call_ai_api "$api" "$prompt") &
        responses["$api"]=$response
    done
    
    wait
    
    # Calcul des scores
    echo -e "${CYAN}[📊] Analyse des réponses...${NC}"
    for api in "${!responses[@]}"; do
        if [ "${responses[$api]}" != "ERROR" ]; then
            scores["$api"]=$(score_response "${responses[$api]}")
            echo -e "${BLUE}    $api: Score ${scores[$api]}${NC}"
        else
            scores["$api"]=0
        fi
    done
    
    # Sélection de la meilleure réponse
    local best_api=""
    local best_score=-1000
    
    for api in "${!scores[@]}"; do
        if [ ${scores[$api]} -gt $best_score ]; then
            best_score=${scores[$api]}
            best_api=$api
        fi
    done
    
    if [ -n "$best_api" ] && [ $best_score -gt 0 ]; then
        echo -e "${GREEN}[🎯] Meilleure IA: $best_api (Score: $best_score)${NC}"
        echo "${responses[$best_api]}"
        log_message "BEST_CHOICE: $best_api - Score: $best_score"
    else
        # Fallback: concaténation des réponses valides
        echo -e "${YELLOW}[⚠] Utilisation du mode fallback (fusion)${NC}"
        local fallback_response=""
        for api in "${!responses[@]}"; do
            if [ "${responses[$api]}" != "ERROR" ]; then
                fallback_response+="[From $api] ${responses[$api]}\n\n"
            fi
        done
        echo -e "$fallback_response"
    fi
}

# Interface utilisateur avancée
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   BESTGPT - ORCHESTRATEUR IA                ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  Combinaison Intelligente de 7 APIs IA Différentes         ║"
    echo "║  Algorithme de Scoring et Fusion Avancée                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${GREEN}APIs Disponibles:${NC} Gemini, DeepSeek, Brave, Llama, GPT-3.5, PowerBrain"
    echo -e "${PURPLE}=======================================================${NC}"
}

# Mode interactif
interactive_mode() {
    show_banner
    while true; do
        echo -e "${YELLOW}"
        read -p "🤖 Posez votre question (ou 'quit' pour quitter): " user_prompt
        echo -e "${NC}"
        
        if [ "$user_prompt" = "quit" ] || [ "$user_prompt" = "exit" ]; then
            echo -e "${GREEN}[+] Au revoir !${NC}"
            break
        fi
        
        if [ -n "$user_prompt" ]; then
            echo -e "${BLUE}[⚡] Traitement en cours...${NC}"
            response=$(merge_responses "$user_prompt")
            echo -e "${GREEN}"
            echo "╔══════════════════════════════════════════════════════════════╗"
            echo "║                         RÉPONSE INTELLIGENTE                 ║"
            echo "╠══════════════════════════════════════════════════════════════╣"
            echo -e "$response" | fold -w 60 -s
            echo "╚══════════════════════════════════════════════════════════════╝"
            echo -e "${NC}"
        fi
    done
}

# Mode ligne de commande
cmd_mode() {
    local prompt=$1
    echo -e "${CYAN}[→] Prompt: $prompt${NC}"
    response=$(merge_responses "$prompt")
    echo -e "${GREEN}[✓] Réponse:${NC}"
    echo "$response"
}

# Point d'entrée principal
main() {
    initialize_system
    
    if [ $# -eq 0 ]; then
        interactive_mode
    else
        cmd_mode "$*"
    fi
}

# Gestion des signaux
trap 'echo -e "${RED}[!] Interruption détectée. Au revoir!${NC}"; exit 1' INT TERM

# Lancement
main "$@"
