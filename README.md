# Financial Advisor Social Media Content Generator

An automated system for generating platform-specific social media content from product knowledge. Stores all content as markdown with timestamps for easy tracking and evolution.

## Overview

This system helps financial advisors scale content creation by:
- **Extracting topics** from product technical guides
- **Generating posts** for LinkedIn, Instagram, and TikTok
- **Maintaining a living archive** of all content (with timestamps)
- **Ensuring brand consistency** via a centralized, tweakable voice guide

All content is stored as markdown and navigable via MkDocs.

## Setup

### Prerequisites
- Python 3.10+
- Anthropic API key (for Claude)
- MkDocs (optional, for local preview)

### Installation

```bash
# Set Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Install MkDocs (for docs preview)
pip install mkdocs mkdocs-material

# Test it works
cd /Users/kennedysigauke/Work/Personal/financial-advisor
```

## Quick Start

### 1. Extract Topics from Technical Guide
```bash
cd scripts
python extract-topics.py
```

This parses the Liberty Lifestyle Protector Technical Guide and creates:
- Individual topic markdown files (`docs/topics/*.md`)
- JSON index (`docs/topics/topics.json`) with all topics

### 2. Generate Posts

Generate LinkedIn posts about "Life Cover":
```bash
python generate-posts.py --platform linkedin --topic life-cover --count 3
```

Generate Instagram shorts about "Income Protection":
```bash
python generate-posts.py --platform instagram --topic income-protection --count 5
```

All posts are saved with timestamps: `docs/posts/{platform}/{YYYY-MM-DD}_{topic}_{n}.md`

### 3. View Content Locally

```bash
mkdocs serve
# Visit http://localhost:8000
```

### 4. Update Brand Voice

Edit `config/brand-voice.md` to adjust:
- Tone and voice
- Platform-specific guidelines
- Topics to prioritize/avoid
- Language rules

Regenerate posts to apply changes:
```bash
python generate-posts.py --platform linkedin --topic life-cover --count 1
```

## Project Structure

```
financial-advisor/
├── README.md                       # This file
├── mkdocs.yml                      # MkDocs config for docs site
│
├── config/
│   └── brand-voice.md             # Brand guidelines (edit this!)
│
├── docs/
│   ├── index.md                   # Home page
│   ├── brand-voice.md             # Brand guidelines (copy from config)
│   │
│   ├── topics/
│   │   ├── index.md               # Topic index (auto-generated)
│   │   ├── topics.json            # Topic data (auto-generated)
│   │   ├── life-cover.md
│   │   ├── income-protection.md
│   │   └── ...                    # One file per extracted topic
│   │
│   └── posts/
│       ├── index.md               # All posts index (auto-generated)
│       ├── linkedin/
│       │   ├── index.md           # LinkedIn posts index (auto-generated)
│       │   ├── 2025-04-27_life-cover_1.md
│       │   ├── 2025-04-27_life-cover_2.md
│       │   └── ...
│       ├── instagram/
│       │   ├── index.md           # Instagram posts index (auto-generated)
│       │   ├── 2025-04-27_life-cover_1.md
│       │   └── ...
│       └── tiktok/
│           ├── index.md           # TikTok posts index (auto-generated)
│           └── ...
│
└── scripts/
    ├── extract-topics.py          # Parse technical guide → topics
    ├── generate-posts.py          # Generate posts using Claude
    └── build-indexes.py           # Auto-build MkDocs indexes
```

## Workflow

### Content Generation Cycle

1. **Edit Brand Voice** → `config/brand-voice.md`
2. **Extract Topics** → `python extract-topics.py`
3. **Generate Posts** → `python generate-posts.py --platform X --topic Y`
4. **Review** → Open in MkDocs or read markdown files
5. **Publish** → Copy posts to Buffer/Later/native platform
6. **Track** → Monitor performance, refine brand voice for next batch

### Timestamps for Evolution Tracking

Each post is saved as: `YYYY-MM-DD_{topic}_{counter}.md`

This allows you to:
- See what was created when
- Track how you've improved over time
- Reuse successful topic angles
- Search by date in MkDocs

## Commands Reference

### Extract Topics
```bash
python scripts/extract-topics.py
# Parses: /Users/kennedysigauke/Downloads/LibertyLifestyleProtectorTechnicalGuide.md
# Creates: docs/topics/*.md + docs/topics/topics.json
```

### Generate Posts
```bash
python scripts/generate-posts.py \
  --platform linkedin \
  --topic life-cover \
  --count 3
```

Options:
- `--platform`: `linkedin`, `instagram`, or `tiktok`
- `--topic`: Topic slug (e.g., `life-cover`, `income-protection`)
- `--count`: Number of posts to generate (default: 1)

### Build Indexes
```bash
python scripts/build-indexes.py
# Auto-generates all index.md files for MkDocs navigation
# Run after generating posts to update navigation
```

### Preview Documentation
```bash
mkdocs serve
# Launches docs site at http://localhost:8000
```

## Examples

### LinkedIn Thought Leadership
```bash
python scripts/generate-posts.py \
  --platform linkedin \
  --topic life-cover \
  --count 2
```

Generates posts like:
- "Why I've seen so many breadwinners skip life cover..."
- "The gap between what people think they need and reality"

### Instagram Educational Hooks
```bash
python scripts/generate-posts.py \
  --platform instagram \
  --topic income-protection \
  --count 5
```

Generates short punchy posts:
- "Lost your income tomorrow? Most people aren't covered."
- "This 1 thing could've prevented financial disaster"

### TikTok Script Ideas
```bash
python scripts/generate-posts.py \
  --platform tiktok \
  --topic funeral-benefit \
  --count 3
```

Generates scripts with visual cues:
- "[shocked face] What happens to your family if you don't wake up tomorrow?"

## Customization

### Adjust Brand Voice
Edit `config/brand-voice.md`:
```markdown
## Core Tone
- Change from "educational" to "conversational"
- Adjust tone for different audiences
- Add platform-specific emojis
```

### Adjust Post Generation
Edit `generate-posts.py` to:
- Change Claude model (line with `model="claude-opus-4-7"`)
- Add new platforms
- Adjust token limits
- Add post approval workflow

## Publishing

### Option 1: Manual Copy-Paste
1. Open `docs/posts/{platform}/{date}_{topic}.md`
2. Copy post content
3. Paste into scheduling tool (Buffer, Later, etc.)

### Option 2: Integration (Future)
The system can be extended to:
- Auto-post to platforms via API
- Schedule posts via Buffer/Later webhooks
- Track engagement metrics

## Troubleshooting

### "Topic not found: life-cover"
Run `python extract-topics.py` first to create topics.

### Claude API errors
Check:
- `export ANTHROPIC_API_KEY="..."` is set
- API key is valid
- Rate limits haven't been exceeded

### MkDocs won't start
```bash
pip install mkdocs mkdocs-material
```

## Next Steps

1. **Run extraction**: `python scripts/extract-topics.py`
2. **Generate your first batch**: `python scripts/generate-posts.py --platform linkedin --topic {some-topic}`
3. **Preview**: `mkdocs serve`
4. **Refine brand voice** as you generate content
5. **Scale**: Keep generating and track what resonates

## Future Enhancements

- [ ] Auto-post to LinkedIn/Instagram via API
- [ ] Performance tracking (likes, engagement, reach)
- [ ] A/B testing for different angles
- [ ] Content calendar view in MkDocs
- [ ] Image/video suggestions for each post
- [ ] Batch scheduling to Buffer/Later

---

**Created:** April 2025  
**Status:** Active  
**Last Updated:** Check `docs/index.md`
