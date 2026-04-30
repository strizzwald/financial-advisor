# Agent Guidance for Financial Advisor Content Generator

## Project Overview

This is a **Financial Advisor Social Media Content Generator** — an automated system for creating platform-specific social media content (LinkedIn, Instagram, TikTok) from financial product knowledge.

**Core capabilities:**
- Extract topics from technical product guides
- Generate platform-specific posts using Claude AI
- Maintain a timestamped archive of all generated content
- Preview and navigate content via MkDocs
- Ensure consistent brand voice across platforms

## For Agents Working With This Project

### Quick Start
1. Read `README.md` for overview and `COMMANDS.md` for quick reference
2. Check `config/brand-voice.md` for current voice guidelines
3. Review `docs/topics/topics.json` to see available topics
4. Use the command reference below to generate or modify content

### Key Files & Their Purpose

| File | Purpose | Agent Action |
|------|---------|--------------|
| `config/brand-voice.md` | Central source of truth for tone, voice, platform guidelines | Read before generating; suggest edits if voice needs refinement |
| `docs/topics/topics.json` | Index of all available topics (auto-generated) | Reference to validate topic slugs before generating posts |
| `docs/topics/*.md` | Individual topic details (summaries, key features) | Read to understand context; suggest new topics if gaps exist |
| `scripts/generate-posts.py` | Post generation engine (currently uses Ollama/Deepseek) | Modify to switch models, add platforms, or adjust generation logic |
| `scripts/extract-topics.py` | Technical guide parser | Run when new technical guides are added |
| `scripts/build-indexes.py` | Auto-generates navigation indexes for MkDocs | Run after bulk post generation to update docs |
| `docs/posts/{platform}/` | Generated posts organized by platform and date | Read to review outputs; suggest improvements to brand voice if quality drifts |
| `mkdocs.yml` | MkDocs configuration for documentation site | Modify if adding new sections or changing site structure |

### Common Agent Workflows

#### Workflow 1: Generate Posts for a Topic
```bash
# 1. Verify topic exists
grep -o '"slug": "[^"]*"' docs/topics/topics.json | head

# 2. Generate posts
python scripts/generate-posts.py --platform linkedin --topic life-cover --count 3

# 3. Rebuild indexes (if not done recently)
python scripts/build-indexes.py

# 4. Optionally preview
mkdocs serve  # Visit http://localhost:8000
```

**Agent decision points:**
- If topic not found: Run `python scripts/extract-topics.py` first (requires technical guide file)
- If quality is poor: Suggest edits to `config/brand-voice.md` and regenerate
- If posts seem off-brand: Check brand-voice.md hasn't drifted

#### Workflow 2: Update Brand Voice
```bash
# 1. Review current brand voice
cat config/brand-voice.md

# 2. Edit based on feedback
# - Adjust tone/characteristics if posts don't reflect desired voice
# - Add/remove platform-specific guidelines
# - Update language rules if certain phrases keep appearing

# 3. Regenerate sample posts to validate changes
python scripts/generate-posts.py --platform linkedin --topic income-protection --count 1

# 4. If good, regenerate batch for all platforms
for platform in linkedin instagram tiktok; do
  python scripts/generate-posts.py --platform $platform --topic life-cover --count 2
done
```

**Agent decision points:**
- Changes should be driven by: generated post quality, stakeholder feedback, or observed patterns
- Always test brand voice changes on a small batch first
- If regenerated posts still don't match desired voice, the issue may be in topic summaries

#### Workflow 3: Add New Products/Topics
```bash
# 1. Get the technical guide (usually a PDF or markdown file)
# 2. Run extraction
python scripts/extract-topics.py

# 3. Verify new topics were created
grep -c '"slug"' docs/topics/topics.json

# 4. Generate posts from new topics
python scripts/generate-posts.py --platform linkedin --topic {new-slug} --count 2
```

**Agent decision points:**
- extraction-topics.py looks for a specific input file path — check the script for location
- New topics should be validated by reviewing the markdown files created in `docs/topics/`
- If extracted topics are missing key details, consider editing them directly in the `.md` files

#### Workflow 4: Review & Iterate on Generated Content
```bash
# 1. List recent posts by platform
ls -lart docs/posts/linkedin/ | tail -5

# 2. Review specific post
cat docs/posts/linkedin/2025-04-29_life-cover_1.md

# 3. If quality issues:
#    a) Check if brand-voice.md needs updating
#    b) Check if topic summary is unclear
#    c) Consider regenerating with different count/platform combo

# 4. If consistently good:
#    Archive satisfied, move to publishing/sharing workflow
```

