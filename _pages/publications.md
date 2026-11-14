---
title: "Publications"
permalink: /publications/
author_profile: true
---

<style>
.pubs { padding-left: 2.6em; }
.pubs li { margin-bottom: 0.8em; font-size: 0.92em; line-height: 1.45; }
</style>

{% assign pubs = site.data.publications %}
{{ pubs.size }} peer-reviewed papers. Also see [Google Scholar](https://scholar.google.com/citations?user=xTpHltEAAAAJ).

\* corresponding author; <u>underlined</u>: student or postdoc supervised by Youtong Zheng.

{% assign groups = pubs | group_by: "year" %}
{% assign count = pubs.size %}
{% for g in groups %}
<h2 id="y{{ g.name }}">{{ g.name }}</h2>
<ol class="pubs" start="{{ count }}" reversed>
{%- for p in g.items -%}
  {%- assign a = p.authors | replace: "Zheng, Y.", "<b>Zheng, Y.</b>" | replace: "Y. Zheng", "<b>Y. Zheng</b>" -%}
  {%- assign last = p.title | slice: -1 -%}
  <li>{{ a }} ({{ p.year }}). {{ p.title }}{% unless last == "?" %}.{% endunless %} <i>{{ p.journal }}</i>{% if p.details %}, {{ p.details }}{% endif %}.{% if p.doi %} <a href="https://doi.org/{{ p.doi }}">doi:{{ p.doi }}</a>{% endif %}</li>
{% endfor %}
</ol>
{% assign count = count | minus: g.items.size %}
{% endfor %}
