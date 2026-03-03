# Condensed Agent Profiles

Condensed profiles are stripped-down versions of each agent's full identity document, optimized for local model context windows.

## Location

Each condensed profile lives alongside its full version in the agent's `Identity/` directory:
- Full: `{Agent}/Identity/{agent}-identity.md` (~2,000+ words)
- Condensed: `{Agent}/Identity/{agent}-local.md` (~400-500 words, <2K tokens)

## What's Preserved

- Core role and question
- Thinking style (2-3 sentences)
- Communication style
- Risk orientation
- Key anti-patterns
- Deliberation protocol behavior
- Personality anchors (names only, no descriptions)

## What's Stripped

- Detailed personality inspiration descriptions
- Extended examples
- Historical context and rationale
- Big Five personality breakdown
- Verbose formatting

## Generating Condensed Profiles

Condensed profiles are manually written, not auto-generated. Each one is crafted to ensure an agent running with only the condensed profile behaves recognizably like one running with the full document.

When updating a full identity document, review the condensed version for consistency.

## Token Budget Target

- Maximum: 2,000 tokens
- Ideal: 1,000-1,500 tokens
- Minimum viable: 500 tokens (emergency compression)
