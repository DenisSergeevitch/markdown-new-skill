#!/usr/bin/env python3
"""Convert public URLs to Markdown through markdown.new."""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple


DEFAULT_API_URL = "https://markdown.new/"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch Markdown from a public URL using markdown.new"
    )
    parser.add_argument("url", help="Public URL to convert (http/https)")
    parser.add_argument(
        "--method",
        choices=["auto", "ai", "browser"],
        default="auto",
        help="Conversion method to request (default: auto)",
    )
    parser.add_argument(
        "--retain-images",
        action="store_true",
        help="Request image retention in output markdown",
    )
    parser.add_argument(
        "--output",
        help="Write markdown to this file instead of stdout",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=45.0,
        help="Request timeout in seconds (default: 45)",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help="markdown.new API endpoint (default: https://markdown.new/)",
    )
    parser.add_argument(
        "--show-headers",
        action="store_true",
        help="Print response headers to stderr",
    )
    parser.add_argument(
        "--deliver-md",
        action="store_true",
        help=(
            "Write output into a .md file and wrap content in pseudo-XML "
            "<url>...</url> tags"
        ),
    )
    return parser


def validate_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url!r}. Use absolute http/https URL.")


def build_request(api_url: str, payload: Dict[str, object]) -> urllib.request.Request:
    data = json.dumps(payload).encode("utf-8")
    return urllib.request.Request(
        api_url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "text/markdown",
            "User-Agent": "codex-markdown-new-skill/1.0",
        },
    )


def normalize_body(body: str, headers: Dict[str, str]) -> Tuple[str, Dict[str, str]]:
    content_type = headers.get("content-type", "")
    if "application/json" not in content_type:
        return body, {}

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return body, {}

    if not isinstance(payload, dict):
        return body, {}

    markdown = payload.get("content")
    if not isinstance(markdown, str):
        return body, {}

    metadata: Dict[str, str] = {}
    for key in ("title", "url", "method", "duration_ms", "timestamp"):
        value = payload.get(key)
        if value is not None:
            metadata[f"response_{key}"] = str(value)

    return markdown, metadata


def print_metadata(
    headers: Dict[str, str], show_headers: bool, response_meta: Dict[str, str]
) -> None:
    tokens = headers.get("x-markdown-tokens")
    remaining = headers.get("x-rate-limit-remaining")

    if tokens:
        print(f"x-markdown-tokens: {tokens}", file=sys.stderr)
    if remaining:
        print(f"x-rate-limit-remaining: {remaining}", file=sys.stderr)
    for key, value in sorted(response_meta.items()):
        print(f"{key}: {value}", file=sys.stderr)

    if show_headers:
        for key, value in sorted(headers.items()):
            print(f"{key}: {value}", file=sys.stderr)


def slugify_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    raw = f"{parsed.netloc}{parsed.path}".strip("/")
    if not raw:
        raw = parsed.netloc or "page"
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", raw).strip("_")
    return slug or "page"


def resolve_output_path(url: str, output_path: Optional[str], deliver_md: bool) -> Optional[str]:
    if output_path:
        if deliver_md and not output_path.lower().endswith(".md"):
            output_path = f"{output_path}.md"
        return output_path

    if deliver_md:
        return f"{slugify_url(url)}.md"

    return None


def wrap_in_url_tag(markdown: str) -> str:
    body = markdown.rstrip("\n")
    return f"<url>\n{body}\n</url>\n"


def write_output(markdown: str, output_path: Optional[str]) -> None:
    if output_path:
        path = Path(output_path)
        if path.parent != Path("."):
            path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(markdown)
        return
    sys.stdout.write(markdown)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        validate_url(args.url)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    payload = {
        "url": args.url,
        "method": args.method,
        "retain_images": bool(args.retain_images),
    }

    req = build_request(args.api_url, payload)

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8", errors="replace")
        print(f"HTTP {err.code} from markdown.new", file=sys.stderr)
        if err.code == 429:
            print(
                "Rate limit reached (documented: 500 requests/day/IP). Retry later.",
                file=sys.stderr,
            )
        if error_body:
            print(error_body.strip(), file=sys.stderr)
        return 1
    except urllib.error.URLError as err:
        print(f"Request failed: {err.reason}", file=sys.stderr)
        return 1

    markdown, response_meta = normalize_body(body, headers)
    print_metadata(headers, args.show_headers, response_meta)

    content = wrap_in_url_tag(markdown) if args.deliver_md else markdown
    output_path = resolve_output_path(args.url, args.output, args.deliver_md)
    write_output(content, output_path)

    if args.deliver_md and output_path:
        print(f"output_file: {Path(output_path).resolve()}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
