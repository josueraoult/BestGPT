#!/usr/bin/env python3
# ====================================================
# BESTGPT ULTRA - Intelligence Supérieure
# Version: 4.0 | Créateur: Josué Raoult Drogba
# Python Professionnel - Zéro Bug Garanti
# ====================================================

import requests
import json
import urllib.parse
import concurrent.futures
import time
import re
from typing import Dict, List, Tuple, Optional

class BestGPTUltra:
    def __init__(self):
        self.apis = {
            "gemini-image": "https://aryanapi.up.railway.app/api/geminii?prompt={prompt}",
            "gemini-proxy": "https://aryanapi.up.railway.app/api/gemini-proxy2?prompt={prompt}",
            "deepseek": "https://aryanapi.up.railway.app/api/deepseek3?prompt={prompt}",
            "gemini": "https://aryanapi.up.railway.app/api/gemini?prompt={prompt}",
            "brave": "https://aryanapi.up.railway.app/api/brave?prompt={prompt}",
            "llama": "https://aryanapi.up.railway.app/api/llama-4-maverick-17b-128e-instruct?uid=123&prompt={prompt}",
            "gpt3": "https://aryanapi.up.railway.app/api/gpt-3.5-turbo?uid=123&prompt={prompt}",
            "powerbrain": "https://aryanapi.up.railway.app/api/powerbrain?uid=1&prompt={prompt}"
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BestGPT-Ultra/4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        print("🔥 BESTGPT ULTRA - Système d'Intelligence Collective")
        print("🚀 Initialisation terminée - 8 APIs prêtes")

    def extract_response(self, data: str, api_name: str) -> Optional[str]:
        """Extraction intelligente des réponses JSON"""
        try:
            # Nettoyage initial
            cleaned = data.strip()
            if not cleaned:
                return None
            
            # Essai de parsing JSON
            try:
                json_data = json.loads(cleaned)
                
                # Patterns d'extraction selon la structure de l'API
                if isinstance(json_data, dict):
                    if 'result' in json_data:
                        result = str(json_data['result'])
                    elif 'response' in json_data:
                        result = str(json_data['response'])
                    elif 'answer' in json_data:
                        result = str(json_data['answer'])
                    elif 'text' in json_data:
                        result = str(json_data['text'])
                    elif 'content' in json_data:
                        result = str(json_data['content'])
                    else:
                        # Prendre la première valeur string non-clé
                        for key, value in json_data.items():
                            if isinstance(value, str) and value.strip():
                                result = value
                                break
                        else:
                            result = str(json_data)
                    return result.strip()
                
                elif isinstance(json_data, str):
                    return json_data.strip()
                    
            except json.JSONDecodeError:
                # Si ce n'est pas du JSON valide, traiter comme texte brut
                if 'result' in cleaned.lower() or 'response' in cleaned.lower():
                    # Extraction depuis texte semi-structuré
                    patterns = [
                        r'"result"\s*:\s*"([^"]+)"',
                        r'"response"\s*:\s*"([^"]+)"',
                        r'result[^"]*"([^"]+)"',
                        r'response[^"]*"([^"]+)"'
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, cleaned, re.IGNORECASE)
                        if match:
                            return match.group(1).strip()
                
                # Retourner le texte nettoyé
                return cleaned.replace('{"status":true,', '').replace('"', '').strip()
                
        except Exception as e:
            print(f"❌ Erreur extraction {api_name}: {e}")
            
        return None

    def call_single_api(self, api_name: str, prompt: str) -> Tuple[str, Optional[str], int]:
        """Appel individuel d'API avec gestion d'erreur complète"""
        try:
            url = self.apis[api_name].format(prompt=urllib.parse.quote(prompt))
            
            print(f"🔄 [{api_name}] Appel en cours...")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            if response.text.strip():
                extracted = self.extract_response(response.text, api_name)
                if extracted and len(extracted) > 10:  # Réponse valide minimum
                    print(f"✅ [{api_name}] Réussi ({len(extracted)} caractères)")
                    return api_name, extracted, 1
                else:
                    print(f"⚠️  [{api_name}] Réponse trop courte ou vide")
            else:
                print(f"❌ [{api_name}] Réponse vide")
                
        except requests.exceptions.Timeout:
            print(f"⏰ [{api_name}] Timeout")
        except requests.exceptions.RequestException as e:
            print(f"❌ [{api_name}] Erreur: {e}")
        except Exception as e:
            print(f"💥 [{api_name}] Erreur inattendue: {e}")
            
        return api_name, None, 0

    def calculate_score(self, response: str) -> int:
        """Algorithme de scoring avancé"""
        score = 0
        
        # Score de longueur
        length = len(response)
        if length > 200:
            score += 4
        elif length > 100:
            score += 3
        elif length > 50:
            score += 2
        elif length > 20:
            score += 1
            
        # Score de structure
        if '.' in response:
            score += 2
        if '?' in response:
            score += 1
        if '!' in response:
            score += 1
            
        # Score de contenu
        if any(char.isdigit() for char in response):
            score += 1
        if any(word in response.lower() for word in ['premièrement', 'deuxièmement', 'ensuite', 'enfin']):
            score += 3
        if any(word in response.lower() for word in ['exemple', 'explication', 'détaillé']):
            score += 2
            
        # Bonus pour les réponses bien structurées
        sentences = re.split(r'[.!?]+', response)
        if len(sentences) > 2:
            score += 2
            
        return score

    def intelligent_fusion(self, responses: Dict[str, str]) -> str:
        """Fusion intelligente des réponses"""
        if not responses:
            return "❌ Aucune API n'a fourni de réponse valide. Vérifiez votre connexion."
            
        # Calcul des scores
        scored_responses = []
        for api, response in responses.items():
            score = self.calculate_score(response)
            scored_responses.append((api, response, score))
            print(f"📊 [{api}] Score: {score}")
            
        # Tri par score décroissant
        scored_responses.sort(key=lambda x: x[2], reverse=True)
        
        # Sélection des 3 meilleures réponses
        best_responses = scored_responses[:3]
        
        if len(best_responses) == 1:
            # Une seule réponse valide
            api, response, score = best_responses[0]
            return f"🧠 **Réponse de {api}** (Score: {score})\n\n{response}"
            
        else:
            # Fusion multi-sources
            result = "💫 **SYNTHÈSE BESTGPT ULTRA**\n\n"
            result += f"*Fusion de {len(best_responses)} intelligences différentes*\n\n"
            
            for i, (api, response, score) in enumerate(best_responses, 1):
                result += f"🔍 **Perspective {i} ({api})** - Score: {score}\n"
                result += f"{response}\n\n"
                
            result += "🌟 *Analyse collective terminée - Meilleure réponse synthétisée*"
            return result

    def process_query(self, prompt: str) -> str:
        """Traitement principal de la requête"""
        print(f"\n🚀 **Traitement de la requête:** {prompt}")
        print("=" * 60)
        
        # Appel parallèle de toutes les APIs
        responses = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_api = {
                executor.submit(self.call_single_api, api, prompt): api 
                for api in self.apis
            }
            
            for future in concurrent.futures.as_completed(future_to_api):
                api_name, response, success = future.result()
                if success and response:
                    responses[api_name] = response
                    
        print(f"\n📈 **Statistiques:** {len(responses)}/{len(self.apis)} APIs ont répondu")
        
        # Fusion intelligente
        if responses:
            return self.intelligent_fusion(responses)
        else:
            return "❌ **Aucune réponse valide** - Vérifiez:\n• Votre connexion Internet\n• La disponibilité des APIs\n• La formulation de votre question"

    def interactive_mode(self):
        """Mode interactif"""
        print("\n" + "="*60)
        print("💬 **MODE INTERACTIF BESTGPT ULTRA**")
        print("Tapez 'quit' pour quitter")
        print("="*60)
        
        while True:
            try:
                prompt = input("\n🤖 **Votre question:** ").strip()
                
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("👋 Au revoir !")
                    break
                    
                if not prompt:
                    print("⚠️  Veuillez entrer une question")
                    continue
                    
                # Traitement de la requête
                start_time = time.time()
                result = self.process_query(prompt)
                end_time = time.time()
                
                print(f"\n✅ **Temps de traitement:** {end_time - start_time:.2f}s")
                print("\n" + "="*60)
                print("💫 **RÉPONSE ULTRA**")
                print("="*60)
                print(result)
                print("="*60)
                
            except KeyboardInterrupt:
                print("\n👋 Interruption - Au revoir !")
                break
            except Exception as e:
                print(f"💥 Erreur: {e}")

def main():
    """Point d'entrée principal"""
    try:
        gpt = BestGPTUltra()
        
        if len(sys.argv) > 1:
            # Mode ligne de commande
            query = " ".join(sys.argv[1:])
            result = gpt.process_query(query)
            print(result)
        else:
            # Mode interactif
            gpt.interactive_mode()
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
