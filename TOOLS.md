# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Image Generation

### nano-banana-pro (Gemini 3 Pro Image)

- ✅ API Key: Configured in `~/.bashrc` as `GEMINI_API_KEY`
- ✅ Available globally - works in all sessions
- Usage:
  ```bash
  uv run ~/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py \
    --prompt "描述" \
    --filename "output.png" \
    --resolution 1K
  ```
- Resolutions: `1K` (default), `2K`, `4K`
- Supports editing with `-i input.png`
- Supports multi-image composition (up to 14 images)

### openai-image-gen (DALL-E)

- ❌ Billing limit reached - currently unavailable
- Fallback: Use nano-banana-pro instead

---

Add whatever helps you do your job. This is your cheat sheet.
