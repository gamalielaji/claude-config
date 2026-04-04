---
name: localize
description: "Run the localization workflow: extract strings, validate localization readiness, check for hardcoded text, and generate translation-ready string tables."
argument-hint: "[scan|extract|validate|status]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---
## Context Engineering (Karpathy Method)

Before execution, this skill automatically:

1. **Load** — Read all files referenced by the user or implied by the task
2. **Research** — If the task involves unfamiliar patterns or decisions, use WebSearch for current best practices (2-3 targeted queries, time-boxed to <20% of task)
3. **Scope** — Define exactly what this skill will produce and what it will NOT touch
4. **Constraints** — Identify boundaries before starting (format, quality bar, domain limits)

After execution, verify:
- [ ] Primary deliverable produced and matches requested format
- [ ] All user requirements addressed, no unresolved assumptions
- [ ] No scope creep beyond the task
- [ ] Recommendations are evidence-based (code, docs, or research)

When this skill is invoked:

1. **Parse the subcommand** from the argument:
   - `scan` — Scan for localization issues (hardcoded strings, missing keys)
   - `extract` — Extract new strings and generate/update string tables
   - `validate` — Validate existing translations for completeness and format
   - `status` — Report overall localization status

2. **For `scan`**:
   - Search `src/` for hardcoded user-facing strings:
     - String literals in UI code that are not wrapped in a localization function
     - Concatenated strings that should be parameterized
     - Strings with positional placeholders (`%s`, `%d`) instead of named ones (`{playerName}`)
   - Search for localization anti-patterns:
     - Date/time formatting not using locale-aware functions
     - Number formatting without locale awareness
     - Text embedded in images or textures (flag asset files)
     - Strings that assume left-to-right text direction
   - Report all findings with file paths and line numbers

3. **For `extract`**:
   - Scan all source files for localized string references
   - Compare against the existing string table (if any) in `assets/data/`
   - Generate new entries for strings that don't have keys yet
   - Suggest key names following the convention: `[category].[subcategory].[description]`
   - Output a diff of new strings to add to the string table

4. **For `validate`**:
   - Read all string table files in `assets/data/`
   - Check each entry for:
     - Missing translations (key exists but no translation for a locale)
     - Placeholder mismatches (source has `{name}` but translation is missing it)
     - String length violations (exceeds character limits for UI elements)
     - Orphaned keys (translation exists but nothing references the key in code)
   - Report validation results grouped by locale and severity

5. **For `status`**:
   - Count total localizable strings
   - Per locale: count translated, untranslated, and stale (source changed since translation)
   - Generate a coverage matrix:

   ```markdown
   ## Localization Status
   Generated: [Date]

   | Locale | Total | Translated | Missing | Stale | Coverage |
   |--------|-------|-----------|---------|-------|----------|
   | en (source) | [N] | [N] | 0 | 0 | 100% |
   | [locale] | [N] | [N] | [N] | [N] | [X]% |

   ### Issues
   - [N] hardcoded strings found in source code
   - [N] strings exceeding character limits
   - [N] placeholder mismatches
   - [N] orphaned keys (can be cleaned up)
   ```

### Rules
- English (en) is always the source locale
- Every string table entry must include a translator comment explaining context
- Never modify translation files directly — generate diffs for review
- Character limits must be defined per-UI-element and enforced automatically
- Right-to-left (RTL) language support should be considered from the start, not bolted on later
---

## Self-Evaluation Checklist

Before presenting final output:

1. Re-read output against the original request
2. Verify all success criteria are met
3. Check that output matches expected format/template
4. Ensure no scope creep or unrequested additions
5. Confirm recommendations are backed by evidence
