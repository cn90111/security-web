{% extends "general/function.vue" %}
{% load i18n %}
{% block title %}l-Diversity {{ block.super }}{% endblock title %}
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
                content: '{% trans '1：執行速度較快，但去識別化後的檔案不一定具備可用性' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '2：「K」 ── 去識別化後，在任意查詢條件下，至少會同時查到K筆資料' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>        
        <cell_introduction
            :introduction = "{
                content: '{% trans '3：「L」 ── 去識別化後，K筆資料中，將至少有L筆資料將完全相同( 包含沒去識別化的最後一欄 )' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
    </function_cell>
{% endblock hint_area %}

{% block script_area %}
    {{ block.super }}
    <script>
        title_area.title.content = "l-Diversity";
        title_area.title.is_chinese = false;
    </script>
{% endblock script_area %}