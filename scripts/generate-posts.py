#!/usr/bin/env python3
"""
Generate social media posts using Ollama/Qwen (local).
Reads brand voice, topic, and creates platform-specific content.
"""

import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

def load_brand_voice(config_path: str) -> str:
    """Load brand voice guidelines."""
    with open(config_path, 'r') as f:
        return f.read()

def load_topic(topic_slug: str, topics_dir: str) -> dict:
    """Load topic details from JSON index."""
    topics_file = Path(topics_dir) / "topics.json"

    if not topics_file.exists():
        print("⚠️  No topics.json found. Run extract-topics.py first.")
        return None

    with open(topics_file, 'r') as f:
        topics = json.load(f)

    matching = [t for t in topics if t['slug'] == topic_slug]
    return matching[0] if matching else None

def generate_posts(platform: str, topic: dict, brand_voice: str, count: int = 1) -> list[str]:
    """Generate posts using Ollama/Qwen (local)."""

    platform_instructions = {
        'linkedin': '''
Create LinkedIn posts that:
- Are 500-1000 characters
- Include thought leadership or personal insight
- End with an engaging question
- Sound professional but approachable
- Reference the topic's business/personal impact
        ''',
        'instagram': '''
Create Instagram caption/hook that:
- Is 60-150 characters max
- Starts with a punchy hook
- Uses 1-2 emojis strategically (no emoji spam)
- Ends with a CTA like "Save this" or "Tag someone"
- Is casual and conversational
        ''',
        'tiktok': '''
Create a TikTok script that:
- Is 60-200 characters
- Opens with a shocking or relatable statement
- Explains one key insight
- Ends with "...wait for it" or similar hook
- Is energetic and conversational
- Suggests visual elements in brackets [like this]
        '''
    }

    prompt = f"""You are a financial advisor creating educational social media content.

## Brand Voice Guidelines
{brand_voice}

## Platform Requirements
{platform_instructions.get(platform, '')}

## Topic
- Name: {topic['name']}
- Summary: {topic['summary']}
- Key features: {', '.join(topic['key_features'])}

Generate {count} unique posts for {platform}.
Vary the angle (benefit, misconception, scenario, or statistic).
Output as JSON array with field "post" for each item.
No additional text, just valid JSON.

Example output format:
[
  {{"post": "Your post content here", "angle": "benefit"}},
  {{"post": "Another unique angle", "angle": "misconception"}}
]
"""

    print(f"🤖 Generating {count} {platform} posts for '{topic['name']}' (Qwen/Ollama)...")
    print("   ⏳ This may take 2-5 minutes on first run (model warming up)...")

    # Call Ollama API directly
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:latest",
        "prompt": prompt,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        # Increase timeout for Qwen inference (can take 5+ minutes on first run)
        with urllib.request.urlopen(req, timeout=600) as response:
            result = json.loads(response.read().decode('utf-8'))
            response_text = result.get('response', '')
    except urllib.error.URLError as e:
        print(f"❌ Error: Cannot connect to Ollama at {url}")
        print("   Make sure Ollama is running: ollama serve")
        print(f"   Error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error generating posts: {e}")
        return []

    try:
        posts = json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback: extract JSON from response
        import re
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            posts = json.loads(json_match.group())
        else:
            posts = [{"post": response_text, "angle": "general"}]

    return posts

def save_posts(posts: list[dict], platform: str, topic_slug: str, posts_dir: str):
    """Save generated posts to markdown files."""

    timestamp = datetime.now().strftime("%Y-%m-%d")
    posts_path = Path(posts_dir) / platform

    posts_path.mkdir(parents=True, exist_ok=True)

    for i, post_data in enumerate(posts):
        post = post_data.get('post', post_data) if isinstance(post_data, dict) else post_data
        angle = post_data.get('angle', 'general') if isinstance(post_data, dict) else 'general'

        # Filename with timestamp and counter
        filename = posts_path / f"{timestamp}_{topic_slug}_{i+1}.md"

        with open(filename, 'w') as f:
            f.write(f"# {timestamp} - {topic_slug}\n\n")
            f.write(f"**Platform:** {platform}\n\n")
            f.write(f"**Angle:** {angle}\n\n")
            f.write(f"## Post Content\n\n")
            f.write(post.strip())
            f.write(f"\n\n---\n")
            f.write(f"*Generated: {datetime.now().isoformat()}*\n")

        print(f"  ✅ {filename.name}")

    return posts_path

def main():
    parser = argparse.ArgumentParser(description="Generate social media posts")
    parser.add_argument('--platform', choices=['linkedin', 'instagram', 'tiktok'], required=True)
    parser.add_argument('--topic', required=True, help="Topic slug (e.g., 'life-cover')")
    parser.add_argument('--count', type=int, default=1, help="Number of posts to generate")
    parser.add_argument('--config-dir', default='/Users/kennedysigauke/Work/Personal/financial-advisor/config')
    parser.add_argument('--topics-dir', default='/Users/kennedysigauke/Work/Personal/financial-advisor/docs/topics')
    parser.add_argument('--posts-dir', default='/Users/kennedysigauke/Work/Personal/financial-advisor/docs/posts')

    args = parser.parse_args()

    # Load brand voice and topic
    brand_voice_file = Path(args.config_dir) / "brand-voice.md"
    if not brand_voice_file.exists():
        print(f"❌ Brand voice not found: {brand_voice_file}")
        return

    brand_voice = load_brand_voice(brand_voice_file)

    topic = load_topic(args.topic, args.topics_dir)
    if not topic:
        print(f"❌ Topic not found: {args.topic}")
        print("Run extract-topics.py first to create topics.")
        return

    # Generate and save posts
    posts = generate_posts(args.platform, topic, brand_voice, args.count)
    save_posts(posts, args.platform, args.topic, args.posts_dir)

    print(f"\n✅ Posts saved to: {args.posts_dir}/{args.platform}/")

if __name__ == "__main__":
    main()
