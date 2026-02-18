# Markdown.new Skill

Single-skill repository for `markdown-new` - official Cloudflare URL-to-Markdown service ([markdown.new](https://markdown.new/)) converted into a skill.

Skill entrypoint:
- `markdown-new/SKILL.md`

## What It Does

`markdown-new` converts public web pages into LLM-ready Markdown using [markdown.new](https://markdown.new), with:
- URL-to-Markdown conversion for summarization, extraction, RAG, and archiving
- conversion fallback control (`auto`, `ai`, `browser`)
- optional image retention
- optional wrapped delivery mode for downstream parsing

## Path Resolution (Important)

- Relative paths such as `scripts/markdown_new_fetch.py` are relative to the skill directory.
- Do not run `python3 scripts/markdown_new_fetch.py ...` from workspace root unless `scripts/` exists there.
- Safe command from any current directory:

```bash
python3 ~/.codex/skills/markdown-new/scripts/markdown_new_fetch.py 'https://example.com'
```

## Modes

### Conversion Modes (`--method`)
- `auto`: default pipeline, fastest successful path
- `ai`: force Workers AI conversion path
- `browser`: force Browser Rendering for JS-heavy pages

### Output Modes
- default: print Markdown to stdout
- `--output <file>`: write Markdown to file
- `--deliver-md`: write `.md` output with wrapped content:

```text
<url>
...markdown...
</url>
```

If `--deliver-md` is used without `--output`, filename is auto-generated from the URL.

## Install Paths

- Codex (macOS/Linux): `~/.codex/skills/markdown-new`
- Claude Code (macOS/Linux): `~/.claude/skills/markdown-new`

## Install on macOS/Linux (single command)

### Codex

```bash
mkdir -p ~/.codex/skills && rm -rf ~/.codex/skills/markdown-new && cp -R /Users/pro16/Dropbox/experiments/skills-i-use/markdown-new ~/.codex/skills/
```

### Claude Code

```bash
mkdir -p ~/.claude/skills && rm -rf ~/.claude/skills/markdown-new && cp -R /Users/pro16/Dropbox/experiments/skills-i-use/markdown-new ~/.claude/skills/
```

## Quick Usage

```bash
python3 scripts/markdown_new_fetch.py 'https://example.com'
python3 scripts/markdown_new_fetch.py 'https://example.com' --method browser --retain-images --output page.md
python3 scripts/markdown_new_fetch.py 'https://example.com' --deliver-md
```

## Credits

- `webservervis` for the markdown conversion service powering this skill.
