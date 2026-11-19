# Agent instructions for this site

Jekyll site (academicpages template), built by GitHub Pages from `master`.

## Purpose (decides what goes on the site)

The site promotes Youtong Zheng and the WEAVE Lab and attracts students, postdocs, and collaborators. Keep it simple and inviting. Add what helps a visitor want to join or collaborate; leave out detail that only matters for a dossier (enrollments, committee lists, evaluation scores, pending or declined grants, every conference abstract).

## Fixed framework (do not redesign)

The layout, menu, and page structure are settled (as of 2026-11-14): Home, Group, Publications, Teaching & Mentoring, About the PI, Lab Handbook, Live Weather, on the academicpages theme. News is an archive page (/news/) reached from the home page's "All news" link, not from the menu (changed at Y. Zheng's request, 2026-11-19). Future requests are small updates: add or correct information, adjust wording, fix a section. Do not change the theme, the menu structure, or the overall style unless Y. Zheng explicitly asks for a redesign.

The home page (agreed with Y. Zheng on 2026-11-15) has: one short paragraph (clouds, storms, extreme weather; right answer for the right physical reason so predictions and projections can be trusted; weaving evidence; physics or knob-tuning becomes physics or shortcut with AI agents), a three-item topic list (storms in km-scale models; ML and AI agents; clouds, aerosols, boundary layer), one recognition sentence (three top awards, no details; DOE national-lab ties and student fellowships/internships), and one Joining us paragraph (self-motivated; no generic or AI-generated emails; TA speaking requirement). Do not name specific funders or projects in the research text. Change this text only after agreeing the wording in conversation.

## Where content lives

| Request | File |
| --- | --- |
| Home: lab intro, research, Join us, recent news | `_pages/about.md` |
| Group members (photos in `images/group/`), alumni | `_pages/group.md` |
| Papers | `_data/publications.yml` (newest first) |
| Manuscripts in review | `_data/manuscripts.yml` |
| Courses, mentoring (images in `images/teaching/`) | `_pages/teaching.html` |
| AI Agent Day sessions (latest shown on Teaching & Mentoring; all on /ai-agent-day/) | `_data/agent_day.yml` (newest first) |
| About the PI: education, positions, awards, service, media | `_pages/cv.md` (URL /about-pi/) |
| All news | `_data/news.yml` (newest first; the News page shows all, the home page the first 7 automatically) |
| Lab Handbook: expectations for group members (presentations; later writing, meetings). One `##` section per topic, figures in `images/handbook/` | `_pages/handbook.md` |
| Live weather | `_pages/weather.md` |
| Sidebar profile, menu | `_config.yml` (`author:`), `_data/navigation.yml` |

## Rules

- Facts come from `Portfolio/` in Y. Zheng's Obsidian vault; citation format and CV wording follow the latest CV (Applications/University of Michigan CLaSP 2026/CV Youtong Zheng.md): `<b>Y. Zheng</b>`; mentored group members underlined with their marker inside, e.g. `<u>Bhattarai, A.†</u>` (graduate student) or `<u>Sarkar, M.‡</u>` (postdoc); no corresponding-author marks. No paper counts or summary sentence on the Publications page.
- **Links are required in News (standing rule, 2026-11-16):** every news item must carry a link to a public page about it (event, program, award, paper, abstract, news story, or a page on this site). Search for one before adding the item; only if nothing public exists may an item go without a link, and say so in the commit message. Keep the same links on the Group page's Student awards.
- Add links wherever a public page exists: a news story or post for an award, the paper for a claim, and a paper's data or code (`links:` in `_data/publications.yml`, taken from the paper's Data Availability statement).
- New paper: add it at the top of `_data/publications.yml` (next `P##` ID from `Portfolio/Publications.md`) and remove it from `_data/manuscripts.yml`.
- Do not use pronouns for people unless they are stated. Write in English.
- Push to `master` only with Y. Zheng's approval, except AI Agent Day entries, which Y. Zheng asked (2026-11-15) to be added after each session. Pages rebuilds in about a minute. Check the changed page live afterwards.

## AI Agent Day updates

After each session is archived in the vault (Wiki/AI Agent Day), add a new entry at the top of `_data/agent_day.yml`: number, date, a short title, one line per talk, and a 3–6 sentence summary. Public text only: methods and lessons, no unpublished numbers or results, no vault links. The Teaching page then shows it as the latest session and the archive page lists all sessions automatically.
