{% extends "general/function_home.vue" %}
{% load i18n %}
{% block title %}k-Anonymity{% endblock title %}

{% block hint_area %}
    <function_cell
        :function_object = "{
            name: {
                content: '{% trans '注意事項' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '1：文件格式( 資料筆數不可超過200筆，資料欄位不可超過4欄 )' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '2：文件大小( 檔案不可大於 1 MB )' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '3：文件內容( 請先刪除如姓名、ID等極具識別能力的欄位 )' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '4：文件內容( 請將要公布的主要內容放在最後一欄，以免對其進行去識別化，例如薪資表中的薪水欄位 )' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '5：檔案請另存新檔為CSV檔(.csv)' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
    </function_cell>
{% endblock hint_area %}

{% block script_area %}
    {{ block.super }}
    <script>
        vue_sidebar.now_page = 'k-Anonymity';
        title_area.title.content = "k-Anonymity";
        title_area.title.is_chinese = false;        
    </script>
{% endblock script_area %}