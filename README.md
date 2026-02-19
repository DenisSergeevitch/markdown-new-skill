# Markdown.new Skill

Single-skill repository for `markdown-new` - official Cloudflare URL-to-Markdown service ([markdown.new](https://markdown.new/)) converted into a skill.

Skill entrypoint:
- `markdown-new/SKILL.md`

## TL;DR

- Convert public URLs to clean Markdown via `markdown.new`.
- Supports method selection: `auto`, `ai`, `browser`.
- Supports standard output, file output, and wrapped delivery mode.

## What This Means

### Method selection (`--method`)

- `auto`: use the fastest successful conversion path. Start here for most URLs.
- `ai`: prefer the Workers AI conversion path.
- `browser`: force browser rendering for JS-heavy pages where plain fetch may miss content.

### Output modes

- standard output: print markdown directly to terminal/stdout (good for pipes).
- file output: `--output <path>` writes markdown to a file.
- wrapped delivery mode: `--deliver-md` writes markdown wrapped in pseudo-XML tags, which is useful for reasoning LLMs on long reads and reduces format confusion:

```text
<url>
...markdown...
</url>
```

If `--deliver-md` is used and `--output` is omitted, a `.md` filename is auto-generated from the URL.

## How It Works

1. Validate that the provided URL is a public `http/https` URL.
2. Send a `POST https://markdown.new/` request with `url`, `method`, and `retain_images`.
3. Accept either response shape: raw markdown (`text/markdown`) or JSON payload with markdown in `content`.
4. Normalize response metadata (for example conversion method and timing).
5. Emit markdown via stdout, file output, or wrapped delivery mode.

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

Manual script invocation from any directory:

```bash
python3 ~/.codex/skills/markdown-new/scripts/markdown_new_fetch.py 'https://example.com'
```

Mode examples:

```bash
# stdout
python3 ~/.codex/skills/markdown-new/scripts/markdown_new_fetch.py 'https://example.com'

# file output
python3 ~/.codex/skills/markdown-new/scripts/markdown_new_fetch.py 'https://example.com' --output page.md

# wrapped delivery mode
python3 ~/.codex/skills/markdown-new/scripts/markdown_new_fetch.py 'https://example.com' --deliver-md --output packet.md
```

## Credits

- `webservervis` for the markdown conversion service powering this skill.
