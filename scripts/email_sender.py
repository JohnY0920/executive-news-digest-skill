#!/usr/bin/env python3
"""
Email Sender for Executive News Digest
Sends formatted digest via Gmail using GOG CLI
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List

class EmailSender:
    def __init__(self, recipient="johnyin@aisemble.ca"):
        self.recipient = recipient
        self.sender_account = None  # Will use GOG_ACCOUNT env var
    
    def format_html_email(self, english_content: Dict, chinese_content: Dict) -> str:
        """Format the digest as HTML email"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 28px;
        }}
        .date {{
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 5px;
        }}
        .section {{
            margin-bottom: 35px;
        }}
        .section-title {{
            color: #2c3e50;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }}
        .headlines {{
            margin-left: 0;
            padding-left: 20px;
        }}
        .headlines li {{
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        .headlines a {{
            color: #3498db;
            text-decoration: none;
        }}
        .headlines a:hover {{
            text-decoration: underline;
        }}
        .source {{
            color: #95a5a6;
            font-size: 12px;
        }}
        .commentary {{
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .commentary-header {{
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }}
        .commentary-text {{
            color: #34495e;
            line-height: 1.7;
        }}
        .divider {{
            border-top: 1px solid #ecf0f1;
            margin: 40px 0;
        }}
        .language-section {{
            margin-top: 50px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 Executive News Digest</h1>
            <div class="date">{datetime.now().strftime('%A, %B %d, %Y')}</div>
        </div>
        
        <!-- ENGLISH SECTION -->
        {self._format_english_section(english_content)}
        
        <!-- CHINESE SECTION -->
        <div class="language-section">
            <div class="divider"></div>
            <h2 style="color: #2c3e50; text-align: center;">中文版本</h2>
            <div class="divider"></div>
            {self._format_chinese_section(chinese_content)}
        </div>
        
        <div class="footer">
            <p>Executive News Digest • Daily at 7:00 AM EST</p>
            <p>Powered by OpenClaw Skills</p>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def _format_english_section(self, content: Dict) -> str:
        """Format English news and commentary"""
        news = content.get("news", {})
        commentary = content.get("commentary", {})
        
        html_parts = []
        
        # News sections
        category_info = {
            "economics": ("📊 Economics", "economics"),
            "world_news": ("🌍 World News", "world_news"),
            "business": ("💼 Business", "business"),
            "ai_technology": ("🤖 AI Technology", "ai_technology")
        }
        
        for cat_key, (cat_name, cat_data_key) in category_info.items():
            articles = news.get(cat_data_key, [])
            if articles:
                html_parts.append(f'<div class="section">')
                html_parts.append(f'<div class="section-title">{cat_name}</div>')
                html_parts.append('<ul class="headlines">')
                for article in articles:
                    title = article.get("title", "")
                    url = article.get("url", "#")
                    source = article.get("source", "")
                    html_parts.append(f'<li>')
                    html_parts.append(f'<a href="{url}" target="_blank">{title}</a>')
                    if source:
                        html_parts.append(f'<br><span class="source">Source: {source}</span>')
                    html_parts.append(f'</li>')
                html_parts.append('</ul>')
                html_parts.append('</div>')
        
        # Commentary sections
        html_parts.append('<div class="divider"></div>')
        html_parts.append('<h2 style="color: #2c3e50; text-align: center;">🎭 Executive Perspectives</h2>')
        html_parts.append('<div class="divider"></div>')
        
        exec_info = {
            "ray_dalio": ("📈 Ray Dalio's Analysis", "ray_dalio"),
            "elon_musk": ("🚀 Elon Musk's Take", "elon_musk"),
            "warren_buffett": ("💰 Warren Buffett's View", "warren_buffett")
        }
        
        for exec_key, (exec_title, exec_data_key) in exec_info.items():
            text = commentary.get(exec_data_key, "")
            if text:
                html_parts.append('<div class="commentary">')
                html_parts.append(f'<div class="commentary-header">{exec_title}</div>')
                # Convert paragraphs to HTML
                paragraphs = text.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        html_parts.append(f'<p class="commentary-text">{para}</p>')
                html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def _format_chinese_section(self, content: Dict) -> str:
        """Format Chinese news and commentary"""
        news = content.get("news", {})
        commentary = content.get("commentary", {})
        
        html_parts = []
        
        # News sections
        category_info = {
            "economics": ("📊 经济", "economics"),
            "world_news": ("🌍 世界新闻", "world_news"),
            "business": ("💼 商业", "business"),
            "ai_technology": ("🤖 人工智能技术", "ai_technology")
        }
        
        for cat_key, (cat_name, cat_data_key) in category_info.items():
            articles = news.get(cat_data_key, [])
            if articles:
                html_parts.append(f'<div class="section">')
                html_parts.append(f'<div class="section-title">{cat_name}</div>')
                html_parts.append('<ul class="headlines">')
                for article in articles:
                    title = article.get("title", "")
                    url = article.get("url", "#")
                    source = article.get("source", "")
                    html_parts.append(f'<li>')
                    html_parts.append(f'<a href="{url}" target="_blank">{title}</a>')
                    if source:
                        html_parts.append(f'<br><span class="source">来源: {source}</span>')
                    html_parts.append(f'</li>')
                html_parts.append('</ul>')
                html_parts.append('</div>')
        
        # Commentary sections
        html_parts.append('<div class="divider"></div>')
        html_parts.append('<h2 style="color: #2c3e50; text-align: center;">🎭 高管观点</h2>')
        html_parts.append('<div class="divider"></div>')
        
        exec_info = {
            "ray_dalio": ("📈 瑞·达利奥的分析", "ray_dalio"),
            "elon_musk": ("🚀 埃隆·马斯克的看法", "elon_musk"),
            "warren_buffett": ("💰 沃伦·巴菲特的观点", "warren_buffett")
        }
        
        for exec_key, (exec_title, exec_data_key) in exec_info.items():
            text = commentary.get(exec_data_key, "")
            if text:
                html_parts.append('<div class="commentary">')
                html_parts.append(f'<div class="commentary-header">{exec_title}</div>')
                # Convert paragraphs to HTML
                paragraphs = text.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        html_parts.append(f'<p class="commentary-text">{para}</p>')
                html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def send_email(self, english_content: Dict, chinese_content: Dict) -> bool:
        """Send the digest via email using GOG CLI"""
        try:
            # Format HTML
            html_body = self.format_html_email(english_content, chinese_content)
            
            # Save HTML to temp file
            temp_html_file = "/tmp/news_digest.html"
            with open(temp_html_file, 'w', encoding='utf-8') as f:
                f.write(html_body)
            
            # Prepare email subject
            subject = f"📰 Executive News Digest - {datetime.now().strftime('%b %d, %Y')}"
            
            # Send via GOG CLI
            # Note: This assumes GOG is configured and GOG_ACCOUNT is set
            cmd = [
                "gog", "gmail", "send",
                "--to", self.recipient,
                "--subject", subject,
                "--html-file", temp_html_file
            ]
            
            print(f"Sending email to {self.recipient}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Email sent successfully!")
                return True
            else:
                print(f"❌ Error sending email: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def save_html_preview(self, english_content: Dict, chinese_content: Dict, filename="digest_preview.html"):
        """Save HTML email as file for preview"""
        html = self.format_html_email(english_content, chinese_content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Preview saved to: {filename}")

def main():
    """Test email sender"""
    # Load content
    try:
        with open('news_digest_raw.json', 'r') as f:
            news_digest = json.load(f)
        with open('commentary_output.json', 'r') as f:
            commentaries = json.load(f)
        with open('translated_digest.json', 'r', encoding='utf-8') as f:
            translated = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: {e}. Run previous scripts first.")
        sys.exit(1)
    
    english_content = {
        "news": news_digest,
        "commentary": commentaries
    }
    
    chinese_content = translated
    
    sender = EmailSender()
    
    # Save HTML preview
    sender.save_html_preview(english_content, chinese_content)
    
    # Optionally send email (uncomment to actually send)
    # sender.send_email(english_content, chinese_content)
    print("\nTo send email, uncomment the send_email() line in main()")

if __name__ == "__main__":
    main()
