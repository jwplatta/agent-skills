# Flashcard Writer Skill

Write Anki flashcards into Obsidian deck files using the vault's card templates.

## Templates

### Anki Basic Flashcard (`templates/Anki Basic Flashcard.md`)
```
START
Basic
<question>
Back:
<answer>
Tags: <space-separated tags>
END
```

### Anki Cloze Flashcard (`templates/Anki Cloze Flashcard.md`)
```
START
Cloze
<sentence with {{c1::cloze}} deletions>
Extra:
<optional additional context>
Tags: <space-separated tags>
END
```

### Anki Deck File (`templates/Anki Review.md`)
Every deck file must start with:
```
TARGET DECK: Obsidian::<DeckName>
FILE TAGS:
```
Then cards follow beneath.

## Card Design Principles

### 1. Atomic — one fact per card
Each card tests exactly one thing. If you find yourself writing "and" in the question, split it into two cards.

### 2. Active recall over recognition
Questions must require the reader to produce the answer from memory — never multiple choice, never "which of the following". Use open-ended cues: "What is...", "How do you...", "Prove that...", "Give an example of...".

### 3. Simple and minimal
- Questions: as short as possible while remaining unambiguous
- Answers: only what's needed to answer the question — no padding, no restating the question
- Strip surrounding context unless it's essential to the answer

### 4. Cloze deletions only for context-heavy facts
Use `Cloze` type only when the surrounding sentence provides necessary context — e.g. filling in a formula inside a definition, or completing a named rule. Use `Basic` for everything else.

Cloze example (good — context matters):
```
START
Cloze
The OLS beta formula is $b = {{c1::\rho_{x,y} \frac{\sigma_y}{\sigma_x}}}$
Extra:
Tags: regression
END
```

Basic example (good — straightforward Q&A):
```
START
Basic
What is the OLS formula for the slope coefficient $b$?
Back:
$$b = \rho_{x,y} \frac{\sigma_y}{\sigma_x} = \frac{Cov(x,y)}{Var(x)}$$
Tags: regression
END
```

### 5. No overlapping cards
One card per concept. Don't write a card asking "What is X?" and another asking "Define X" — they test the same thing. If a concept has multiple angles worth testing, make each angle genuinely distinct (e.g. formula vs. intuition vs. proof).

### 6. Optimize for long-term retention
Cards should be slightly effortful to answer — not trivially easy, not impossibly hard. Calibrate difficulty so that recalling the answer requires genuine retrieval effort. Avoid:
- Cards whose answer is obvious from the question wording
- Cards with excessively long answers (break them up)
- Cards that test rote recognition instead of understanding

## Math Formatting

Always use LaTeX for math. Surround all math with dollar signs:
- Inline: `$x^2 + y^2 = r^2$`
- Display (own line): `$$E(x) = \sum_{i=1}^n P(x_i) \cdot x_i$$`

Never write math as plain text (e.g. never write `E(x) = sum P(xi) * xi`).

## Back Field Formatting

Always put the answer on a new line after `Back:`. Never inline it on the same line.

**Correct:**
```
START
Basic
What is the variance formula?
Back:
$$Var(x) = E(x^2) - E(x)^2$$
Tags: statistics
END
```

**Incorrect:**
```
START
Basic
What is the variance formula?
Back: $$Var(x) = E(x^2) - E(x)^2$$
Tags: statistics
END
```

## Tags

Use lowercase hyphenated tags. Include at least one topic tag per card. Multiple tags are space-separated on the `Tags:` line.

Example: `Tags: fast-math probability bayes`
