# Agent instructions for this site

Jekyll site (academicpages template), built by GitHub Pages from `master`.

## Purpose (decides what goes on the site)

The site promotes Youtong Zheng and the WEAVE Lab and attracts students, postdocs, and collaborators. Keep it simple and inviting. Add what helps a visitor want to join or collaborate; leave out detail that only matters for a dossier (enrollments, committee lists, evaluation scores, pending or declined grants, every conference abstract).

## Where content lives

| Request | File |
| --- | --- |
| Home: lab intro, research, Join us, recent news | `_pages/about.md` |
| Group members (photos in `images/group/`), alumni | `_pages/group.md` |
| Papers | `_data/publications.yml` (newest first) |
| Manuscripts in review | `_data/manuscripts.yml` |
| Courses, mentoring (images in `images/teaching/`) | `_pages/teaching.html` |
| Education, positions, awards, service, media | `_pages/cv.md` |
| All news | `_pages/news.md` (keep the latest ~7 also on the home page) |
| Live weather | `_pages/weather.md` |
| Sidebar profile, menu | `_config.yml` (`author:`), `_data/navigation.yml` |

## Rules

- Facts come from `Portfolio/` in Y. Zheng's Obsidian vault; citation format and CV wording follow the latest CV (Applications/University of Michigan CLaSP 2026/CV Youtong Zheng.md): `<b>Y. Zheng</b>`, `†` after a mentored graduate student, `‡` after a mentored postdoc, no corresponding-author marks.
- New paper: add it at the top of `_data/publications.yml` (next `P##` ID from `Portfolio/Publications.md`) and remove it from `_data/manuscripts.yml`.
- Do not use pronouns for people unless they are stated. Write in English.
- Push to `master` only with Y. Zheng's approval; Pages rebuilds in about a minute. Check the changed page live afterwards.
