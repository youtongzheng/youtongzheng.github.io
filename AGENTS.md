# Agent instructions for this site

Jekyll site (academicpages template), built by GitHub Pages from `master`.

## Purpose (decides what goes on the site)

The site promotes Youtong Zheng and the WEAVE Lab and attracts students, postdocs, and collaborators. Keep it simple and inviting. Add what helps a visitor want to join or collaborate; leave out detail that only matters for a dossier (enrollments, committee lists, evaluation scores, pending or declined grants, every conference abstract).

## Fixed framework (do not redesign)

The layout, menu, and page structure are settled (as of 2026-11-14): Home, Group, Publications, Teaching & Mentoring, About the PI, News, Live Weather, on the academicpages theme. Future requests are small updates: add or correct information, adjust wording, fix a section. Do not change the theme, the menu structure, or the overall style unless Y. Zheng explicitly asks for a redesign.

The home page (agreed with Y. Zheng on 2026-11-15) has: one short paragraph (clouds, storms, extreme weather; right answer for the right physical reason so predictions and projections can be trusted; weaving evidence; physics or knob-tuning becomes physics or shortcut with AI agents), a three-item topic list (storms in km-scale models; ML and AI agents; clouds, aerosols, boundary layer), one recognition sentence (three top awards, no details; DOE national-lab ties and student fellowships/internships), and one Joining us paragraph (self-motivated; no generic or AI-generated emails; TA speaking requirement). Do not name specific funders or projects in the research text. Change this text only after agreeing the wording in conversation.

## Where content lives

| Request | File |
| --- | --- |
| Home: lab intro, research, Join us, recent news | `_pages/about.md` |
| Group members (photos in `images/group/`), alumni | `_pages/group.md` |
| Papers | `_data/publications.yml` (newest first) |
| Manuscripts in review | `_data/manuscripts.yml` |
| Courses, mentoring (images in `images/teaching/`) | `_pages/teaching.html` |
| About the PI: education, positions, awards, service, media | `_pages/cv.md` (URL /about-pi/) |
| All news | `_pages/news.md` (keep the latest ~7 also on the home page) |
| Live weather | `_pages/weather.md` |
| Sidebar profile, menu | `_config.yml` (`author:`), `_data/navigation.yml` |

## Rules

- Facts come from `Portfolio/` in Y. Zheng's Obsidian vault; citation format and CV wording follow the latest CV (Applications/University of Michigan CLaSP 2026/CV Youtong Zheng.md): `<b>Y. Zheng</b>`; mentored group members underlined with their marker inside, e.g. `<u>Bhattarai, A.†</u>` (graduate student) or `<u>Sarkar, M.‡</u>` (postdoc); no corresponding-author marks. No paper counts or summary sentence on the Publications page.
- New paper: add it at the top of `_data/publications.yml` (next `P##` ID from `Portfolio/Publications.md`) and remove it from `_data/manuscripts.yml`.
- Do not use pronouns for people unless they are stated. Write in English.
- Push to `master` only with Y. Zheng's approval; Pages rebuilds in about a minute. Check the changed page live afterwards.
