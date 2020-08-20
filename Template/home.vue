{% extends "base.vue" %}
{% load i18n %}
{% block title %}Home{% endblock title %}

{% block context_area %}
{% trans '使用' as enter %}
    <function_cell v-if = "update_display"
        :function_object = "{
            name: {
                content: '{% trans '更新公告' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '說明： 將於 X/X X:X 時關閉伺服器進行系統更新，系統將會停止所有正在執行中的檔案，請您不要執行過大的檔案，以免被終止，預計於 X:X 時重新啟動伺服器，感謝您的使用' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
        <vue_button
            url = "{% url 'update_log' %}"
            :button_text = "{
                content: '{% trans '更新日誌' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></vue_button>
    </function_cell>
    
    <function_cell
        :function_object = "{
            name: {
                content: 'DPView: Differentially Private Synthetic Dataset Generation',
                is_chinese: false,
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '說明： 差分隱私適用於資料筆數較大的資料集，建議至少含有一萬筆紀錄且維度也會受資料筆數影響不能太高。' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
        <vue_button
            url = "{% url 'DPView:home' %}"
            :button_text = "{
                content: '{{ enter }}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></vue_button>
    </function_cell>
    
    <function_cell
        :function_object = "{
            name: {
                content: 'k-Anonymity for De-Identifying Dataset',
                is_chinese: false,
            },
        }"
    >
        <vue_button
            url = "{% url 't_Closeness:home' %}"
            :button_text = "{
                content: '{{ enter }}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></vue_button>
    </function_cell>
    
    <function_cell v-if = "release_display"
        :function_object = "{
            name: {
                content: 'k-Anonymity for De-Identifying Dataset',
                is_chinese: false,
            },
        }"
    >
        <vue_button
            url = "{% url 'k_Anonymity:home' %}"
            :button_text = "{
                content: '{{ enter }}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></vue_button>
    </function_cell>
    
    <function_cell v-if = "release_display"
        :function_object = "{
            name: {
                content: 'l-Diversity for De-Identifying Dataset',
                is_chinese: false,
            },
        }"
    >
        <vue_button
            url = "{% url 'l_Diversity:home' %}"
            :button_text = "{
                content: '{{ enter }}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></vue_button>
    </function_cell>
{% endblock context_area %}

{% block footer_area %}
    {% include 'footer.html' %}
{% endblock footer_area %}

{% block script_area %}
    <script>
        vue_sidebar.now_page = 'Home';
        title_area.title.content = "{% trans '歡迎使用本系統' %}";
        title_area.title.is_chinese = '{{ LANGUAGE_CODE }}' === 'zh-hant';
        title_area.introduction.content = "{% trans '可於左方導覽列或下方區塊選擇您要使用的去識別化方法' %}";
        title_area.introduction.is_chinese = '{{ LANGUAGE_CODE }}' === 'zh-hant';        
    </script>
    
    <script>
        $(function () {
            var url = "{% url 'check_file_status' %}"
            $.getJSON(url, function (request) {
                if (request == null) {
                    var url = "{% url 'initialize' %}"
                    $.get(url);
                } else if (request.finish == true) {
                    next = true
                    while (next) {
                        if (confirm("{% trans '檔案去識別化完成，是否查看執行結果?' %}")) {
                            next = false
                            window.location = request.url;
                        } else {
                            if (confirm("{% trans '確定執行新的去識別化嗎?先前的執行結果將不會保留' %}")) {
                                next = false
                                $.get("{% url 'initialize' %}");
                            }
                        }
                    }
                } else if (request.finish == false) {
                    next = true
                    while (next) {
                        if (confirm("{% trans '檔案執行中，是否查看執行進度?' %}")) {
                            next = false
                            window.location = request.url;
                        } else {
                            if (confirm("{% trans '確定執行新的去識別化嗎?先前的執行進度將不會保留' %}")) {
                                next = false
                                $.get(request.break_url);
                                $.get("{% url 'initialize' %}");
                            }
                        }
                    }
                } else {
                    alert("{% trans 'home.html finish不符合預期，請通知開發人員，finish = ' %}"+request.finish);
                }
            })
        })
    </script>
{% endblock script_area %}