#!/usr/bin/env python3
"""
Auto-generate index.md files for mkdocs navigation.
Scans posts directory and creates searchable indexes.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def build_infographics_index(infographics_dir: str):
    """Generate index for infographics."""

    infographics_path = Path(infographics_dir)

    if not infographics_path.exists():
        return

    # Find all SVG files
    svgs = sorted(infographics_path.glob('*.svg'), reverse=True)

    index_content = """# Infographics

Visual diagrams and educational infographics for social media.

## Available Infographics

| Date | Topic | File |
|------|-------|------|
"""

    for svg_file in svgs:
        # Extract date and topic from filename
        name_parts = svg_file.stem.split('_', 1)
        date = name_parts[0] if name_parts else 'Unknown'
        topic = name_parts[1] if len(name_parts) > 1 else 'General'

        index_content += f"| {date} | {topic} | [{svg_file.name}]({svg_file.name}) |\n"

    index_content += f"""

## Statistics

- Total infographics: {len(svgs)}
- Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

Each infographic is a self-contained SVG visual that complements your social media posts.
Perfect for Instagram stories, Pinterest, and educational content.
"""

    index_file = infographics_path / "index.md"
    with open(index_file, 'w') as f:
        f.write(index_content)

    print(f"✅ {index_file}")


def build_post_indexes(posts_dir: str):
    """Generate index files for each platform and main posts directory."""

    posts_path = Path(posts_dir)

    # Scan all posts
    platforms = {}
    all_posts = []

    for platform_dir in posts_path.iterdir():
        if not platform_dir.is_dir():
            continue

        platform = platform_dir.name
        posts = []

        for post_file in sorted(platform_dir.glob('*.md'), reverse=True):
            # Skip index files
            if post_file.name == 'index.md':
                continue

            with open(post_file, 'r') as f:
                content = f.read()

            # Extract metadata
            lines = content.split('\n')
            title = lines[0].replace('# ', '').strip() if lines else 'Untitled'
            angle = ''

            for line in lines:
                if line.startswith('**Angle:**'):
                    angle = line.replace('**Angle:**', '').strip()
                    break

            posts.append({
                'file': post_file.name,
                'title': title,
                'angle': angle,
                'path': f"posts/{platform}/{post_file.name}"
            })

        platforms[platform] = posts
        all_posts.extend([(platform, p) for p in posts])

    # Generate platform-specific indexes
    for platform, posts in platforms.items():
        index_content = f"""# {platform.capitalize()} Posts

Generated social media content for {platform}.

## Recent Posts

| Date | Topic | Angle |
|------|-------|-------|
"""

        for post in posts[:50]:  # Latest 50
            date = post['title'].split(' - ')[0] if ' - ' in post['title'] else 'Unknown'
            topic = post['title'].split(' - ')[1] if ' - ' in post['title'] else 'General'
            angle = post['angle'] or 'General'
            # Use relative path from current directory
            relative_path = post['file']

            index_content += f"| {date} | [{topic}]({relative_path}) | {angle} |\n"

        index_content += f"\n## Statistics\n\n"
        index_content += f"- Total posts: {len(posts)}\n"
        index_content += f"- Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

        # Write platform index
        index_file = Path(posts_dir) / platform / "index.md"
        index_file.parent.mkdir(parents=True, exist_ok=True)

        with open(index_file, 'w') as f:
            f.write(index_content)

        print(f"✅ {index_file}")

    # Generate main posts index
    main_index = f"""# All Generated Posts

Overview of all social media content across platforms.

## By Platform

"""

    for platform in ['linkedin', 'instagram', 'tiktok']:
        if platform in platforms:
            count = len(platforms[platform])
            main_index += f"- **[{platform.capitalize()}]({platform}/index.md)** — {count} posts\n"

    main_index += f"""

## Quick Stats

| Platform | Post Count |
|----------|-----------|
"""

    for platform in ['linkedin', 'instagram', 'tiktok']:
        if platform in platforms:
            count = len(platforms[platform])
            main_index += f"| {platform.capitalize()} | {count} |\n"

    main_index += f"""

---

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

All posts are stored with timestamps for easy tracking of content evolution.
"""

    main_index_file = Path(posts_dir) / "index.md"
    with open(main_index_file, 'w') as f:
        f.write(main_index)

    print(f"✅ {main_index_file}")

def build_topics_index(topics_dir: str):
    """Generate index for extracted topics."""

    topics_file = Path(topics_dir) / "topics.json"

    if not topics_file.exists():
        print("⚠️  No topics.json found. Run extract-topics.py first.")
        return

    with open(topics_file, 'r') as f:
        topics = json.load(f)

    index_content = f"""# Extracted Topics

Products and concepts extracted from the technical guide.

## Available Topics

| Topic | Slug | Features |
|-------|------|----------|
"""

    for topic in sorted(topics, key=lambda t: t['name']):
        slug = topic.get('slug', topic['name'].lower().replace(' ', '-'))
        feature_count = len(topic.get('key_features', []))

        index_content += f"| [{topic['name']}]({slug}.md) | `{slug}` | {feature_count} features |\n"

    index_content += f"""

## Statistics

- Total topics: {len(topics)}
- Last extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

Use these topics with the post generator:
```bash
python generate-posts.py --platform linkedin --topic {topics[0]['slug']} --count 3
```
"""

    index_file = Path(topics_dir) / "index.md"
    with open(index_file, 'w') as f:
        f.write(index_content)

    print(f"✅ {index_file}")

def main():
    posts_dir = "/Users/kennedysigauke/Work/Personal/financial-advisor/docs/posts"
    topics_dir = "/Users/kennedysigauke/Work/Personal/financial-advisor/docs/topics"
    infographics_dir = f"{posts_dir}/infographics"

    print("🔨 Building indexes...\n")

    build_post_indexes(posts_dir)
    print()
    build_infographics_index(infographics_dir)
    print()
    build_topics_index(topics_dir)

    print("\n✅ Indexes built successfully")

if __name__ == "__main__":
    main()
