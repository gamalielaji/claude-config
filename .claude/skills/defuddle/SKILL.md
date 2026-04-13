---
name: defuddle
description: Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page.
user-invocable: true
allowed-tools: Bash
---

# Defuddle

Use Defuddle CLI to extract clean readable content from web pages. Prefer over WebFetch for standard web pages — it removes navigation, ads, and clutter, reducing token usage.

1. **Check Defuddle is installed** — if not: `npm install -g defuddle`
2. **Parse the URL to markdown** — `defuddle parse <url> --md`
3. **Save to file if needed** — `defuddle parse <url> --md -o content.md`
4. **Extract specific metadata if needed** — `defuddle parse <url> -p title` (or `description`, `domain`)

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with both HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |

## When to Use vs Alternatives

| Scenario | Use |
|----------|-----|
| Standard article, blog, docs page | **Defuddle** (cleaner output, fewer tokens) |
| SPA / JavaScript-rendered content | **WebFetch** (Defuddle may return empty body) |
| Auth-gated or login-required page | **WebFetch** or browser tools |
| Page behind Cloudflare/bot protection | **WebFetch** (Defuddle gets blocked) |
| Defuddle returns empty or garbled output | Fall back to **WebFetch** |

## Error Handling

- **Not installed**: If `defuddle` command not found, run `npm install -g defuddle` first
- **Empty output**: Page is likely a SPA. Fall back to `WebFetch`
- **Timeout/connection error**: Check URL validity. Retry once, then fall back to `WebFetch`
- **Garbled/partial output**: Page may have anti-bot protection. Fall back to `WebFetch`
