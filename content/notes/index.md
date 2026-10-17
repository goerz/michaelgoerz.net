---
Title: Notes
Jinja: True
Template: page.html
----

<div class="notes-index">
<nav class="pill-nav" aria-label="Browse notes">
<a class="pill" href="{{ SITEURL }}/{{ CATEGORIES_URL | default('categories.html') }}"><i class="fa-regular fa-folder"></i> Categories</a>
<a class="pill" href="{{ SITEURL }}/{{ TAGS_URL | default('tags.html') }}"><i class="fa-solid fa-tags"></i> Tags</a>
</nav>
{% for year, notes_in_year in notes|groupby('date.year')|reverse %}
<section class="note-year">
<h2>{{ year }}</h2>
<ul class="note-list">
{% for note in notes_in_year|sort(attribute='date',reverse=True) %}
<li>
<time datetime="{{ note.date.isoformat() }}">{{ note.date.strftime('%b') }} {{ note.date.day }}</time>
{% if note.exturl %}
<span><a href="{{ note.exturl }}">{{ note.title }}</a> <i class="fa-solid fa-arrow-up-right-from-square external-icon" title="External link"></i></span>
{% else %}
<a href="{{ SITEURL }}/{{ note.url }}">{{ note.title }}</a>
{% endif %}
</li>
{% endfor %}
</ul>
</section>
{% endfor %}
</div>
