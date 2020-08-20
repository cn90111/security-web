{% load i18n %}
<function_cell
    :function_object = "{
        name: {
            content: '{{ title }}{% trans '(前200筆)' %}',
            is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
        },
    }"
    remove_padding = true
>
    <div class="modal-body">
        <div id={{ id }} aligh="center" style = "height:250px; overflow:scroll; border:2px black solid; " >
        </div>
    </div>
</function_cell>
    
<script>
$(function () {
    var display_table = $('#{{ id }}');
    var url = '{{ display_url }}';
    $.getJSON(url, {
            'File' : '{{ file_name }}',
        }, function (table) {
            display_table.html(table);
        }
    )
});
</script>