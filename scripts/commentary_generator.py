#!/usr/bin/env python3
"""
Commentary Generator for Executive News Digest
Generates perspectives from Ray Dalio, Elon Musk, and Warren Buffett
"""

import json
import sys
from typing import Dict, List

class CommentaryGenerator:
    def __init__(self):
        self.executives = {
            "ray_dalio": {
                "name": "Ray Dalio",
                "emoji": "📈",
                "focus": "Macroeconomic patterns, systemic risks, historical parallels",
                "tone": "Analytical, principles-based, long-term cycles"
            },
            "elon_musk": {
                "name": "Elon Musk",
                "emoji": "🚀",
                "focus": "Innovation implications, disruption potential, technological acceleration",
                "tone": "Bold, future-oriented, first-principles thinking"
            },
            "warren_buffett": {
                "name": "Warren Buffett",
                "emoji": "💰",
                "focus": "Business fundamentals, value creation, long-term investment implications",
                "tone": "Wisdom-based, conservative, value-oriented"
            }
        }
    
    def generate_commentary_prompt(self, executive_key: str, news_summary: str) -> str:
        """Generate prompt for executive commentary"""
        executive = self.executives[executive_key]
        
        prompt = f"""Based on today's news headlines covering Economics, World News, Business, and AI Technology, provide commentary as {executive['name']} would analyze the overall themes.

News Summary:
{news_summary}

Your task: Analyze the OVERALL THEMES across all categories from {executive['name']}'s perspective.

Focus on: {executive['focus']}
Tone: {executive['tone']}

Guidelines:
- Analyze overarching patterns and themes, not individual headlines
- Connect different categories (e.g., how economic trends relate to tech developments)
- Provide 2-3 key insights that {executive['name']} would identify
- Be authentic to {executive['name']}'s known thinking patterns and principles
- Keep it concise (3-4 paragraphs maximum)
- Be specific and actionable where possible

Write the commentary now:"""
        
        return prompt
    
    def format_news_summary(self, news_digest: Dict[str, List[Dict]]) -> str:
        """Format news digest into a summary for commentary generation"""
        summary = []
        
        category_names = {
            "economics": "ECONOMICS",
            "world_news": "WORLD NEWS",
            "business": "BUSINESS",
            "ai_technology": "AI TECHNOLOGY"
        }
        
        for category, articles in news_digest.items():
            category_name = category_names.get(category, category.upper())
            summary.append(f"\n{category_name}:")
            for i, article in enumerate(articles, 1):
                summary.append(f"  {i}. {article['title']}")
        
        return "\n".join(summary)
    
    def generate_all_commentary(self, news_digest: Dict[str, List[Dict]]) -> Dict[str, str]:
        """
        Generate commentary from all three executives
        Note: This uses LLM calls which should be handled by the caller
        This method returns the prompts that should be sent to an LLM
        """
        news_summary = self.format_news_summary(news_digest)
        
        commentary_prompts = {}
        for exec_key in self.executives.keys():
            commentary_prompts[exec_key] = self.generate_commentary_prompt(exec_key, news_summary)
        
        return commentary_prompts
    
    def format_commentary_display(self, commentaries: Dict[str, str]) -> str:
        """Format the commentary for display"""
        output = []
        output.append("\n" + "=" * 60)
        output.append("🎭 EXECUTIVE PERSPECTIVES")
        output.append("=" * 60)
        
        for exec_key, commentary in commentaries.items():
            executive = self.executives[exec_key]
            output.append(f"\n{executive['emoji']} {executive['name'].upper()}'S ANALYSIS")
            output.append("-" * 60)
            output.append(commentary)
            output.append("")
        
        return "\n".join(output)
    
    def create_mock_commentary(self, news_digest: Dict[str, List[Dict]]) -> Dict[str, str]:
        """Create mock commentary for testing"""
        return {
            "ray_dalio": """Looking at today's headlines, I see three interconnected themes that reflect the current phase of the long-term debt cycle:

First, the economic indicators suggest we're transitioning from the tightening phase to a more accommodative stance. The Fed's potential rate cuts signal recognition that inflation has been sufficiently contained, though we must remain vigilant about second-order effects. This monetary policy shift will have cascading impacts across asset classes.

Second, the geopolitical landscape shows continued fragmentation alongside selective cooperation. This reflects the fundamental tension between globalization and national interests - a pattern we've seen throughout history during periods of major power transitions. Companies and investors must now navigate multiple spheres of influence rather than one unified global system.

Third, the AI technology developments represent genuine productivity enhancements, but we must distinguish between bubble-driven speculation and real value creation. The regulatory frameworks being discussed are inevitable - every transformative technology eventually faces this societal reckoning. The key is whether regulation enables or stifles innovation.

Overall assessment: We're in a transitional period where old paradigms are giving way to new ones. Successful navigation requires understanding these historical patterns while remaining adaptable to unprecedented developments.""",

            "elon_musk": """Looking at these headlines through first principles: the rate of technological change is accelerating faster than our institutions can adapt, which creates both massive opportunities and systemic risks.

The AI developments are the most significant. We're clearly in an exponential phase - each breakthrough enables the next one faster. The healthcare AI accuracy numbers are real, not hype. But the regulatory frameworks being proposed are already obsolete before implementation. We need regulation that's adaptive and principle-based, not prescriptive.

On the economic front: traditional monetary policy is increasingly ineffective in a world where information and capital move at light speed. Central banks are flying blind with decade-old models while the actual economy operates on entirely different physics. This creates arbitrage opportunities for those who understand both systems.

The business news shows incumbents trying to buy their way into the future through M&A. That rarely works. Real innovation comes from understanding the problem from scratch and building solutions that are 10x better, not 10% better. The companies making genuine R&D investments in hard tech will dominate the next decade.

Bottom line: We're at an inflection point where technological capabilities are outpacing human institutions. The organizations and individuals who can operate at software speed while others are stuck in hardware mindsets will capture disproportionate value.""",

            "warren_buffett": """Today's headlines remind me of a few enduring principles that have guided successful investing for decades.

First, on the economic news: interest rates matter, but they don't change the fundamental value of great businesses. A wonderful business with strong competitive advantages - what we call a moat - will thrive across different interest rate environments. The key is identifying companies with sustainable competitive advantages and competent, honest management. Those factors determine long-term value far more than near-term rate movements.

The business news about earnings and M&A activity shows some companies creating real value and others making expensive mistakes. The best mergers happen when excellent companies buy other excellent companies at fair prices. Too often, we see mediocre businesses overpaying for acquisitions to mask underlying problems. That never ends well.

On technology and AI: I've never been able to predict which technologies will win, so I focus on businesses I can understand with economics that make sense. Some of these AI developments will create enormous value, but a lot of capital will also be destroyed chasing the next big thing. The winners will be businesses that use AI to strengthen their existing competitive advantages, not those built entirely on hype.

The world news reminds us that uncertainty is permanent. We've always had geopolitical challenges, economic cycles, and technological disruption. What works is buying pieces of wonderful businesses at sensible prices and holding them for the long term. That strategy has worked for over a century and will continue working for the next century."""
        }

def main():
    """Test the commentary generator"""
    # Load sample news data
    try:
        with open('news_digest_raw.json', 'r') as f:
            news_digest = json.load(f)
    except FileNotFoundError:
        print("Error: news_digest_raw.json not found. Run news_fetcher.py first.")
        sys.exit(1)
    
    generator = CommentaryGenerator()
    
    # For testing, use mock commentary
    commentaries = generator.create_mock_commentary(news_digest)
    
    # Display
    print(generator.format_commentary_display(commentaries))
    
    # Save to JSON
    with open('commentary_output.json', 'w') as f:
        json.dump(commentaries, f, indent=2)
    print("\nCommentary saved to: commentary_output.json")

if __name__ == "__main__":
    main()
