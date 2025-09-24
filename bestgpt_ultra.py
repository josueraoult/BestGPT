#!/usr/bin/env python3
# ====================================================
# BESTGPT ULTRA - Intelligence Supérieure
# Version: 4.0 | Créateur: Josué Raoult Drogba
# Repo: https://github.com/josueraoult/BestGPT
# ====================================================

import requests
import json
import urllib.parse
import concurrent.futures
import time
import re
import sys
from typing import Dict, List, Tuple, Optional

class BestGPTUltra:
    def __init__(self):
        self.apis = {
            "gemini": "https://aryanapi.up.railway.app/api/gemini?prompt={prompt}",
            "gemini-proxy": "https://aryanapi.up.railway.app/api/gemini-proxy2?prompt={prompt}",
            "deepseek": "https://aryanapi.up.railway.app/api/deepseek3?prompt={prompt}",
            "brave": "https://aryanapi.up.railway.app/api/brave?prompt={prompt}",
            "gpt3": "https://aryanapi.up.railway.app/api/gpt-3.5-turbo?uid=123&prompt={prompt}",
            "powerbrain": "https://aryanapi.up.railway.app/api/powerbrain?uid=1&prompt={prompt}"
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; BestGPT-Ultra/4.0)',
            'Accept': '*/*'
        })
        
        print("🔥 BESTGPT ULTRA - Intelligence Collective")
        print("📡 Chargement de 6 APIs IA...")

    def smart_extract(self, data: str, api_name: str) -> Optional[str]:
        """Extraction intelligente multi-formats"""
        try:
            if not data or data.strip() == "":
                return None
                
            data = data.strip()
            
            # Essai 1: JSON direct
            try:
                json_data = json.loads(data)
                if isinstance(json_data, dict):
                    for key in ['result', 'response', 'answer', 'text', 'content', 'message']:
                        if key in json_data and json_data[key]:
                            result = str(json_data[key]).strip()
                            if result and result != "null":
                                return result
                    # Prendre la première valeur string
                    for value in json_data.values():
                        if isinstance(value, str) and value.strip():
                            return value.strip()
            except:
                pass
            
            # Essai 2: Regex patterns
            patterns = [
                r'"result"\s*:\s*"([^"]+)"',
                r'"response"\s*:\s*"([^"]+)"', 
                r'"answer"\s*:\s*"([^"]+)"',
                r'"text"\s*:\s*"([^"]+)"',
                r'result[^"]*"([^"]+)"',
                r'response[^"]*"([^"]+)"'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, data, re.IGNORECASE)
                if match:
                    result = match.group(1).strip()
                    if result and len(result) > 5:
                        return result
            
            # Essai 3: Nettoyage et retour texte brut
            clean_data = re.sub(r'^{[^}]*}', '', data)  # Enlever objets JSON vides
            clean_data = re.sub(r'\s+', ' ', clean_data).strip()
            
            if len(clean_data) > 10:
                return clean_data
                
        except Exception as e:
            print(f"⚠️  Erreur extraction {api_name}: {e}")
            
        return None

    def call_api(self, api_name: str, prompt: str) -> Tuple[str, Optional[str], int]:
        """Appel d'API avec gestion d'erreur robuste"""
        try:
            encoded_prompt = urllib.parse.quote(prompt)
            url = self.apis[api_name].format(prompt=encoded_prompt)
            
            print(f"🔄 {api_name}...")
            
            response = self.session.get(url, timeout=12)
            
            if response.status_code == 200:
                content = response.text.strip()
                if content:
                    extracted = self.smart_extract(content, api_name)
                    if extracted and len(extracted) > 15:
                        print(f"✅ {api_name} → {len(extracted)} caractères")
                        return api_name, extracted, 1
                    else:
                        print(f"❌ {api_name} → Réponse invalide")
                else:
                    print(f"❌ {api_name} → Contenu vide")
            else:
                print(f"❌ {api_name} → HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ {api_name} → Timeout")
        except requests.exceptions.RequestException as e:
            print(f"🌐 {api_name} → Erreur réseau")
        except Exception as e:
            print(f"💥 {api_name} → Erreur: {str(e)[:50]}")
            
        return api_name, None, 0

    def quality_score(self, text: str) -> int:
        """Score de qualité avancé"""
        if not text or len(text) < 10:
            return 0
            
        score = 0
        
        # Longueur
        length = len(text)
        if length > 150: score += 3
        elif length > 80: score += 2
        elif length > 30: score += 1
        
        # Structure
        if '.' in text: score += 2
        if '?' in text or '!' in text: score += 1
        if any(mark in text for mark in [',', ';', ':']): score += 1
        
        # Contenu riche
        if any(word in text.lower() for word in ['exemple', 'détaillé', 'premièrement', 'ensuite']):
            score += 2
        if any(char.isdigit() for char in text): score += 1
        
        return score

    def merge_responses(self, responses: Dict[str, str]) -> str:
        """Fusion intelligente des meilleures réponses"""
        if not responses:
            return "❌ Aucune réponse valide reçue. Vérifiez votre connexion Internet."
        
        # Calcul des scores
        scored = [(api, resp, self.quality_score(resp)) for api, resp in responses.items()]
        scored.sort(key=lambda x: x[2], reverse=True)
        
        # Filtrage des réponses de qualité
        valid_responses = [s for s in scored if s[2] > 0]
        
        if not valid_responses:
            # Fallback: prendre la plus longue réponse
            longest = max(responses.items(), key=lambda x: len(x[1]))
            return f"📝 {longest[0]}: {longest[1]}"
        
        if len(valid_responses) == 1:
            # Une seule bonne réponse
            api, resp, score = valid_responses[0]
            return f"🎯 **Meilleure réponse ({api})**\n\n{resp}"
        
        # Fusion multi-sources
        result = f"💫 **SYNTHÈSE BESTGPT** ({len(valid_responses)} sources)\n\n"
        
        for i, (api, resp, score) in enumerate(valid_responses[:3], 1):
            result += f"🔍 **Source {i} - {api}** (qualité: {score}/10)\n"
            result += f"{resp}\n\n"
        
        result += "🌟 *Analyse collective terminée*"
        return result

    def process(self, prompt: str) -> str:
        """Traitement principal"""
        print(f"\n🚀 **Question:** {prompt}")
        print("=" * 50)
        
        start_time = time.time()
        responses = {}
        
        # Appels parallèles
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self.call_api, api, prompt): api for api in self.apis}
            
            for future in concurrent.futures.as_completed(futures):
                api, response, success = future.result()
                if success:
                    responses[api] = response
        
        duration = time.time() - start_time
        print(f"\n📊 **Résultats:** {len(responses)}/{len(self.apis)} APIs ont répondu")
        print(f"⏱️  **Temps:** {duration:.2f}s")
        
        return self.merge_responses(responses)

    def interactive(self):
        """Mode conversationnel"""
        print("\n" + "="*60)
        print("💬 **BESTGPT ULTRA - MODE INTERACTIF**")
        print("Tapez 'quit' pour quitter")
        print("="*60)
        
        while True:
            try:
                prompt = input("\n🤖 **Vous:** ").strip()
                
                if prompt.lower() in ['quit', 'exit', 'q']:
                    print("👋 Au revoir!")
                    break
                    
                if not prompt:
                    continue
                
                response = self.process(prompt)
                print(f"\n💫 **BestGPT:**\n{response}")
                print("\n" + "-"*50)
                
            except KeyboardInterrupt:
                print("\n👋 Interruption - Au revoir!")
                break
            except Exception as e:
                print(f"💥 Erreur: {e}")

def main():
    """Point d'entrée"""
    try:
        gpt = BestGPTUltra()
        
        if len(sys.argv) > 1:
            # Mode ligne de commande
            query = " ".join(sys.argv[1:])
            result = gpt.process(query)
            print(f"\n💫 **Réponse:**\n{result}")
        else:
            # Mode interactif
            gpt.interactive()
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
