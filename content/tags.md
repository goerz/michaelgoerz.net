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
            <h4 class="card-title">
                <a data-bs-toggle="collapse" href="#collapse-{{tag.slug}}" role="button" aria-expanded="false" aria-controls="collapse-{{tag.slug}}"><span class="collapse-card-label">{{ tag }}</span><span class="badge rounded-pill text-bg-secondary">{{ notes|count }}</span></a>
            </h4>
        </div>
        <div id="collapse-{{tag.slug}}" class="collapse">
            <div class="card-body">
                {% for note in notes|sort(attribute='date',reverse=True) %}
                <p><span class="categories-timestamp"><time datetime="{{ note.date.isoformat() }}"> {{ note.date.date() }}</time></span>
                {% if note.exturl %}
                <i class="fa-solid fa-arrow-up-right-from-square"></i> <a href="{{ note.exturl }}">{{ note.title }}</a>
                {% else %}
                <a href="{{ SITEURL }}/{{ note.url }}">{{ note.title }}</a>
                {% endif %}
                {% endfor %}
            </div>
        </div>
    </div>
    {% endfor %}
</div>
