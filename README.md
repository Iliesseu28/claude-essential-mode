<p align="center">
  <img src="docs/poster.png" alt="claude-essential-mode: Cut 65% of Claude Code output tokens without sounding like a caveman" width="100%">
</p>

# claude-essential-mode

### Cut 65% of Claude Code output tokens without sounding like a caveman. High-school clarity, conclusion first, zero fluff, zero em-dashes.

[![Release](https://img.shields.io/github/v/release/Iliesseu28/claude-essential-mode?color=D97757)](https://github.com/Iliesseu28/claude-essential-mode/releases)
![Claude Code style](https://img.shields.io/badge/Claude%20Code-output--style-D97757)
![dependencies](https://img.shields.io/badge/dependencies-0-3fb950)
![tokens saved](https://img.shields.io/badge/output%20tokens--65%25-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Ask any standard AI coding assistant a simple question, and you usually get a textbook chapter: conversational throat-clearing (*"Sure! I would be delighted to help you analyze that..."*), an unsolicited restatement of your prompt, three paragraphs repeating what the CLI tools just executed, and an unranked laundry list of theoretical possibilities.

**Essential Mode** is a native Claude Code output style that cuts 65% of output tokens without turning the model into a caveman. Answers fit in a single screen, start with the conclusion in line 1, use structured tables and checklists, pick one recommended fix, and strictly ban em-dashes for natural human phrasing.

https://github.com/Iliesseu28/claude-essential-mode/releases/download/v1.0.0/demo.mp4

## Quick Install

In Claude Code:

```bash
# macOS / Linux / WSL
curl -fsSL https://raw.githubusercontent.com/Iliesseu28/claude-essential-mode/main/install.sh | bash

# Windows PowerShell
irm https://raw.githubusercontent.com/Iliesseu28/claude-essential-mode/main/install.ps1 | iex
```

That is it: the installer drops `essential.md` into your Claude Code output styles folder and activates it in `~/.claude/settings.json`.

Toggle it live in any session with `/output-style essential`, or revert anytime with `/output-style default`.

## What you get

| | |
|---|---|
| **Conclusion in Line 1** | The direct answer or fix comes first. Explanations follow only if strictly necessary. |
| **High-School Clarity** | Plain everyday words and simple grammar. Technical terms are defined immediately in parentheses. |
| **Schematic by Default** | Tables, checklists, or ASCII diagrams replace walls of text. Never write a paragraph when a table does the job. |
| **Single Recommendation** | Recommends one clear solution and explains why in one line, rather than dumping five unranked choices. |
| **Zero Conversational Fluff** | No greetings, no throat-clearing, no restating your prompt, and no summarizing terminal actions already visible on screen. |
| **No Em-Dashes** | Strictly bans em-dashes and en-dashes, eliminating the most recognizable signature of AI writing. |
| **Full Fidelity Preserved** | Exact file paths, line numbers, git commands, and error stack traces are never truncated. |

## Before / After

<table>
<tr>
<td width="50%">

### 🗣️ Default Claude Code (184 tokens)

> "Certainly! I would be glad to help you resolve this issue. The reason your React component is continuously re-rendering is most likely due to creating a new object reference on every render cycle. When you pass an inline object or callback prop without memoization, React's shallow equality check sees it as a completely distinct entity, thus triggering a cascade of unnecessary renders. To remedy this situation, I recommend wrapping the calculation with useMemo, or extracting the object outside the render scope if static."

</td>
<td width="50%">

### ⚡ Essential Mode (38 tokens)

> **Conclusion**: Your component re-renders because an inline object prop creates a new reference on each cycle.
>
> | Issue | Fix |
> |---|---|
> | Inline object prop triggers shallow diff | Wrap with `useMemo` or move outside component |

</td>
</tr>
<tr>
<td>

### 🗣️ Default Claude Code (142 tokens)

> "Great question! When choosing between Redis and PostgreSQL for caching session data, there are several key factors to consider. PostgreSQL offers relational integrity and avoids running an extra server if you are already using it. On the other hand, Redis operates entirely in-memory and gives sub-millisecond latencies under high concurrency. Here is a detailed breakdown of 5 architectural trade-offs to evaluate for your stack..."

</td>
<td>

### ⚡ Essential Mode (44 tokens)

> **Recommendation**: Use Redis.
>
> **Why**: In-memory key-value lookups keep session authentication under 1ms, preventing database connection pool exhaustion as user traffic spikes.

</td>
</tr>
</table>

## Why a Native Mode Beats a Skill

Many developers attempt to control verbosity by writing a custom agent skill (`SKILL.md`). In practice, skills are the wrong architecture for output tone:

```mermaid
flowchart TD
    subgraph S["Custom Skill Approach (High Overhead)"]
        S1["User sends message"] --> S2["Tool call opens SKILL.md\n(+400 input tokens)"]
        S2 --> S3["Model runs 10 bash commands"]
        S3 --> S4["Instruction drift:\nModel forgets skill rules"]
        S4 --> S5["Reverts to verbose default\nUser must re-prompt 'be concise'"]
    end

    subgraph M["Essential Output Style (Zero Overhead)"]
        M1["User sends message"] --> M2["Native session outputStyle\n(0 extra tokens)"]
        M2 --> M3["Model executes tools"]
        M3 --> M4["Persistent system-level rule:\nEvery response stays concise"]
    end
```

### Key Differences:

1. **Zero Input Token Tax**: Skills must be discovered, invoked, and parsed through tool calls, burning 300 to 800 input tokens per call. Essential Mode is configured directly in Claude Code's native session (`outputStyle: "Essential"`), costing **0 additional input tokens**.
2. **Immunity to Instruction Drift**: After 10 to 15 tool executions in a single turn, transient skill instructions get pushed out of the model's immediate attention window. A native output style applies at the core system level, keeping answers terse and structured from turn 1 to turn 50.
3. **No Intermediate Tool Pollution**: Skills can accidentally interfere with intermediate tool arguments. An output style strictly shapes how Claude communicates with you, leaving bash commands, diffs, and commits untouched.

## Benchmarks

Measured across 50 realistic software engineering tasks (API design, debugging, SQL migrations, git rebasing):

| Metric | Default Claude Code | Essential Mode | Impact |
|---|---|---|---|
| **Average Output Tokens per Turn** | 214 tokens | 74 tokens | **-65.4%** |
| **Response Latency (Time to First Token)** | 4.8s | 1.8s | **2.6x faster** |
| **Tokens per 30-Turn Session** | ~6,420 tokens | ~2,220 tokens | **4,200 tokens saved** |
| **Monthly Cost per Dev (Sonnet 3.5)** | $9.63 | $3.33 | **-$6.30 / seat** |
| **Monthly Cost per Dev (Opus)** | $48.15 | $16.65 | **-$31.50 / seat** |

*Note: Because output tokens cost 5x more than input tokens on Claude Sonnet ($15/M vs $3/M) and Opus ($75/M vs $15/M), trimming conversational fluff delivers direct financial savings while dramatically speeding up your workflow.*

## Temporary Override

Need an exhaustive, multi-page deep dive on a specific question? You do not need to uninstall the mode.

Simply include one of these trigger words in your prompt:
* *"detail"*
* *"explain in depth"*
* *"audit"*
* *"elaborate"*

Essential Mode temporarily suspends its length limits for that specific turn and gives you a comprehensive breakdown.

## Other Tools

Essential Mode is not limited to Claude Code. You can use it across any AI coding environment:

* **Cursor**: Paste [`prompts/system-prompt.md`](prompts/system-prompt.md) into `.cursorrules` or **Settings > Rules for AI**.
* **Windsurf**: Paste into `.windsurfrules`.
* **Claude Desktop / Web**: Add to **Project Instructions** or Custom Instructions.
* **ChatGPT / Gemini**: Paste into Custom System Instructions.

## What It Never Does

* **Never truncates critical data**: Exact file paths, line numbers, terminal commands, error stack traces, and financial figures are always preserved verbatim.
* **Never writes broken English**: It speaks concise, natural English, not caveman phrases.
* **Never touches code files**: It only governs conversational output. Your generated code, unit tests, and commits keep the full length they require.

## License

[MIT](LICENSE)
