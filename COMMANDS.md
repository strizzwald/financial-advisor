# Quick Command Reference

Save this for fast access to common operations.

## Setup (Do Once)

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Install MkDocs for preview (optional)
pip install mkdocs mkdocs-material

# Navigate to project
cd /Users/kennedysigauke/Work/Personal/financial-advisor
```

## Extract Topics (Do Once)

```bash
# Parse technical guide → create topics
python scripts/extract-topics.py
```

## Generate Posts (Repeated)

```bash
# LinkedIn posts about life-cover
python scripts/generate-posts.py --platform linkedin --topic life-cover --count 3

# Instagram shorts about income-protection
python scripts/generate-posts.py --platform instagram --topic income-protection --count 5

# TikTok scripts about any topic
python scripts/generate-posts.py --platform tiktok --topic funeral-benefit --count 2

# Get topic slugs available
grep '"slug"' docs/topics/topics.json | grep -o '"[^"]*"' | tail -n +2 | head -10
```

## Update & Navigate

```bash
# Regenerate all indexes (do after generating posts)
python scripts/build-indexes.py

# Preview docs locally
mkdocs serve
# → Visit http://localhost:8000

# List recent posts
ls -lart docs/posts/linkedin/ | tail -5

# View a specific post
cat docs/posts/linkedin/2025-04-27_life-cover_1.md
```

## Edit Brand Voice

```bash
# Edit brand voice (all posts use this)
nano config/brand-voice.md

# Then regenerate posts to apply changes
python scripts/generate-posts.py --platform linkedin --topic life-cover --count 1
```

## Common Workflows

### Generate Multiple Posts Quickly
```bash
for topic in life-cover income-protection funeral-benefit; do
  python scripts/generate-posts.py --platform linkedin --topic $topic --count 2
done
python scripts/build-indexes.py
mkdocs serve
```

### Create Content for All Three Platforms
```bash
topic="life-cover"
python scripts/generate-posts.py --platform linkedin --topic $topic --count 2
python scripts/generate-posts.py --platform instagram --topic $topic --count 5
python scripts/generate-posts.py --platform tiktok --topic $topic --count 3
python scripts/build-indexes.py
```

### Find Posts from Specific Date
```bash
# All posts from April 27
find docs/posts -name "2025-04-27*"

# LinkedIn posts from April 27
ls docs/posts/linkedin/2025-04-27*
```

## Platform Guidelines (Quick Ref)

**LinkedIn** (500-1000 chars)
```bash
python scripts/generate-posts.py --platform linkedin --topic life-cover --count 1
```
→ Professional, thought leadership, question ending

**Instagram** (60-150 chars)
```bash
python scripts/generate-posts.py --platform instagram --topic life-cover --count 1
```
→ Punchy hook, 1-2 emojis, casual CTA

**TikTok** (60-200 chars)
```bash
python scripts/generate-posts.py --platform tiktok --topic life-cover --count 1
```
→ Hook, quick insight, visual cues [in brackets], energy

## Debug / Check

```bash
# View available topics
cat docs/topics/topics.json | jq '.[] | .slug'

# Count posts by platform
echo "LinkedIn: $(ls docs/posts/linkedin/*.md 2>/dev/null | wc -l)"
echo "Instagram: $(ls docs/posts/instagram/*.md 2>/dev/null | wc -l)"
echo "TikTok: $(ls docs/posts/tiktok/*.md 2>/dev/null | wc -l)"

# Check API key is set
echo $ANTHROPIC_API_KEY

# Check latest post
ls -lart docs/posts/*/[0-9]*.md | tail -1
```

## Customize

```bash
# Edit brand voice
nano config/brand-voice.md

# Edit post generation (models, lengths, etc)
nano scripts/generate-posts.py

# Change which model Claude uses
# Find: model="claude-opus-4-7"
# Change to: model="claude-sonnet-4-6" (faster/cheaper)
```

## File Locations

| What | Where |
|------|-------|
| Brand voice | `config/brand-voice.md` |
| Topics | `docs/topics/*.md` |
| LinkedIn posts | `docs/posts/linkedin/` |
| Instagram posts | `docs/posts/instagram/` |
| TikTok posts | `docs/posts/tiktok/` |
| Scripts | `scripts/` |
| Documentation | `docs/index.md` |

---

**Pro tip:** Pin this file to your terminal or editor for fast reference.
