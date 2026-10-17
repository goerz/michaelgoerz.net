---
Title: Notes
Jinja: True
Template: page.html
----

<div id="categories_tags_link">
  <a href="{{ SITEURL }}/{{ CATEGORIES_URL | default('categories.html') }}"><i class="fa-solid fa-box-archive fa-lg"></i><span class="icon-label">Categories</span></a>
  &nbsp; &nbsp; &nbsp;
  <a href="{{ SITEURL }}/{{ TAGS_URL | default('tags.html') }}"><i class="fa-solid fa-tags fa-lg"></i><span class="icon-label">Tags</span></a>
</div>

{% for note in notes|sort(attribute='date',reverse=True) %}
  <p><span class="categories-timestamp"><time datetime="{{ note.date.isoformat() }}">{{ note.date.date() }}</time></span>
  &nbsp;
  {% if note.exturl %}
  <i class="fa-solid fa-arrow-up-right-from-square"></i> <a href="{{ note.exturl }}">{{ note.title }}</a>
  {% else %}
  <a href="{{ SITEURL }}/{{ note.url }}">{{ note.title }}</a>
  {% endif %}
  </p>
{% endfor %}
