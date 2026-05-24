# Resume Editor Skill

Write tailored resume versions for Joseph Platta using source material from this Obsidian vault.

## Step 1 — Read Source Material

Before doing anything else, read these vault files:

**Always read:**
- `Notes/resume/WallStreetQuants Resume Writing Notes.md` — quant-specific guidelines, section ordering, narrative
- `Notes/Resume Notes.md` — comprehensive experience narratives, metrics, value propositions
- `Notes/resume/README.md` — index of available resume files

**Read based on target role:**
- Quant/finance role → `Notes/Quant Resume Template.md`
- ML / research role → `Notes/Machine Learning Engineer Resume.md`, `Notes/Research Engineer Resume.md`
- General SWE / product → `Notes/General Resume.md`
- LeadersAtlas detail → `Notes/LeadersAtlas Resume Experience.md`
- Feedback and anti-patterns → `Notes/Resume Feedback.md`

## Step 2 — Ask the User

Before drafting, ask:
1. **Target role type** — quant research, ML engineer, backend SWE, product engineer, or other?
2. **Company or job description** — paste the JD or describe the company (optional but helpful)
3. **Emphasis** — any sections, roles, or skills to highlight or de-emphasize?
4. **Output format** — markdown draft to copy into a doc, or annotated notes on an existing version?

## Step 3 — Draft the Resume

Apply the following principles from the vault's own notes:

### Structure & Length
- 1 page only
- Front-load for first-impression bias — strongest credentials appear first
- Section order by role:
  - **Quant**: Education & Awards → Experience (Independent Quant Research first) → Quant Projects → Skills
  - **ML/Research**: Experience → Education → Projects → Skills
  - **SWE/Product**: Experience → Education → Skills

### Experience Framing
- Precedence: Quant > Applied Math Research > Data Science/ML > Software Engineering > Everything else
- Reframe titles to be role-relevant (e.g. sabbatical → "Independent Quant Research", Procore → "Senior Software Engineer")
- Write quant-relevant bullets: data cleaning, statistical analysis, backtesting, research, large codebase maintenance
- Use action-result format: strong verb + what you did + quantified outcome
- Only use metrics that appear in the vault notes — do not invent numbers

### Formatting
- Bold key achievements throughout to guide the eye
- Skills & Interests always at the bottom
- No industry jargon from non-target domains — explain in plain language

### Narrative
> An engineer and ML grad who has been building and trading systematic options strategies, and is now formalizing that into quant research.

Adapt this narrative to the target role when writing the summary or framing experience.

## Step 4 — Output

Produce a clean markdown resume draft with all sections clearly headed. The user can copy this into a `.docx`. If the user asks for revision, apply targeted edits — do not regenerate the whole resume unless asked.
