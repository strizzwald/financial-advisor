# Financial Advisor Content Generator

Automated system for generating LinkedIn, Instagram, and TikTok content from financial product technical guides using Claude AI.

## Core Pipeline

```
source/*.md (technical guide)
  → scripts/extract-topics.py → docs/topics/*.md + topics.json
  → scripts/generate-posts.py → docs/posts/{platform}/{date}_{topic}_{n}.md
  → scripts/build-indexes.py  → MkDocs navigation indexes
  → mkdocs serve              → http://localhost:8000
```

## Common Commands

```bash
# 1. Extract topics from the technical guide
python scripts/extract-topics.py

# 2. Generate posts (platform: linkedin | instagram | tiktok)
python scripts/generate-posts.py --platform linkedin --topic life-cover --count 3

# 3. Rebuild navigation indexes after generating posts
python scripts/build-indexes.py

# 4. Preview docs locally
mkdocs serve
```

## Key Files

| File | Purpose |
|------|---------|
| `config/brand-voice.md` | Brand tone and platform-specific guidelines — read before generating |
| `docs/topics/topics.json` | Index of available topic slugs (auto-generated) |
| `docs/topics/*.md` | Individual topic summaries and key features |
| `scripts/generate-posts.py` | Post generation engine (uses Claude API) |
| `scripts/extract-topics.py` | Parses technical guides into topic files |
| `scripts/build-indexes.py` | Generates MkDocs navigation indexes |
| `source/` | Raw technical guides (input to extraction) |

## Environment

```bash
export ANTHROPIC_API_KEY="your-key-here"
pip install mkdocs mkdocs-material  # for docs preview
```

## Content Rules

- Do not manually edit `docs/posts/` — regenerate instead
- Do not manually edit `docs/topics/topics.json` — run extract-topics.py to update
- Always run `build-indexes.py` after bulk post generation
- Brand voice changes require regenerating posts to take effect

## Platform Specs

| Platform | Length | Tone |
|----------|--------|------|
| LinkedIn | 500–1000 chars | Professional, thought leadership, ends with question |
| Instagram | 60–150 chars | Punchy hook, 1–2 emojis, casual CTA |
| TikTok | 60–200 chars | Hook + quick insight + visual cues `[in brackets]` |

## Post Quality Checklist

- [ ] Matches platform tone
- [ ] No investment advice or guarantees
- [ ] No AI markers ("As an AI…")
- [ ] Includes relatable example or question
- [ ] Ends with engaging CTA

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Topic not found: X" | Run `extract-topics.py` first; check `topics.json` for valid slugs |
| Off-brand posts | Review and update `config/brand-voice.md`, then regenerate |
| MkDocs won't start | `pip install mkdocs mkdocs-material` |
