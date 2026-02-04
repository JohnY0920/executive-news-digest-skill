#!/usr/bin/env python3
"""
Executive News Digest - Main Orchestrator
Runs daily at 7:00 AM EST to generate and send the news digest
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / '.env')

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from news_fetcher import NewsFetcher
from commentary_generator import CommentaryGenerator
from translator import DigestTranslator
from email_sender import EmailSender

class DigestOrchestrator:
    def __init__(self):
        self.work_dir = script_dir
        self.fetcher = NewsFetcher()
        self.generator = CommentaryGenerator()
        self.translator = DigestTranslator()
        self.sender = EmailSender(recipient=os.environ.get('RECIPIENT_EMAIL', 'johnyin@aisemble.ca'))
        self.log_file = self.work_dir / "digest_log.txt"
        
        # LLM configuration
        self.gemini_key = os.environ.get('GEMINI_API_KEY')
        self.kimi_key = os.environ.get('KIMI_API_KEY')
    
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_message + '\n')
        except:
            pass
    
    def call_llm_for_commentary(self, prompts: dict) -> dict:
        """Call LLM API to generate commentary (Gemini Flash with Kimi fallback)"""
        commentaries = {}
        
        for exec_key, prompt in prompts.items():
            self.log(f"Generating commentary for {exec_key}...")
            
            # Try Gemini Flash first (using REST API)
            try:
                import requests
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
                }
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    commentaries[exec_key] = data['candidates'][0]['content']['parts'][0]['text']
                    self.log(f"✓ {exec_key} commentary generated via Gemini Flash")
                    time.sleep(0.5)  # Rate limiting
                    continue
                else:
                    raise Exception(f"Gemini API returned {response.status_code}: {response.text}")
            except Exception as e:
                self.log(f"Gemini Flash failed for {exec_key}: {e}")
            
            # Fallback to Kimi K2.5
            try:
                import requests
                headers = {
                    "Authorization": f"Bearer {self.kimi_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "moonshot-v1-8k",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
                response = requests.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    commentaries[exec_key] = data['choices'][0]['message']['content']
                    self.log(f"✓ {exec_key} commentary generated via Kimi K2.5")
                    time.sleep(1)  # Rate limiting
                else:
                    raise Exception(f"Kimi API returned {response.status_code}")
            except Exception as e:
                self.log(f"Kimi fallback failed for {exec_key}: {e}")
                # Use mock as last resort
                commentaries[exec_key] = self.generator.create_mock_commentary({})[exec_key]
                self.log(f"⚠ Using mock commentary for {exec_key}")
        
        return commentaries
    
    def call_llm_for_translation(self, content: dict) -> dict:
        """Call LLM API to translate content to Simplified Chinese"""
        self.log("Translating to Simplified Chinese...")
        
        # Prepare translation prompt
        translation_request = {
            "news": content["news"],
            "commentary": content["commentary"]
        }
        
        prompt = f"""Translate the following news digest to Simplified Chinese (简体中文).
Maintain professional business terminology and keep the structure intact.

Input:
{json.dumps(translation_request, indent=2, ensure_ascii=False)}

Output the translation in the same JSON structure, with all text translated to Simplified Chinese.
Only output valid JSON, no explanation."""

        # Try Gemini Flash first (using REST API)
        try:
            import requests
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 4096}
            }
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                result_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
                # Extract JSON from response
                if '```json' in result_text:
                    result_text = result_text.split('```json')[1].split('```')[0].strip()
                elif '```' in result_text:
                    result_text = result_text.split('```')[1].split('```')[0].strip()
                translated = json.loads(result_text)
                self.log("✓ Translation completed via Gemini Flash")
                return translated
            else:
                raise Exception(f"Gemini API returned {response.status_code}: {response.text}")
        except Exception as e:
            self.log(f"Gemini Flash translation failed: {e}")
        
        # Fallback to Kimi K2.5
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {self.kimi_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "moonshot-v1-8k",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            response = requests.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                result_text = data['choices'][0]['message']['content'].strip()
                if '```json' in result_text:
                    result_text = result_text.split('```json')[1].split('```')[0].strip()
                elif '```' in result_text:
                    result_text = result_text.split('```')[1].split('```')[0].strip()
                translated = json.loads(result_text)
                self.log("✓ Translation completed via Kimi K2.5")
                return translated
            else:
                raise Exception(f"Kimi API returned {response.status_code}")
        except Exception as e:
            self.log(f"Kimi translation failed: {e}")
        
        # Use mock translation as last resort
        self.log("⚠ Using mock translation")
        return self.translator.create_mock_translation(content["news"], content["commentary"])
    
    def run(self):
        """Main execution flow"""
        self.log("=" * 60)
        self.log("Starting Executive News Digest Generation")
        self.log("=" * 60)
        
        try:
            # Step 1: Fetch news
            self.log("Step 1: Fetching news from sources...")
            news_digest = self.fetcher.fetch_all_news()
            self.log(f"Fetched {sum(len(v) for v in news_digest.values())} headlines")
            
            # Save raw news
            news_file = self.work_dir / "news_digest_raw.json"
            with open(news_file, 'w') as f:
                json.dump(news_digest, f, indent=2)
            self.log(f"Saved raw news to {news_file}")
            
            # Step 2: Generate commentary
            self.log("Step 2: Generating executive commentary...")
            prompts = self.generator.generate_all_commentary(news_digest)
            commentaries = self.call_llm_for_commentary(prompts)
            self.log("Generated commentary from all three executives")
            
            # Save commentary
            commentary_file = self.work_dir / "commentary_output.json"
            with open(commentary_file, 'w') as f:
                json.dump(commentaries, f, indent=2)
            self.log(f"Saved commentary to {commentary_file}")
            
            # Step 3: Translate to Chinese
            self.log("Step 3: Translating to Simplified Chinese...")
            english_content = {
                "news": news_digest,
                "commentary": commentaries
            }
            translated = self.call_llm_for_translation(english_content)
            self.log("Translation completed")
            
            # Save translation
            translation_file = self.work_dir / "translated_digest.json"
            with open(translation_file, 'w', encoding='utf-8') as f:
                json.dump(translated, f, indent=2, ensure_ascii=False)
            self.log(f"Saved translation to {translation_file}")
            
            # Step 4: Format and send email
            self.log("Step 4: Formatting and sending email...")
            
            chinese_content = translated
            
            # Save HTML preview
            preview_file = self.work_dir / "digest_preview.html"
            self.sender.save_html_preview(english_content, chinese_content, str(preview_file))
            self.log(f"Saved HTML preview to {preview_file}")
            
            # Send email
            success = self.sender.send_email(english_content, chinese_content)
            
            if success:
                self.log("✅ Email sent successfully!")
            else:
                self.log("❌ Failed to send email")
                return False
            
            self.log("=" * 60)
            self.log("Executive News Digest completed successfully!")
            self.log("=" * 60)
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error: {e}")
            import traceback
            self.log(traceback.format_exc())
            return False

def main():
    """Main entry point"""
    orchestrator = DigestOrchestrator()
    success = orchestrator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
