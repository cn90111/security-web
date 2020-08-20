<!DOCTYPE html>
{% load i18n %}
{% load static %}

<style>
    @font-face {
        font-family:'Taipei_Sans_TC';
        src: url('{% static 'font/TaipeiSansTCBeta-Light.ttf' %}') format("truetype");
    }
</style>

<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>{% block title %}title{% endblock title %}</title>
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        <link rel="stylesheet" href="{% static 'css/vuesax.css' %}">
        <link rel="stylesheet" href="{% static 'css/shadow.css' %}">
        <link rel="stylesheet" href="{% static 'css/font.css' %}">
        <link rel="stylesheet" href="{% static 'css/line.css' %}">
    	<script src="{% static 'js/jquery-3.5.1.min.js' %}"></script>
    	<script src="{% static 'js/bootstrap.min.js' %}"></script>
        <script src="{% static 'js/vue.js' %}"></script>
    	<script src="{% static 'js/docs.min.js' %}"></script>
	</head>
    <body style="background-image: url('{% static 'img/vuesax_background.png' %}'); background-repeat:no-repeat; background-color:#f5f5f5;">
        <div id="alert" style="display:none" class="alert row justify-content-between" role="alert">
            <h3 id="alert_text"></h3>
            <button type="button" class="close" onclick="close_alert()" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="row" style="margin-right:0px;">
            <div class="col-md-3">
                {% include 'sidebar.vue' %}
            </div>
            <div class="col-md-9">
                <div class="container-fluid" id="title_area" style="background-color:#FFFFFF; height:100px;">
                    <h1 style="color:#921AFF;" class="row justify-content-center align-items-center" :class="font_class(title.is_chinese)">[[ title.content ]]</h1>
                    <p style="color:#5B5B5B; padding-top:7px;" class="row justify-content-center align-items-center top_gray_line" :class="font_class(title.is_chinese)">[[ introduction.content ]]</p>
                </div>
                <div style="padding-top:10px">
                    <div id="function_list" class="container-fluid" style="padding-right:15px; padding-left:15px;">
                        {% block context_area %}{% endblock context_area %}
                    </div>
                </div>
            </div>
        </div>
        {% block footer_area %}{% endblock footer_area %}        
        <script>
            Vue.component('vue_button', {
                delimiters: ['[[', ']]'],
                props: ['url', 'event', 'button_text'],
                data: function () {
                    return {
                        button_color: '#0000ff',
                    }
                },
                template: '\
                    <a :href=url :onclick=event class="btn-lg row justify-content-center align-items-center" :style="button_style" :class="font_class(button_text.is_chinese)">[[ button_text.content ]]</a>\
                ',
                computed: {
                    button_style () {
                        return 'color:' + this.button_color;
                    },
                },
                methods: {
                    font_class: function (is_chinese) {
                        if (is_chinese) {
                            return 'chinese_font';
                        } else {
                            return 'english_font';
                        }
                    },
                },
            });
            
            Vue.component('cell_introduction', {
                delimiters: ['[[', ']]'],
                props: ['introduction', 'end_introduction'],
                data: function () {
                    return {
                        font_color: '#5B5B5B',
                    }
                },
                template: '\
                    <h5 class="card-title" :class="font_class(introduction.is_chinese)" :style="font_style">[[ introduction.content ]]</h5>\
                ',
                computed: {
                    font_style () {
                        style = 'color:' + this.font_color + ';';
                        if (this.end_introduction) {
                            style += 'padding-bottom:10px;';
                        }
                        return style;
                    },
                },
                methods: {
                    font_class: function (is_chinese) {
                        if (is_chinese) {
                            return 'chinese_font';
                        } else {
                            return 'english_font';
                        }
                    },
                },
            });
                        
            new Vue({
                delimiters: ['[[', ']]'],
                el: '#function_list',
                data: {                
                    update_display: false,
                    release_display: false,
                },
                components: {
                    'function_cell': {
                        delimiters: ['[[', ']]'],
                        props: ['function_object', 'remove_padding'],
                        data: function () {
                            return {
                                header_color: '#f5f5f5',
                                body_color: '#ffffff',
                                font_color: '#5B5B5B',
                            }
                        },
                        template: '\
                            <div class="shadow mb-3" style="width:100%">\
                                <div class="card-header" :style="header_style">\
                                    <h2 :style="font_style" :class="font_class(function_object.name.is_chinese)">[[ function_object.name.content ]]</h2>\
                                </div>\
                                <div :style="body_style">\
                                    <slot></slot>\
                                </div>\
                            </div>\
                        ',
                        computed: {
                            header_style () {
                                return 'background-color:' + this.header_color;
                            },
                            body_style () {
                                style = 'background-color:' + this.body_color + ';';
                                if (!this.remove_padding) {
                                    style += 'padding:40px; padding-bottom:20px;';
                                }
                                return style;
                            },
                            font_style () {
                                return 'color:' + this.font_color;
                            },
                        },
                        methods: {
                            font_class: function (is_chinese) {
                                if (is_chinese) {
                                    return 'chinese_font';
                                } else {
                                    return 'english_font';
                                }
                            },
                        },
                    },
                },
            });
            
            var title_area = new Vue({
                delimiters: ['[[', ']]'],
                el: '#title_area',
                data: {
                    title: {
                        content: "title",
                        is_chinese: false,
                    },
                    introduction: {
                        content: "introduction",
                        is_chinese: false,
                    },
                },
                methods: {
                    font_class: function (is_chinese) {
                        if (is_chinese) {
                            return 'chinese_font';
                        } else {
                            return 'english_font';
                        }
                    },
                },
            });
        </script>
        
        <script>
            alert_jquery = $('#alert');
            alert_text_jquery = $('#alert_text');
            
            function initial_alert(text) {
                alert_jquery.removeClass()
                alert_jquery.addClass('alert row justify-content-between')
                alert_text_jquery.text(text)
                alert_jquery.show()
                window.scrollTo(0, 0)
            }
            
            function danger_alert(text) {
                initial_alert(text)
                alert_jquery.addClass('alert-danger')
            }
            
            function success_alert(text) {
                initial_alert(text)
                alert_jquery.addClass('alert-success')
            }
            
            function warning_alert(text) {
                initial_alert(text)
                alert_jquery.addClass('alert-warning')
            }
            
            function close_alert() {
                alert_jquery.hide()
            }
        </script>
        {% block script_area %}{% endblock script_area %}
	</body>
</html>