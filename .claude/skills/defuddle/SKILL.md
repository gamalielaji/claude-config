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
