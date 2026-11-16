---
title: "Publications"
permalink: /publications/
author_profile: true
---

<style>
.pubs { padding-left: 2.6em; }
.pubs li { margin-bottom: 0.8em; font-size: 0.92em; line-height: 1.45; }
.status { color: #b5172f; }
</style>

{% assign pubs = site.data.publications %}
**Bold**: Youtong Zheng · <u>Underlined</u>: group member († graduate student, ‡ postdoctoral researcher mentored by Youtong)

<h2 id="in-review">Manuscripts in review</h2>
<ul class="pubs">
{%- for m in site.data.manuscripts -%}
  <li>{{ m.authors }}. {{ m.title }}. <i>{{ m.journal }}</i>, <span class="status">{{ m.status }}</span>.</li>
{%- endfor -%}
</ul>

{% assign groups = pubs | group_by: "year" %}
{% assign count = pubs.size %}
{% for g in groups %}
<h2 id="y{{ g.name }}">{{ g.name }}</h2>
<ol class="pubs" start="{{ count }}" reversed>
{%- for p in g.items -%}
  {%- assign last = p.title | slice: -1 -%}
  <li>{{ p.authors }} ({{ p.year }}). {{ p.title }}{% unless last == "?" %}.{% endunless %} <i>{{ p.journal }}</i>{% if p.details %}, {{ p.details }}{% endif %}.{% if p.doi %} <a href="https://doi.org/{{ p.doi }}">doi:{{ p.doi }}</a>{% endif %}{% for l in p.links %} [<a href="{{ l.url }}">{{ l.label }}</a>]{% endfor %}</li>
{% endfor %}
</ol>
{% assign count = count | minus: g.items.size %}
{% endfor %}
