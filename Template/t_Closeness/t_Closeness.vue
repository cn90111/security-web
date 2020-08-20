{% extends "general/function.vue" %}
{% load i18n %}
{% block title %}k-Anonymity {{ block.super }}{% endblock title %}

{% block hint_area %}
    <function_cell
        :function_object = "{
            name: {
                content: '{% trans '說明' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '1：「K」 ── 去識別化後，在任意查詢條件下，至少會同時查到K筆資料' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        {% if false %}
            <cell_introduction
                :introduction = "{
                    content: '{% trans '2：「T」 ── 去識別化後，K筆資料中的主要內容(最後一欄)的分布，將與整個資料集的分布相差在T以內' %}',
                    is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                }"
            ></cell_introduction>
            <cell_introduction
                :introduction = "{
                    content: '{% trans '3：執行速度較快，若可用性過低可藉由調高T來提升可用性' %}',
                    is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                }"
            ></cell_introduction>
        {% endif %}
    </function_cell>
{% endblock hint_area %}
{% block script_area %}
    {{ block.super }}
    <script>
        title_area.title.content = "k-Anonymity";
        title_area.title.is_chinese = false;
    </script>
{% endblock script_area %}