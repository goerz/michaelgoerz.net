---
Title: Tags
Jinja: True
Section: Notes
Template: page.html
----


<div class="collapse-list">
    {%- for tag in tags|sort %}
    {% set notes  = tags[tag] %}
    <div class="card collapse-card">
        <div class="card-header">
            <h2 class="card-title">
                <a data-bs-toggle="collapse" href="#collapse-{{tag.slug}}" role="button" aria-expanded="false" aria-controls="collapse-{{tag.slug}}"><span class="collapse-card-label">{{ tag }}</span><span class="count-badge">{{ notes|count }}</span><i class="fa-solid fa-chevron-down collapse-chevron" aria-hidden="true"></i></a>
            </h2>
        </div>
        <div id="collapse-{{tag.slug}}" class="collapse">
            <div class="card-body">
                <ul class="note-list">
                {% for note in notes|sort(attribute='date',reverse=True) %}
                <li>
                <time datetime="{{ note.date.isoformat() }}">{{ note.date.strftime('%Y-%m-%d') }}</time>
                {% if note.exturl %}
                <span><a href="{{ note.exturl }}">{{ note.title }}</a> <i class="fa-solid fa-arrow-up-right-from-square external-icon" title="External link"></i></span>
                {% else %}
                <a href="{{ SITEURL }}/{{ note.url }}">{{ note.title }}</a>
                {% endif %}
                </li>
                {% endfor %}
                </ul>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
