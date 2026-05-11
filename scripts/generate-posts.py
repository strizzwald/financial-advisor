#!/usr/bin/env python3
"""
Generate social media posts using the Claude API (claude-sonnet-4-6).
Reads brand voice, product definitions, scenarios, and topic to create platform-specific content.
Requires ANTHROPIC_API_KEY environment variable.
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime

def load_brand_voice(config_path: str) -> str:
    with open(config_path, 'r') as f:
        return f.read()

def load_scenarios(config_path: str) -> str:
    scenarios_file = Path(config_path).parent / "scenarios.md"
    if not scenarios_file.exists():
        return ""
    with open(scenarios_file, 'r') as f:
        return f.read()

def load_product_definition(config_path: str, topic_slug: str) -> str:
    defs_file = Path(config_path).parent / "product-definitions.md"
    if not defs_file.exists():
        return ""
    content = defs_file.read_text()
    # Extract only the section for this topic slug
    pattern = f"## {topic_slug}\n"
    start = content.find(pattern)
    if start == -1:
        return ""
    end = content.find("\n---", start + len(pattern))
    section = content[start:end].strip() if end != -1 else content[start:].strip()
    return section

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

def generate_posts(platform: str, topic: dict, brand_voice: str, count: int = 1, scenarios: str = "", product_definition: str = "") -> list[str]:
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
Produce an infographic story in this exact JSON structure (no extra fields):

{
  "angle": "<angle name>",
  "narration": "<full story narration — 3-5 sentences that read as a cohesive arc: introduce the person, reveal the gap, land the insight, end with a soft CTA>",
  "frames": [
    {
      "number": 1,
      "caption": "<short bold text overlay for this frame, max 12 words>",
      "image_prompt": "<detailed prompt for an AI image generator: describe the scene, mood, style, and any text to show on screen. South African context. Photorealistic infographic style. No real people — use illustrated or silhouette figures.>"
    },
    {
      "number": 2,
      "caption": "...",
      "image_prompt": "..."
    },
    {
      "number": 3,
      "caption": "...",
      "image_prompt": "..."
    },
    {
      "number": 4,
      "caption": "<ends with a soft CTA, e.g. 'Book a free call — link in bio'>",
      "image_prompt": "..."
    }
  ]
}

Story arc across 4 frames:
- Frame 1: Introduce the person and their situation (age, income, lifestyle)
- Frame 2: Show the gap or the risk — what they're missing or what happened
- Frame 3: Reveal the insight — what a simple solution looks like in plain English
- Frame 4: Resolution or CTA — what life looks like with the right cover in place

Style rules:
- Narration and captions must be plain English — no jargon, no product mechanics
- Use specific rand amounts and ages from the scenario
- No hashtags, no emojis
- Image prompts: clean infographic aesthetic, warm tones, South African setting (suburb, township, gym, office)
        '''
    }

    angles = [
        "client-story: Open with an anonymised person (age, situation, specific rand amounts). Reveal what they were missing. Land one clear insight. Do NOT name the product until the very end, if at all.",
        "before-after: Contrast a financial situation before taking action vs after. Use specific numbers.",
        "savings-tip: A standalone money habit or observation — no product pitch required.",
        "financial-health-check: A short list (3-5 items) of warning signs people ignore.",
        "misconception: Bust one common myth about money, cover, or financial planning.",
        "real-cost: Show what a gap in cover actually costs in rands — make the number concrete.",
        "life-stage: Tie the insight to a specific life event (new baby, new job, marriage, retrenchment).",
    ]

    scenarios_section = f"""
## Client Scenarios (use these as inspiration — adapt freely, don't copy verbatim)
{scenarios}
""" if scenarios else ""

    product_section = f"""
## Product Definition (THIS IS THE ONLY PRODUCT YOU ARE WRITING ABOUT)
{product_definition}

IMPORTANT RULES:
- Only write about what this product covers (see "Trigger" and "Benefit" above)
- Never reference what other products cover
- Use the "Plain-English label" when you need to name the product — never use technical policy terms
- Do not invent or guess at product mechanics beyond what is stated above
""" if product_definition else f"""
## Topic
- Name: {topic['name']}
- Summary: {topic['summary']}
"""

    prompt = f"""You are a financial advisor creating educational social media content for South African audiences.
Your goal is to create content that feels relatable and human — lead with a person's real situation, not a product feature.

## Brand Voice Guidelines
{brand_voice}

