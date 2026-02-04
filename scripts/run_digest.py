#!/usr/bin/env python3
"""
Executive News Digest - Main Orchestrator
Runs daily at 7:00 AM EST to generate and send the news digest
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

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
        self.sender = EmailSender(recipient="johnyin@aisemble.ca")
        self.log_file = self.work_dir / "digest_log.txt"
    
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
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
            
            # In production, this would call an LLM API
            # For now, using mock commentary
            commentaries = self.generator.create_mock_commentary(news_digest)
            
            # TODO: Replace with actual LLM calls:
            # prompts = self.generator.generate_all_commentary(news_digest)
            # commentaries = self.call_llm_for_commentary(prompts)
            
            self.log("Generated commentary from all three executives")
            
            # Save commentary
            commentary_file = self.work_dir / "commentary_output.json"
            with open(commentary_file, 'w') as f:
                json.dump(commentaries, f, indent=2)
            self.log(f"Saved commentary to {commentary_file}")
            
            # Step 3: Translate to Chinese
            self.log("Step 3: Translating to Simplified Chinese...")
            
            # In production, this would call an LLM API for translation
            # For now, using mock translation
            translated = self.translator.create_mock_translation(news_digest, commentaries)
            
            # TODO: Replace with actual LLM translation:
            # translation_prompts = {
            #     "news": self.translator.translate_headlines(news_digest),
            #     "commentary": self.translator.translate_commentary(commentaries)
            # }
            # translated = self.call_llm_for_translation(translation_prompts)
            
            self.log("Translation completed")
            
            # Save translation
            translation_file = self.work_dir / "translated_digest.json"
            with open(translation_file, 'w', encoding='utf-8') as f:
                json.dump(translated, f, indent=2, ensure_ascii=False)
            self.log(f"Saved translation to {translation_file}")
            
            # Step 4: Format and send email
            self.log("Step 4: Formatting and sending email...")
            
            english_content = {
                "news": news_digest,
                "commentary": commentaries
            }
            
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
    
    def call_llm_for_commentary(self, prompts: dict) -> dict:
        """
        Call LLM API to generate commentary
        This should be implemented with actual LLM API calls
        """
        # TODO: Implement with Claude API or similar
        # Example:
        # import anthropic
        # client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        # 
        # commentaries = {}
        # for exec_key, prompt in prompts.items():
        #     response = client.messages.create(
        #         model="claude-sonnet-4",
        #         max_tokens=1000,
        #         messages=[{"role": "user", "content": prompt}]
        #     )
        #     commentaries[exec_key] = response.content[0].text
        # 
        # return commentaries
        pass
    
    def call_llm_for_translation(self, prompts: dict) -> dict:
        """
        Call LLM API to translate content
        This should be implemented with actual LLM API calls
        """
        # TODO: Implement with Claude API or similar
        pass

def main():
    """Main entry point"""
    orchestrator = DigestOrchestrator()
    success = orchestrator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
