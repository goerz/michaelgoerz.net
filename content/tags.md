---
Title: Tags
Jinja: True
Section: Notes
Template: page.html
----


<div class="panel-group" id="accordion">
    {%- for tag in tags|sort %}
    {% set notes  = tags[tag] %}
    <div class="panel panel-default">
        <div class="panel-heading">
            <h4 class="panel-title">
                <a data-toggle="collapse" data-parent="#accordion" href="#collapse-{{tag.slug}}">{{ tag }} <span class="badge pull-right">{{ notes|count }}</span></a>
            </h4>
        </div>
        <div id="collapse-{{tag.slug}}" class="panel-collapse collapse">
            <div class="panel-body">
                {% for note in notes|sort(attribute='date',reverse=True) %}
                <p><span class="categories-timestamp"><time datetime="{{ note.date.isoformat() }}"> {{ note.date.date() }}</time></span>
                {% if note.exturl %}
                <i class="fa fa-external-link"></i> <a href="{{ note.exturl }}">{{ note.title }}</a>
                {% else %}
                <a href="{{ SITEURL }}/{{ note.url }}">{{ note.title }}</a>
                {% endif %}
                {% endfor %}
            </div>
        </div>
    </div>
    {% endfor %}
</div>