## Platform Requirements
{platform_instructions.get(platform, '')}
{product_section}{scenarios_section}
## Available Angles
{chr(10).join(f"- {a}" for a in angles)}

Generate {count} unique posts for {platform}.
Pick a different angle for each post. Prioritise client-story, before-after, and real-cost angles — these perform best on social media.
Use specific rand amounts and ages where relevant. South African context throughout.
Never lead with the product name. Lead with a person or a situation.
When mentioning the solution: use only the plain-English label from the product definition — never explain mechanics or policy terms. The goal is to spark curiosity and drive them to book a call.

Output a JSON array of {count} post objects. Each object must match exactly the structure defined in the platform requirements above.
No additional text outside the JSON array.
"""

    print(f"🤖 Generating {count} {platform} posts for '{topic['name']}' (claude-sonnet-4-6)...")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable is not set.")
        return []

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = message.content[0].text
    except Exception as e:
        print(f"❌ Error calling Claude API: {e}")
        return []

    try:
        posts = json.loads(response_text)
    except json.JSONDecodeError:
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
        if not isinstance(post_data, dict):
            post_data = {"post": post_data, "angle": "general"}

        angle = post_data.get('angle', 'general')
        filename = posts_path / f"{timestamp}_{topic_slug}_{i+1}.md"

        with open(filename, 'w') as f:
            f.write(f"# {timestamp} - {topic_slug}\n\n")
            f.write(f"**Platform:** {platform}  \n")
            f.write(f"**Angle:** {angle}  \n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write("---\n\n")

            if platform == 'tiktok' and 'narration' in post_data:
                f.write("## Narration\n\n")
                f.write(post_data['narration'].strip())
                f.write("\n\n")

                frames = post_data.get('frames', [])
                if frames:
                    f.write("## Visualization Script\n\n")
                    for frame in frames:
                        num = frame.get('number', '')
                        caption = frame.get('caption', '')
                        image_prompt = frame.get('image_prompt', '')
                        f.write(f"### Frame {num}\n\n")
                        f.write(f"**Caption:** {caption}\n\n")
                        f.write(f"**Image prompt:**\n> {image_prompt}\n\n")
            else:
                f.write("## Post Content\n\n")
                f.write(str(post_data.get('post', '')).strip())
                f.write("\n\n")

        print(f"  ✅ {filename.name}")

    return posts_path

def load_env(project_root: Path):
    """Load .env from project root or any ancestor directory."""
    candidates = [project_root] + list(project_root.parents)
    for directory in candidates:
        env_file = directory / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    k = key.strip()
                    if not os.environ.get(k):
                        os.environ[k] = value.strip()
            break

def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    parser = argparse.ArgumentParser(description="Generate social media posts")
    parser.add_argument('--platform', choices=['linkedin', 'instagram', 'tiktok'], required=True)
    parser.add_argument('--topic', required=True, help="Topic slug (e.g., 'life-cover')")
    parser.add_argument('--count', type=int, default=1, help="Number of posts to generate")
    parser.add_argument('--config-dir', default=str(project_root / "config"))
    parser.add_argument('--topics-dir', default=str(project_root / "docs" / "topics"))
    parser.add_argument('--posts-dir', default=str(project_root / "docs" / "posts"))

    args = parser.parse_args()

    load_env(project_root)

    # Load brand voice and topic
    brand_voice_file = Path(args.config_dir) / "brand-voice.md"
    if not brand_voice_file.exists():
        print(f"❌ Brand voice not found: {brand_voice_file}")
        return

    brand_voice = load_brand_voice(brand_voice_file)
    scenarios = load_scenarios(brand_voice_file)
    product_definition = load_product_definition(brand_voice_file, args.topic)

    topic = load_topic(args.topic, args.topics_dir)
    if not topic:
        print(f"❌ Topic not found: {args.topic}")
        print("Run extract-topics.py first to create topics.")
        return

    if product_definition:
        print(f"   ✅ Product definition loaded for '{args.topic}'")
    else:
        print(f"   ⚠️  No product definition found for '{args.topic}' — model may hallucinate")

    # Generate and save posts
    posts = generate_posts(args.platform, topic, brand_voice, args.count, scenarios, product_definition)
    save_posts(posts, args.platform, args.topic, args.posts_dir)

    print(f"\n✅ Posts saved to: {args.posts_dir}/{args.platform}/")

if __name__ == "__main__":
    main()
