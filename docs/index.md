# Financial Advisor Content Hub

Automated social media content generator for financial education. Creates LinkedIn posts, Instagram shorts, and TikTok scripts from product knowledge.

## Quick Start

### Generate posts on-demand
```bash
cd scripts
python generate-posts.py --platform linkedin --topic "life-cover" --count 3
```

### View content
```bash
mkdocs serve
# Then visit http://localhost:8000
```

### Update brand voice
Edit `../config/brand-voice.md` and regenerate posts for consistency.

## Structure

- **`config/brand-voice.md`** — Brand guidelines (tweakable)
- **`docs/topics/`** — Extracted product topics from technical guide
- **`docs/posts/`** — Generated social media content (organized by platform + timestamp)
- **`scripts/`** — Generation and utility scripts

## Workflow

1. **Extract Topics** → Parse technical guide for key concepts
2. **Generate Posts** → Create platform-specific content using Claude API
3. **Review & Tweak** → Edit brand voice as needed
4. **Publish** → Copy posts to scheduling tool (Buffer, Later, etc.)
5. **Track** → Monitor performance, refine for next batch

## Platform Guidelines

### LinkedIn (Professional, Long-form)
- 500-1000 characters
- Thought leadership angle
- Include personal insight or question

### Instagram / TikTok (Casual, Short-form)
- 60-150 characters
- Punchy hook first
- Visual-friendly formatting

## Generated Content

All posts are stored with timestamps: `YYYY-MM-DD_topic-slug.md`

This allows easy tracking of:
- What was generated when
- How topics evolve
- Performance trends by date

---

**Last updated:** Run `python scripts/build-indexes.py` to auto-update navigation
