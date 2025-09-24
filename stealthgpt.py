#!/usr/bin/env python3
# ====================================================
# STEALTHGPT - Réponse IA Unifiée et Propre
# Version: 5.0 | Créateur: Josué Raoult Drogba  
# Interface propre - Fusion invisible
# ====================================================

import requests
import json
import urllib.parse
import concurrent.futures
import time
import re
import sys
import random
from typing import Dict, List, Optional

class StealthGPT:
    def __init__(self):
        self.apis = {
            "gemini": "https://aryanapi.up.railway.app/api/gemini?prompt={prompt}",
            "deepseek": "https://aryanapi.up.railway.app/api/deepseek3?prompt={prompt}", 
            "gpt3": "https://aryanapi.up.railway.app/api/gpt-3.5-turbo?uid=123&prompt={prompt}",
            "brave": "https://aryanapi.up.railway.app/api/brave?prompt={prompt}",
            "powerbrain": "https://aryanapi.up.railway.app/api/powerbrain?uid=1&prompt={prompt}"
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*'
        })
        
        # Styles de réponse pour paraître humain
        self.response_styles = [
            "D'accord, voici ce que je peux vous dire :",
            "Après analyse, voici la réponse :", 
            "Je comprends votre question. Voici :",
            "Excellente question ! Voici ce que j'en pense :",
            "D'après mes informations :",
            "Voici une réponse détaillée :",
            "Je me penche sur votre question. Voici :"
        ]

    def extract_clean_text(self, data: str) -> Optional[str]:
        """Extraction ultra-propre du texte"""
        try:
            if not data or len(data.strip()) < 5:
                return None
                
            data = data.strip()
            
            # Essai JSON
            try:
                json_data = json.loads(data)
                if isinstance(json_data, dict):
                    # Chercher le contenu textuel
                    for key in ['content', 'result', 'response', 'answer', 'text', 'message']:
                        if key in json_data and json_data[key]:
                            text = str(json_data[key]).strip()
                            if text and text.lower() not in ['null', 'none', '']:
                                return self.clean_response(text)
                    
                    # Prendre la première valeur string valide
                    for value in json_data.values():
                        if isinstance(value, str) and len(value.strip()) > 10:
                            return self.clean_response(value.strip())
            except:
                pass
            
            # Nettoyage des réponses brutes
            clean_data = re.sub(r'^{.*?}', '', data)  # Enlever objets JSON
            clean_data = re.sub(r'[\{\}\[\]]', '', clean_data)  # Enlever symboles
            clean_data = re.sub(r'"\w+":', '', clean_data)  # Enlever clés JSON
            clean_data = re.sub(r'\s+', ' ', clean_data).strip()
            
            if len(clean_data) > 15:
                return self.clean_response(clean_data)
                
        except Exception:
            pass
            
        return None

    def clean_response(self, text: str) -> str:
        """Nettoyage et formatage professionnel"""
        # Enlever les tokens techniques
        text = re.sub(r'chatcmpl-\w+', '', text)
        text = re.sub(r'fp_\w+', '', text)
        text = re.sub(r'\{\s*"id".*?\}', '', text)
        text = re.sub(r'tokens?:\s*\d+', '', text)
        
        # Formatage du texte
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.capitalize()
        
        # S'assurer que ça se termine par un point
        if text and text[-1] not in ['.', '!', '?']:
            text += '.'
            
        return text

    def call_api_stealth(self, api_name: str, prompt: str) -> Optional[str]:
        """Appel silencieux d'API"""
        try:
            url = self.apis[api_name].format(prompt=urllib.parse.quote(prompt))
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200 and response.text.strip():
                return self.extract_clean_text(response.text)
                
        except Exception:
            pass
            
        return None

    def score_response(self, text: str) -> int:
        """Évaluation discrète de la qualité"""
        if not text or len(text) < 20:
            return 0
            
        score = 0
        
        # Longueur optimale (ni trop court ni trop long)
        if 50 <= len(text) <= 500:
            score += 3
        elif len(text) > 500:
            score += 1
            
        # Qualité linguistique
        if text.count('.') >= 1: score += 2
        if any(mark in text for mark in [',', ';', ':']): score += 1
        if text[0].isupper() and text[-1] in '.!?': score += 1
        
        # Contenu substantiel
        if any(word in text.lower() for word in [' parce que', ' cependant', ' par exemple', ' donc']):
            score += 2
            
        return score

    def intelligent_merge(self, responses: Dict[str, str]) -> str:
        """Fusion intelligente et invisible"""
        if not responses:
            return "Je n'ai pas pu obtenir d'informations pour le moment. Pouvez-vous reformuler votre question ?"
        
        # Évaluer et trier les réponses
        scored_responses = []
        for api, text in responses.items():
            score = self.score_response(text)
            if score > 0:
                scored_responses.append((text, score))
        
        if not scored_responses:
            # Fallback: prendre la réponse la plus longue
            longest = max(responses.values(), key=len)
            return self.format_final_response(longest)
        
        # Stratégie de fusion avancée
        if len(scored_responses) == 1:
            best_text, best_score = scored_responses[0]
        else:
            # Combiner les meilleurs éléments de chaque réponse
            scored_responses.sort(key=lambda x: x[1], reverse=True)
            
            # Prendre la meilleure réponse comme base
            best_text = scored_responses[0][0]
            
            # Ajouter des éléments des autres réponses si complémentaires
            for text, score in scored_responses[1:2]:  # Juste la deuxième meilleure
                if score > 3:
                    # Extraire des phrases uniques
                    sentences = re.split(r'[.!?]+', text)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if (sentence and len(sentence) > 20 and 
                            sentence not in best_text and 
                            not any(word in sentence.lower() for word in ['error', 'null', 'undefined'])):
                            best_text += " " + sentence + "."
                            break
        
        return self.format_final_response(best_text)

    def format_final_response(self, text: str) -> str:
        """Formatage final pour paraître humain"""
        # Choisir un style aléatoire
        style = random.choice(self.response_styles)
        
        # Nettoyer le texte
        text = self.clean_response(text)
        
        # Limiter la longueur si nécessaire
        if len(text) > 600:
            sentences = re.split(r'[.!?]+', text)
            text = '.'.join(sentences[:3]) + '.'
            
        return f"{style} {text}"

    def process_question(self, prompt: str) -> str:
        """Traitement principal - Interface propre"""
        # Appel parallèle silencieux
        responses = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_api = {
                executor.submit(self.call_api_stealth, api, prompt): api 
                for api in self.apis
            }
            
            for future in concurrent.futures.as_completed(future_to_api):
                result = future.result()
                if result:
                    api_name = future_to_api[future]
                    responses[api_name] = result
        
        # Fusion invisible
        return self.intelligent_merge(responses)

    def interactive_mode(self):
        """Mode interactif épuré"""
        print("\n" + "="*50)
        print("🧠 **SYSTÈME DE RÉPONSE INTELLIGENTE**")
        print("Tapez 'quit' pour quitter")
        print("="*50)
        
        while True:
            try:
                user_input = input("\n👤 **Vous:** ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("🔄 **Système:** Au revoir !")
                    break
                    
                if not user_input:
                    continue
                
                # Affichage sobre du traitement
                print("🔄 **Traitement en cours...**")
                
                # Obtention de la réponse
                response = self.process_question(user_input)
                
                # Affichage unique et propre
                print(f"🤖 **Réponse:** {response}")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n🔄 **Système:** Session terminée.")
                break
            except Exception as e:
                print(f"🤖 **Réponse:** Désolé, une erreur est survenue. Réessayez.")

def main():
    """Point d'entrée"""
    try:
        gpt = StealthGPT()
        
        if len(sys.argv) > 1:
            # Mode ligne de commande discret
            query = " ".join(sys.argv[1:])
            response = gpt.process_question(query)
            print(response)
        else:
            # Mode interactif
            gpt.interactive_mode()
            
    except Exception as e:
        print("Erreur système. Vérifiez votre connexion.")

if __name__ == "__main__":
    main()