### Model Selection & Performance

**Current setup:** Uses Ollama with `deepseek-r1:latest`

**Switching to Claude:**
- Edit `scripts/generate-posts.py` to use Anthropic SDK instead of Ollama
- Will require `ANTHROPIC_API_KEY` environment variable
- Consider using `claude-opus-4-7` for best quality, `claude-sonnet-4-6` for speed/cost balance

**Performance notes:**
- Ollama local inference: 2-5 minutes per batch (model warming)
- Generation is slow; don't over-optimize prematurely
- Success metric: Posts match brand voice and drive engagement

### Editing & Customization Points for Agents

**Safe to edit without breaking things:**
- `config/brand-voice.md` — Update guidelines, adjust tone
- Topic markdown files directly (`docs/topics/*.md`) — Fix summaries or key features
- `mkdocs.yml` — Adjust documentation site styling/structure

**Requires care (test after editing):**
- `scripts/generate-posts.py` — Model changes, platform additions, token limits
- `scripts/extract-topics.py` — Input file paths, parsing logic
- `scripts/build-indexes.py` — Index generation logic

**Don't edit:**
- `docs/posts/` — This is generated output; regenerate instead of manually editing
- `docs/topics/topics.json` — Auto-generated index; run extraction script to update

### Understanding the Pipeline

```
Technical Guide (PDF/Markdown)
  ↓
extract-topics.py
  ↓
docs/topics/*.md + docs/topics/topics.json
  ↓
generate-posts.py (reads topics + brand-voice)
  ↓
docs/posts/{platform}/{date}_{topic}_{n}.md
  ↓
build-indexes.py (creates navigation)
  ↓
mkdocs.serve (documentation site for preview)
  ↓
Manual copy → Publishing platform (LinkedIn, Instagram, TikTok)
```

### Environment Setup for Agents

Before running scripts, ensure:
```bash
# If using Claude instead of Ollama:
export ANTHROPIC_API_KEY="your-key-here"

# If using Ollama (current):
ollama serve  # Must be running in another terminal

# Optional: MkDocs for preview
pip install mkdocs mkdocs-material
```

### Testing & Validation

**Post quality checklist:**
- [ ] Matches platform tone (professional for LinkedIn, casual for Instagram/TikTok)
- [ ] Respects character/word limits
- [ ] No AI-specific markers ("As an AI", "I cannot", etc.)
- [ ] Includes relatable examples or questions
- [ ] No investment advice or guarantees
- [ ] Ends with engaging CTA

**Content validation:**
```bash
# Count posts by platform to track output
ls -1 docs/posts/linkedin/*.md | wc -l
ls -1 docs/posts/instagram/*.md | wc -l
ls -1 docs/posts/tiktok/*.md | wc -l

# Find posts from a specific date
find docs/posts -name "2025-04-29*"
```

### Troubleshooting

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| "Topic not found: X" | Topic slug doesn't exist | Run `extract-topics.py` or check `topics.json` |
| Posts are generic/off-brand | Brand voice not applied correctly | Review `brand-voice.md`; regenerate; compare |
| Ollama connection error | Ollama not running | Start Ollama: `ollama serve` in another terminal |
| MkDocs won't start | Dependencies missing | `pip install mkdocs mkdocs-material` |
| Generated posts have weird JSON | Model output parsing failed | Check prompt structure; consider switching models |

### When to Suggest Human Intervention

Escalate to human stakeholder when:
- **Brand voice drift detected:** Posts don't match guidelines despite proper setup
- **Low-quality generations:** Multiple batches fail quality checks
- **Engagement feedback:** Posts aren't performing; need strategic pivot
- **New product launch:** New technical guide with fundamentally different messaging
- **Platform changes:** New platforms (YouTube Shorts, Threads, etc.) need platform-specific guidelines

### Future Enhancement Opportunities for Agents

These are explicitly NOT implemented yet, but agents may want to contribute:

- [ ] Auto-post to LinkedIn/Instagram via API (requires OAuth setup)
- [ ] Performance tracking dashboard (stores likes, engagement, reach)
- [ ] A/B testing framework (compare angle effectiveness)
- [ ] Content calendar view in MkDocs
- [ ] Image/video suggestions per post (integration with Nanobana/vision APIs)
- [ ] Batch scheduling to Buffer/Later (webhook integration)
- [ ] Sentiment analysis on generated posts (quality gate before publishing)

---

**Last Updated:** April 29, 2025  
**Maintained by:** Human stakeholder + Claude agents  
**Status:** Active, regularly generating content
