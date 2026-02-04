#!/usr/bin/env python3
"""
News Fetcher for Executive News Digest
Fetches headlines from multiple sources across 4 categories
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List

class NewsFetcher:
    def __init__(self):
        self.categories = {
            "economics": ["economics", "economy", "GDP", "inflation", "federal reserve", "monetary policy"],
            "world_news": ["world news", "international", "geopolitics", "global affairs"],
            "business": ["business news", "markets", "stocks", "corporate", "earnings"],
            "ai_technology": ["artificial intelligence", "AI", "machine learning", "tech innovation"]
        }
        self.headlines_per_category = 5
    
    def fetch_web_search_news(self, query: str, count: int = 5) -> List[Dict]:
        """
        Fetch news using web search (Brave API if available)
        Falls back to mock data if API not available
        """
        # Check for Brave API key
        import os
        brave_key = os.environ.get('BRAVE_API_KEY')
        
        if not brave_key:
            print(f"Warning: No BRAVE_API_KEY found, using mock data for: {query}")
            return self._get_mock_news(query, count)
        
        try:
            # Use Brave Search API
            url = "https://api.search.brave.com/res/v1/news/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": brave_key
            }
            params = {
                "q": query,
                "count": count,
                "freshness": "pd"  # Past day
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                return [
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "source": item.get("meta_url", {}).get("netloc", ""),
                        "published": item.get("age", "")
                    }
                    for item in results[:count]
                ]
            else:
                print(f"Brave API error {response.status_code}, using mock data")
                return self._get_mock_news(query, count)
                
        except Exception as e:
            print(f"Error fetching from Brave API: {e}, using mock data")
            return self._get_mock_news(query, count)
    
    def _get_mock_news(self, query: str, count: int) -> List[Dict]:
        """Generate mock news data for testing"""
        category_map = {
            "economics": [
                "Fed Signals Potential Rate Cuts in Q2 2026",
                "Global Inflation Rates Show Signs of Stabilization",
                "US GDP Growth Exceeds Expectations at 3.2%",
                "European Central Bank Maintains Steady Policy",
                "China's Economic Data Points to Gradual Recovery"
            ],
            "world": [
                "G7 Summit Addresses Climate and Security Concerns",
                "Middle East Peace Talks Show Progress",
                "Asian Nations Strengthen Trade Partnerships",
                "UN Report Highlights Global Development Goals",
                "International Response to Humanitarian Crisis Gains Momentum"
            ],
            "business": [
                "Tech Giants Report Strong Q4 Earnings",
                "Major Merger Announced in Automotive Sector",
                "Retail Sales Data Exceeds Analyst Projections",
                "Energy Companies Pivot Toward Renewable Investments",
                "Startup Unicorns Continue to Emerge in AI Space"
            ],
            "ai": [
                "OpenAI Announces Major Model Architecture Breakthrough",
                "AI Regulation Framework Proposed by EU Parliament",
                "Healthcare AI Shows 95% Accuracy in Early Detection",
                "Major Tech Companies Form AI Safety Coalition",
                "Quantum Computing Advances Enable New AI Capabilities"
            ]
        }
        
        # Determine which mock category to use
        for key in category_map:
            if key in query.lower():
                headlines = category_map[key]
                return [
                    {
                        "title": headline,
                        "url": f"https://example.com/news/{i}",
                        "source": "Mock News Source",
                        "published": "1 hour ago"
                    }
                    for i, headline in enumerate(headlines[:count])
                ]
        
        # Default mock data
        return [
            {
                "title": f"Mock headline for: {query} ({i+1})",
                "url": f"https://example.com/news/{i}",
                "source": "Mock Source",
                "published": "1 hour ago"
            }
            for i in range(count)
        ]
    
    def fetch_all_news(self) -> Dict[str, List[Dict]]:
        """Fetch news for all categories"""
        news_digest = {}
        
        for category, queries in self.categories.items():
            print(f"Fetching {category} news...")
            # Use primary query for each category
            primary_query = queries[0]
            news_digest[category] = self.fetch_web_search_news(primary_query, self.headlines_per_category)
        
        return news_digest
    
    def format_for_display(self, news_digest: Dict[str, List[Dict]]) -> str:
        """Format news digest for display"""
        output = []
        output.append("=" * 60)
        output.append(f"NEWS DIGEST - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        output.append("=" * 60)
        output.append("")
        
        category_names = {
            "economics": "📊 ECONOMICS",
            "world_news": "🌍 WORLD NEWS",
            "business": "💼 BUSINESS",
            "ai_technology": "🤖 AI TECHNOLOGY"
        }
        
        for category, articles in news_digest.items():
            output.append(f"\n{category_names.get(category, category.upper())}")
            output.append("-" * 60)
            for i, article in enumerate(articles, 1):
                output.append(f"{i}. {article['title']}")
                output.append(f"   Source: {article['source']} | {article['published']}")
                output.append(f"   URL: {article['url']}")
                output.append("")
        
        return "\n".join(output)

def main():
    """Main function for testing"""
    fetcher = NewsFetcher()
    news = fetcher.fetch_all_news()
    print(fetcher.format_for_display(news))
    
    # Save to JSON
    output_file = "news_digest_raw.json"
    with open(output_file, 'w') as f:
        json.dump(news, f, indent=2)
    print(f"\nRaw data saved to: {output_file}")

if __name__ == "__main__":
    main()
