{% extends "base.vue" %}
{% load i18n %}
{% block title %}execute page{% endblock title %}
{% block context_area %}
{% trans '小時' as hour %}
{% trans '分' as minute %}
{% trans '秒' as second %}
{% trans '目前進度：' as completion_rate %}
    {% block hint_area %}{% endblock hint_area %}
    <function_cell
        :function_object = "{
            name: {
                content: '{% trans '參數設定' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            },
        }"
    >
        <form id="parameter_form">
            {% csrf_token %}
            {% for field in form %}
                {% if forloop.counter0|divisibleby:3 %}
                    <div class="form-row">
                {% endif %}
                <div class="form-group col-md-4">
                    {{ field.label_tag }}<br>
                    {{ field }}
                    {% if field.help_text %}
                        <small style="color: grey">{{ field.help_text }}</small>
                    {% endif %}
                    {% for error in field.errors %}
                        <p style="color: red">{{ error }}</p>
                    {% endfor %}
                </div>
                {% if forloop.last or forloop.counter|divisibleby:3 %}
                    </div>
                {% endif %}
            {% endfor %}
            <div class="form-row justify-content-center">
                <div class="form-group col-md-2">
                    <vue_button
                        url = 'javascript:void(0)'
                        event = 'execute()'
                        :button_text = "{
                            content: '{% trans '執行' %}',
                            is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                        }"
                    ></vue_button>
                </div>
                <div class="form-group col-md-2">
                    <vue_button
                        url = '{% url 'home' %}'
                        :button_text = "{
                            content: '{% trans '返回主選單' %}',
                            is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
                        }"
                    ></vue_button>
                </div>
            </div>
            <div class="progress-div" style="width:90%; left:5%;">
                <label> {% trans '進度條' %} </label> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <span id="Check_Txt" style="color:red">{% trans '執行時間：' %}<span id="Check_i">0 {{ hour }} 0 {{ minute }} 0 {{ second }}</span>
                <div id="bar" class="progress progress-striped active">
                    <div class="progress-bar progress-bar-warning" aria-valuemax="100" aria-valuemin="0" aria-valuenow="0" style="width:0%">
                    </div>
                </div>
                <div class="progress-text progress-bar-striped active"  role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="min-width: 2em; ">
                </div>
            </div>
        </form>
    </function_cell>
{% endblock context_area %}

{% block script_area %}
{% trans '小時' as hour %}
{% trans '分' as minute %}
{% trans '秒' as second %}
{% trans '目前進度：' as completion_rate %}
<script>
    vue_sidebar.now_page = '{{ caller }}';
    title_area.introduction.content = "{% trans '參數設定完成後，即可按下執行開始進行去識別化' %}";
    title_area.introduction.is_chinese = '{{ LANGUAGE_CODE }}' === 'zh-hant';
</script>

<script>
    var SetMinute = 0;
    var progress_bar_jquary = $('.progress-bar');
    var progress_text_jquary = $('.progress-text');
    var execute_jquary = $('#execute');
    var now_progress = 0;
    
    function success(sitv, mm) {
        clearInterval(sitv);
        clearInterval(mm);
        progress_bar_jquary.css('width', '100%');
        progress_bar_jquary.text('100%');
        $('#bar').removeClass('active');
        progress_text_jquary.text("{% trans '執行完成' %}");
        execute_jquary.removeAttr('disabled');
        success_alert("{% trans '檔案執行完畢' %}");
        $(window).off();
        window.location = '{{ finish_url }}';
    }
    
    function check_time() {
        SetMinute += 1;
        var Check_i = document.getElementById("Check_i");
        var Cal_Hour = Math.floor(SetMinute / 3600);
        var Cal_Minute = Math.floor(Math.floor(SetMinute % 3600) / 60);
        var Cal_Second = SetMinute % 60;
        Check_i.innerHTML = Cal_Hour + ' {{ hour }} ' + Cal_Minute + ' {{ minute }} ' + Cal_Second + ' {{ second }}';
    }
    
    function reset() {
        SetMinute = 0;
        progress_bar_jquary.css('width', 0 + '%');
        progress_bar_jquary.text(0 + '%');
        progress_text_jquary.text('{{ completion_rate }}');
        progress_text_jquary.css('width', '100%');
        $('#prog_in').width(0 + '%');
    }
    
    function progress_check() {
        var prog_url = '{{ show_progress_url }}'
        $.getJSON(prog_url, function (data) {
            {# console.log("come in num_progress="+num_progress)#}
            $('.progress-div').css('visibility', 'visible');
            now_progress = data.num_progress;
            progress_bar_jquary.css('width', data.num_progress + '%');
            progress_bar_jquary.text(data.num_progress + '%');
            progress_text_jquary.text('{{ completion_rate }}'+ data.log);
            progress_text_jquary.css('width', '100%');
            $('#prog_in').width(data.num_progress + '%');
        });
    }
    
    $(function () {
        var url = "{% url 'check_file_status' %}"
        $.getJSON(url, function (request) {
            if (request == null) {
                return;
            }
            if (request.finish == true) {
                window.location = request.url;
            } else if (request.finish == false) {
                reset()
                window.scrollTo(0, document.body.scrollHeight)
                execute_jquary.attr('disabled', 'disabled');
                progress_check()
                var mm = window.setInterval("check_time()", 1000);
                var sitv = window.setInterval("progress_check()", 10000);
                var success_check = window.setInterval( function () {
                    if (now_progress == 100) {
                        clearInterval(success_check);
                        success(sitv, mm);
                    }
                }, 10000);
            }
        })
    })
    
    function execute() {
        reset()
        window.scrollTo(0, document.body.scrollHeight)
        execute_jquary.attr('disabled', 'disabled');
        var mm = window.setInterval('check_time()', 1000);
        var sitv = window.setInterval('progress_check()', 10000);
        var url = '{{ execute_url }}'
        var data = {csv_name : '{{ file_name }}'}
        {% for field in form %}
            data['{{ field.html_name }}'] = $('#{{ field.auto_id }}').val()
        {% endfor %}
        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            success: function () {
                success(sitv, mm);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                var jsonObj = JSON.parse(xhr.responseText);
                clearInterval(sitv);
                clearInterval(mm);
                progress_text_jquary.text("{% trans '執行失敗' %}");
                execute_jquary.removeAttr('disabled');
                danger_alert(jsonObj.message);
            }
        });
    }
</script>
{% endblock script_area %}