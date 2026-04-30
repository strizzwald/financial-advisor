# Getting Started

Your automated financial advisor content generation system is ready. Follow these steps to create your first posts.

## Step 1: Set Your API Key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Get your API key from https://console.anthropic.com (you may need to create an account or use your existing one).

## Step 2: Install MkDocs (Optional, for Preview)

```bash
pip install mkdocs mkdocs-material
```

This allows you to preview your content locally.

## Step 3: Extract Topics from Technical Guide

Run this to parse the technical guide and create topic files:

```bash
cd /Users/kennedysigauke/Work/Personal/financial-advisor
python scripts/extract-topics.py
```

This will:
- Parse the Liberty Lifestyle Protector Technical Guide
- Create individual topic markdown files
- Generate a JSON index of all topics

**Output:** `docs/topics/*.md` and `docs/topics/topics.json`

## Step 4: Generate Your First Posts

After extraction completes, list available topics:

```bash
cat docs/topics/topics.json | jq '.[].slug' | head -10
```

Then generate posts for a topic:

```bash
python scripts/generate-posts.py \
  --platform linkedin \
  --topic "life-cover" \
  --count 2
```

This will:
- Read the topic and brand voice
- Generate 2 unique LinkedIn posts using Claude
- Save them to `docs/posts/linkedin/`

**Try other platforms:**
```bash
# Instagram short hooks
python scripts/generate-posts.py --platform instagram --topic "income-protection" --count 3

# TikTok scripts
python scripts/generate-posts.py --platform tiktok --topic "life-cover" --count 2
```

## Step 5: View Your Posts

### Option A: View as Markdown Files
```bash
# See recent LinkedIn posts
ls -la docs/posts/linkedin/ | tail -5

# Read a specific post
cat docs/posts/linkedin/2025-04-27_life-cover_1.md
```

### Option B: Preview in MkDocs
```bash
mkdocs serve
```

Then visit `http://localhost:8000` in your browser.

## Step 6: Build Navigation Indexes

After generating posts, update navigation:

```bash
python scripts/build-indexes.py
```

This auto-generates index files for easier browsing in MkDocs.

## Step 7: Refine & Iterate

### Tweak Brand Voice
Edit `config/brand-voice.md` to adjust:
- Tone and professionalism level
- Emoji usage
- Platform-specific CTAs
- Topics to prioritize

Then regenerate posts to see the impact:
```bash
python scripts/generate-posts.py --platform linkedin --topic "life-cover" --count 1
```

### Generate More Content
Pick a new topic and run the generator:
```bash
python scripts/generate-posts.py \
  --platform instagram \
  --topic "funeral-benefit" \
  --count 5
```

## What Happens Behind the Scenes

1. **extract-topics.py** — Parses the technical guide, finds headers and bullet points, creates topic files
2. **generate-posts.py** — Calls Claude API to create platform-specific content based on brand voice + topic
3. **build-indexes.py** — Scans generated posts and creates index files for MkDocs navigation

All posts are stored with timestamps: `YYYY-MM-DD_{topic}_{counter}.md`

This means you can:
- See what was created when
- Track evolution of your content
- Find posts from a specific date
- Reuse successful angles

## Example: Full Workflow

```bash
# 1. Extract topics from technical guide
python scripts/extract-topics.py

# 2. See what topics are available
grep '"slug"' docs/topics/topics.json | head -5

# 3. Generate LinkedIn posts about multiple topics
python scripts/generate-posts.py --platform linkedin --topic "life-cover" --count 3
python scripts/generate-posts.py --platform linkedin --topic "income-protection" --count 2

# 4. Generate Instagram shorts
python scripts/generate-posts.py --platform instagram --topic "life-cover" --count 5

# 5. Build indexes for better navigation
python scripts/build-indexes.py

# 6. Preview everything
mkdocs serve
```

## Troubleshooting

**"topics.json not found"**
→ Run `python scripts/extract-topics.py` first

**"Topic not found"**
→ Check the slug in `docs/topics/topics.json` matches what you're asking for

**Claude API errors**
→ Make sure `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY`

**MkDocs won't start**
→ Run `pip install mkdocs mkdocs-material`

## Next: Advanced Usage

Once you're comfortable:
- **Batch generation**: Create a loop to generate multiple platforms at once
- **Performance tracking**: Add a spreadsheet to track engagement by topic/angle
- **Content calendar**: Use MkDocs to plan your posting schedule
- **API integration**: Auto-post to LinkedIn/Instagram (future enhancement)

## Customization Ideas

### Edit Brand Voice for Different Personas
Create multiple voice files:
- `brand-voice-expert.md` (technical, authoritative)
- `brand-voice-friendly.md` (casual, relatable)
- `brand-voice-educator.md` (educational, in-depth)

### Add More Topics
Manually add markdown files to `docs/topics/` with similar structure, then generate posts.

### Change Generation Model
Edit `generate-posts.py` line with `model=` to use different Claude versions (e.g., `claude-sonnet-4-6` for faster/cheaper).

## Questions?

Check:
- README.md — Full documentation
- config/brand-voice.md — Brand guidelines
- docs/index.md — Content overview

---

**Ready? Start with:**
```bash
cd /Users/kennedysigauke/Work/Personal/financial-advisor
python scripts/extract-topics.py
```
