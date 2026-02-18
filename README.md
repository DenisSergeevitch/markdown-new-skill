# Markdown.new Skill

Single-skill repository for `markdown-new` - official Cloudflare URL-to-Markdown service ([markdown.new](https://markdown.new/)) converted into a skill.

Skill entrypoint:
- `markdown-new/SKILL.md`

## TL;DR

- Convert public URLs to clean Markdown via `markdown.new`.
- Supports method selection: `auto`, `ai`, `browser`.
- Supports standard output, file output, and wrapped delivery mode.

## Install on macOS/Linux (single command)

### Codex

```bash
git clone https://github.com/DenisSergeevitch/markdown-new-skill.git /tmp/markdown-new-skill && mkdir -p ~/.codex/skills && rm -rf ~/.codex/skills/markdown-new && cp -R /tmp/markdown-new-skill/markdown-new ~/.codex/skills/
```

### Claude Code

```bash
git clone https://github.com/DenisSergeevitch/markdown-new-skill.git /tmp/markdown-new-skill && mkdir -p ~/.claude/skills && rm -rf ~/.claude/skills/markdown-new && cp -R /tmp/markdown-new-skill/markdown-new ~/.claude/skills/
```

## Usage

```md
Use $markdown-new to convert web URLs into LLM-ready Markdown.
```

## Credits

- `webservervis` for the markdown conversion service powering this skill.
