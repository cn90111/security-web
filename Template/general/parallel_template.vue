{% extends "base.vue" %}
{% load i18n %}
{% block title %}parallel template{% endblock title %}
{% block context_area %}
    <div id="hint_area">
        {% block hint_area %}{% endblock hint_area %}
    </div>
    <div style="width:100%;">
        <form id="parameter_form">
            {% csrf_token %}
            <div class="form-row">
                {% block left_container %}
                    <div class="form-group col-md-6">
                    </div>
                {% endblock left_container %}
                {% block right_container %}
                    <div class="form-group col-md-6">
                    </div>
                {% endblock right_container %}
            </div>
            {% block bottom_container %}
            {% endblock bottom_container %}
            <div class="form-row">
                {% block button %}
                    <div class="form-group col-md-2">
                        <button id="execute" type="button" class="btn btn-primary" style="width:100%">{% trans '繼續執行' %}</button>
                    </div>
                {% endblock button %}
            </div>
        </form>
    </div>
{% endblock context_area %}

{% block script_area %}
{% endblock script_area %}