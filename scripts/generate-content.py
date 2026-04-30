#!/usr/bin/env python3
"""
Master content generator: Creates posts + infographics in one command.
"""

import subprocess
import argparse
import sys
from pathlib import Path

def run_command(cmd: list, description: str) -> bool:
    """Run a command and report status."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False

    print(result.stdout.strip())
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate social media posts + infographics")
    parser.add_argument('--topic', required=True, help="Topic slug (e.g., 'life-cover')")
    parser.add_argument('--platform', choices=['linkedin', 'instagram', 'tiktok', 'all'], default='all')
    parser.add_argument('--count', type=int, default=3, help="Posts per platform")

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    platforms = ['linkedin', 'instagram', 'tiktok'] if args.platform == 'all' else [args.platform]

    print(f"🚀 Generating content for '{args.topic}'")
    print(f"   Platforms: {', '.join(platforms)}")
    print(f"   Posts per platform: {args.count}")

    all_success = True

    # Generate posts for each platform
    for platform in platforms:
        cmd = [
            'python3', str(script_dir / 'generate-posts.py'),
            '--platform', platform,
            '--topic', args.topic,
            '--count', str(args.count)
        ]
        if not run_command(cmd, f"📝 Generating {platform} posts"):
            all_success = False

    # Generate infographic
    cmd = [
        'python3', str(script_dir / 'generate-infographics.py'),
        '--topic', args.topic
    ]
    if not run_command(cmd, "🎨 Generating infographic"):
        all_success = False

    # Build indexes
    cmd = ['python3', str(script_dir / 'build-indexes.py')]
    if not run_command(cmd, "📑 Building navigation indexes"):
        all_success = False

    if all_success:
        print(f"\n✅ Content generated successfully!")
        print(f"\n📍 Location: docs/posts/")
        print(f"   - Posts: docs/posts/{{platform}}/")
        print(f"   - Infographics: docs/posts/infographics/")
        print(f"\n💡 Next: Run 'mkdocs serve' to preview")
    else:
        print(f"\n⚠️  Some steps failed. Check output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
