# Resume Editor Skill

Write tailored resume versions for Joseph Platta. **The WallStreetQuants (WSQ) methodology is the primary authority.** All structure, ordering, framing, and writing decisions follow the WSQ guidelines in `Notes/resume/WallStreetQuants Resume Writing Notes.md` unless the target role is explicitly non-quant.

## Step 1 — Read Source Material

Read these files before doing anything else:

**Always read (required):**
- `Notes/resume/WallStreetQuants Resume Writing Notes.md` — **primary authority on structure, section order, writing style, and narrative**
- `Notes/Resume Notes.md` — experience narratives, metrics, value propositions
- `Notes/resume/README.md` — index of available resume files

**Read based on target role:**
- Quant/finance → `Notes/Quant Resume Template.md`
- ML/research → `Notes/Machine Learning Engineer Resume.md`, `Notes/Research Engineer Resume.md`
- General SWE/product → `Notes/General Resume.md`
- LeadersAtlas detail → `Notes/LeadersAtlas Resume Experience.md`
- Feedback/anti-patterns → `Notes/Resume Feedback.md`

## Step 2 — Ask the User

Before drafting, ask:
1. **Target role type** — quant research, ML engineer, backend SWE, product engineer, or other?
2. **Company or job description** — paste the JD or describe it (optional but helpful)
3. **Emphasis** — any sections, roles, or skills to highlight or omit?
4. **Output format** — markdown draft, or annotated notes on an existing version?

## Step 3 — Draft the Resume

Follow the WSQ guidelines strictly. Key rules below are drawn directly from them.

### Narrative (WSQ)
> An engineer and ML grad who has been building and trading systematic options strategies, and is now formalizing that into quant research.

### Structure & Length (WSQ)
- **1 page. No exceptions.**
- Front-load for first-impression bias.
- **Preferred section order (quant):** Experience → Education → Awards → Quant Projects → Skills & Interests
  - Sabbatical = "Independent Quant Research" (first under Experience)
  - Then: Founding Engineer, Senior Software Engineer, Palmer, Teaching
- **Alternative order if education is the strongest credential:** Education & Awards → Experience → Quant Projects → Skills & Interests
- Skills & Interests always at the very bottom.

### Experience Precedence (WSQ)
Quant > Applied Math Research > Data Science / ML > Software Engineering > Everything else.
- Software engineering trumps traditional finance experience.
- Reframe titles to be quant-relevant:
  - Sabbatical → **Independent Quant Research**
  - Procore → **Senior Software Engineer**
  - LeadersAtlas → **Founding Engineer** or **Product Engineer**
  - Palmer → find a quant-adjacent framing
- Explain any firm that won't be recognized (LeadersAtlas, Palmer Consulting).
- Write quant-relevant bullets: data cleaning, statistical analysis, backtesting, large codebase maintenance, research.
- Emphasize results, use simple clear language, quantify where possible.

### Awards Section (WSQ)
Quant firms want a track record of excellence. Include:
- Department/school-wide awards (e.g. James H. Robb Memorial Award — highest GPA in major at Marquette)
- Math and STEM competitions
- Highly exceptional non-STEM awards
- Kaggle, quant competitions, research or grant awards
- Highlight "cringe" credentials like SATs if strong

### Quant Projects Section (WSQ)
- Call the section **"Quant Projects"**
- Quality over quantity: **1–3 projects maximum**
- First bullet of each project must state: type of strategy, universe/asset class, performance (backtest OK), holding period
- Use quant terminology throughout
- Include concrete metrics quants care about
- Can place quant projects under Professional Experience instead (consider for options strategies)

### Writing Style (WSQ)
- Less is more — avoid clutter, highlight only quant-relevant experience
- Show don't tell — prove skills by showing what you've done
- Titles and labels matter — people see them first
- **Bold** key achievements throughout to guide the eye
- No jargon from other industries — explain in plain language
- Okay to omit irrelevant experience entirely

### Skills & Interests (WSQ — always at bottom)
Skills: Python, NumPy, Pandas, SQL, backtesting/quant research, deep learning/PyTorch, ML/scikit-learn, Linux, plus others from dev resume.
Interests: marathoning, philosophy, Magic: The Gathering.

## Step 4 — Output

Produce a clean markdown resume draft with all sections clearly headed. The user can copy this into a `.docx`. On revision, make targeted edits — do not regenerate the whole resume unless asked.
