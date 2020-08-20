{% load i18n %}
{% load static %}
{% trans '更新日誌' as update_log %}
<div style="height:100%;">
    <div id="vue_sidebar" :style="background_color" style="height:100%;">
        <ul style="padding-top:20px; padding-left:20px">
            <sidebar_cell
                :cell_title = "{
                    content: 'Home',
                    is_chinese: false,
                    highlight: 'Home' === now_page,
                    url: '{% url 'home' %}',
                }"
            ></sidebar_cell>
            <sidebar_cell
                :cell_title = "{
                    content: 'DPView',
                    is_chinese: false,
                    highlight: 'DPView' === now_page,
                    url: '{% url 'DPView:home' %}',
                }"
            ></sidebar_cell>
            <sidebar_cell
                :cell_title = "{
                    content: 'k-Anonymity',
                    is_chinese: false,
                    highlight: 't_Closeness' === now_page,
                    url: '{% url 't_Closeness:home' %}',
                }"
            ></sidebar_cell>            
            <sidebar_cell v-if = "release_display"
                :cell_title = "{
                    content: 'k-Anonymity',
                    is_chinese: false,
                    highlight: 'k_Anonymity' === now_page,
                    url: '{% url 'k_Anonymity:home' %}',
                }"
            ></sidebar_cell>
            <sidebar_cell v-if = "release_display"
                :cell_title = "{
                    content: 'l-Diversity',
                    is_chinese: false,
                    highlight: 'l_Diversity' === now_page,
                    url: '{% url 'l_Diversity:home' %}',
                }"
            ></sidebar_cell>
            <sidebar_cell
                :cell_title = "{
                    content: '{{ update_log }}',
                    is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                    highlight: 'update_log' === now_page,
                    url: '{% url 'update_log' %}',
                }"
            ></sidebar_cell>
            {% if user.is_authenticated %}
                <sidebar_cell
                    :cell_title = "{
                        content: '{% trans '帳號管理' %}',
                        is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                        highlight: false,
                    }"
                    :cell_links = "[{
                        display: {
                            content: '{% trans '更改密碼' %}',
                            is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                            highlight: false,
                        },
                        event: 'change_password()',
                    },{
                        display: {
                            content: '{% trans '登出' %}',
                            is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                            highlight: false,
                        },
                        event: 'location.href=\'{% url 'logout' %}\'',
                    },{
                        display: {
                            content: '{% trans '刪除帳號' %}',
                            is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                            highlight: false,
                        },
                        event: 'delete_account()',
                    },]"
                ></sidebar_cell>
            {% endif %}            
            <div>
                <form id="i18n" action="{% url 'set_language' %}" method="post">
                    {% csrf_token %}
                    <input name="next" type="hidden" value="{{ request.get_full_path|remove_language_code }}"/>
                    <input name="language" type="hidden" value="{{ LANGUAGE_CODE }}" />
                    <sidebar_cell
                        :cell_title = "{
                            content: '{% trans '語言切換' %}',
                            is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                            highlight: false,
                        }"
                        :cell_links = "[
                            {% for code, name in LANGUAGES %}
                                {
                                    display: {
                                        content: '{{ name }}',
                                        is_chinese: '{{ code }}' === 'zh-hant',
                                        highlight: '{{ code }}' === '{{ LANGUAGE_CODE }}',
                                    },
                                    event: 'switch_language(\'{{ code }}\')',
                                },
                            {% endfor %}
                        ]"
                    ></sidebar_cell>
                </form>
            </div>
        </ul>
    </div>
</div>

<script>
    vue_sidebar = new Vue({
        delimiters: ['[[', ']]'],
        el: '#vue_sidebar',
        data: {            
            background_color: "background-color:#FFFFFF",
            release_display: false,
            now_page: 'Home',
        },
        components: {
            'sidebar_cell': {
                delimiters: ['[[', ']]'],
                props: ['cell_title', 'cell_links'],
                template: '\
                    <div class="top_gray_line">\
                        <div class="navbar-brand" style="width:100%; font-size:22px">\
                            <a :href="click_style()" :style=title_color() :class="font_class(cell_title.is_chinese)">[[ cell_title.content ]]</a>\
                            <ul v-if="cell_links" class="top_gray_line" style="padding-left:15px; width:100%;">\
                                <ul v-for="cell_link in cell_links" :key=cell_link.display.content>\
                                    <a href="javascript:void(0)" :onclick=cell_link.event :style=context_color(cell_link) :class="font_class(cell_link.display.is_chinese)">[[ cell_link.display.content ]]</a>\
                                </ul>\
                            </ul>\
                        </div>\
                    </div>\
                ',
                methods: {
                    click_style: function() {
                        if (this.cell_title.url) {
                            return this.cell_title.url;
                        }
                    },
                    font_class: function (is_chinese) {
                        if (is_chinese) {
                            return 'chinese_font';
                        } else {
                            return 'english_font';
                        }
                    },
                    title_color: function() {
                        if (this.cell_title.highlight) {
                            return 'color:#921AFF;';
                        }
                        return 'color:#000000';
                    },
                    context_color: function(cell_link) {
                        if (cell_link.display.highlight) {
                            return 'color:#921AFF;';
                        }
                        return 'color:#292421';
                    },
                },
            },
        },
    });
</script>

<script>
    function switch_language(language) {
        $("[name='language']").val(language);
        $('#i18n').submit();
    }
    
    function delete_account() {
        var answer = prompt("{% trans '帳號即將刪除，刪除後資料無法回復，如確定要刪除請輸入密碼' %}", '');
        var url = "{% url 'password_check' %}";
        var data = {
            'password' : answer,
        };
        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            success: function () {
                window.location = "{% url 'delete_account' %}";
            },
            error: function (xhr, ajaxOptions, thrownError) {
                var jsonObj = JSON.parse(xhr.responseText);
                danger_alert(jsonObj.message);
            }
        });
    }
    
    function change_password() {
        var answer = prompt("{% trans '請輸入原本的密碼，以繼續進行密碼更改' %}", '');
        var url = "{% url 'password_check' %}";
        var data = {
            'password' : answer,
        };
        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            success: function () {
                window.location = "{% url 'change_password' %}";
            },
            error: function (xhr, ajaxOptions, thrownError) {
                var jsonObj = JSON.parse(xhr.responseText);
                danger_alert(jsonObj.message);
            }
        });
    }
</script>