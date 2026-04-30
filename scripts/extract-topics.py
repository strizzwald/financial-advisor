#!/usr/bin/env python3
"""
Extract key topics and concepts from technical product guide.
Parses text to identify products, features, and use cases.
"""

import re
import json
from pathlib import Path
from datetime import datetime

def extract_topics(markdown_file: str) -> list[dict]:
    """Extract topics from technical guide (handles plain text from PDF)."""

    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    topics = []

    # Product names and key sections we're looking for
    product_keywords = [
        'life cover', 'adapted life cover', 'renewable cover', 'funeral benefit',
        'educator', 'educator xtra', 'capital disability', 'capital disability plus',
        'impairment', 'impairment plus', 'income protector', 'challenge income',
        'living lifestyle', 'living lifestyle plus', 'female living lifestyle',
        'child living lifestyle', 'future protector', 'financial protector',
        'medical premium protector', 'premium protector', 'loan protection',
        'life annuity', 'wellness bonus', 'addlib'
    ]

    lines = content.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check if this line contains a product keyword
        line_lower = stripped.lower()

        for keyword in product_keywords:
            if keyword in line_lower and len(stripped) < 100 and len(stripped) > 3:
                # Make sure it's mostly uppercase (actual header, not body text)
                if stripped.isupper() or (stripped[0].isupper() and all(w[0].isupper() for w in stripped.split() if w)):
                    title = stripped

                    # Get context (next few lines)
                    body_lines = []
                    for j in range(i+1, min(i+8, len(lines))):
                        next_line = lines[j].strip()
                        if next_line and len(next_line) < 150 and not next_line.isupper():
                            body_lines.append(next_line)
                            if len(body_lines) >= 3:
                                break

                    body = '\n'.join(body_lines)

                    # Extract summary
                    summary = body.split('\n')[0] if body else f"Learn about {title.lower()}"
                    if len(summary) > 150:
                        summary = summary[:150] + "..."

                    # Build slug safely
                    slug = keyword.replace(' ', '-').lower()

                    topic = {
                        'name': title,
                        'slug': slug,
                        'summary': summary,
                        'key_features': [],
                        'full_content': body[:300],
                        'created_at': datetime.now().isoformat()
                    }

                    topics.append(topic)
                    break  # Don't match the same line twice

    # Remove duplicates
    seen_slugs = set()
    unique_topics = []
    for t in topics:
        if t['slug'] not in seen_slugs:
            seen_slugs.add(t['slug'])
            unique_topics.append(t)

    return unique_topics

def save_topics(topics: list[dict], output_dir: str):
    """Save extracted topics as markdown files and JSON index."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save individual topic files
    for topic in topics:
        filename = output_path / f"{topic['slug']}.md"
        with open(filename, 'w') as f:
            f.write(f"# {topic['name']}\n\n")
            f.write(f"{topic['summary']}\n\n")

            if topic['key_features']:
                f.write("## Key Features\n\n")
                for feature in topic['key_features']:
                    f.write(f"- {feature}\n")

        print(f"✅ Created: {filename}")

    # Save JSON index
    index_file = output_path / "topics.json"
    with open(index_file, 'w') as f:
        json.dump(topics, f, indent=2)

    print(f"✅ Topics index: {index_file}")

def main():
    # Get the project root (parent of scripts directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    technical_guide = project_root / "source" / "LibertyLifestyleProtectorTechnicalGuide.md"
    output_dir = project_root / "docs" / "topics"

    if not technical_guide.exists():
        print(f"❌ Technical guide not found: {technical_guide}")
        return

    print(f"📖 Extracting topics from: {technical_guide}")
    topics = extract_topics(str(technical_guide))
    print(f"📊 Found {len(topics)} topics\n")

    save_topics(topics, str(output_dir))
    print(f"\n✅ Topics extracted to: {output_dir}")

if __name__ == "__main__":
    main()
