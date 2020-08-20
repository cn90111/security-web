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
                content: '{% trans '1：去識別化後的檔案可用性高，但執行速度較慢，可先執行 t-Closeness 測試是否符合需求' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '2：「K」 ── 去識別化後，在任意查詢條件下，至少會同時查到K筆資料' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
    </function_cell>
{% endblock hint_area %}

{% block script_area %}
    {{ block.super }}
    <script>
        title_area.title.content = "k-Anonymity";
        title_area.title.is_chinese = false;
    </script>
{% endblock script_area %}