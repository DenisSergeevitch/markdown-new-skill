# markdown.new API Reference Notes

## Endpoints

- Prefix conversion: `GET https://markdown.new/<absolute-url>`
- API conversion: `POST https://markdown.new/`

## POST Request

- Content type: `application/json`
- Body fields:
  - `url` (string, required): public URL to convert
  - `method` (string, optional): `auto` (default), `ai`, or `browser`
  - `retain_images` (boolean, optional): `false` (default)

Example:

```json
{
  "url": "https://example.com",
  "method": "auto",
  "retain_images": false
}
```

## Response

- Status: `200` on success
- Prefix mode typically returns Markdown (`text/markdown`)
- POST mode may return JSON (`application/json`) with Markdown in `content`
- Common headers:
  - `x-markdown-tokens`: estimated token count for the returned Markdown
  - `x-rate-limit-remaining`: remaining requests for current daily quota

## Conversion Pipeline (as documented)

1. Request native Markdown via `Accept: text/markdown`
2. Fall back to Workers AI `toMarkdown()` when HTML is returned
3. Fall back to Browser Rendering for JS-heavy pages

## Operational Notes

- Documented rate limit: 500 requests/day per IP
- `429` indicates rate-limit exhaustion
- Public URLs only; authenticated/paywalled pages may fail
- Browser rendering usually adds latency compared with `auto`/`ai`

## Skill Script Notes

- `scripts/markdown_new_fetch.py --deliver-md` writes a `.md` file and wraps the markdown body with pseudo-XML tags:

```text
<url>
...markdown...
</url>
```
