{% extends "base.vue" %}
{% load i18n %}
{% block title %}update log{% endblock title %}
{% block context_area %}
    <function_cell
        :function_object = "{
            name: {
                content: '{% trans '最新更新 8/5 ver 0.3.1' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '調整項目：' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '1. 程式資源取得方式更改：CDN → 直接載入' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
    </function_cell>
    
    <function_cell
        :function_object = "{
            name: {
                content: '8/4 ver 0.3',
                is_chinese: false,
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '調整項目：' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '1. 字串關係配對顯示方式更改：瀑布式排列 → 折疊式排列' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '2. 數字自訂區間顯示方式更改：瀑布式排列 → 折疊式排列' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '3. 新增/刪除按鈕顯示方式更改：文字 → 圖片' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '4. 字串關係配對，刪除欄位方式最佳化：只能刪除最後一列 → 可任意刪除任意列' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '5. 數字自訂區間，設定區間方式最佳化：先輸入區間數量後產生區間 → 直接產生區間，並使用新增區間按鈕來增加區間' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
    </function_cell>
    
    <function_cell
        :function_object = "{
            name: {
                content: '7/29 ver 0.2',
                is_chinese: false,
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '新增項目：' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '1. 去識別化進度記錄，現在只需按下執行，就可以關閉網頁，下次進入網站時，將會引導到目前所執行的進度' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '調整項目：' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '1. 等候提示：文字 → 轉圈圈' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '2. 進度條%數顯示：完成度粗分 → 細分' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '3. 錯誤提示方式：彈出式視窗 → 置頂公告' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '4. 執行頁面bug修復，排除特定情況下進度條倒退、執行失敗等bug' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
    </function_cell>
    
    <function_cell
        :function_object = "{
            name: {
                content: '7/21 ver 0.1',
                is_chinese: false,
            },
        }"
    >
        <cell_introduction
            :introduction = "{
                content: '{% trans '新增項目：' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '1. 公佈欄' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '2. 更新日誌' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '3. 更改密碼功能' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '調整項目：' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '1. 檔案上傳限制：無上限 → 4MB' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '2. 勾選框操作：勾選時其餘選項鎖定 → 可自由切換勾選的內容' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '3. 字串關係配對：循環配對時，將引起程式卡死 → 檢測到循環就跳出視窗提示' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '4. 字串關係配對：配對時最高層關係沒配對自己，引起程式錯誤 → 程式將自動配對最高層關係' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '5. 字串關係配對：刪除自訂欄位時，如果自訂欄位沒有輸入內容則會刪除失敗 → 可在任意狀況下刪除' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
        ></cell_introduction>
        <cell_introduction
            :introduction = "{
                content: '{% trans '6. 可用度檢測：選擇所用方法後就會立刻執行 → 需按下確認後才會執行' %}',
                is_chinese: '{{ LANGUAGE_CODE }}' === 'zh-hant',
            }"
            end_introduction = true
        ></cell_introduction>
    </function_cell>
{% endblock context_area %}

{% block script_area %}
<script>
    vue_sidebar.now_page = 'update_log';
    title_area.title.content = "{% trans '更新日誌' %}";
    title_area.title.is_chinese = '{{ LANGUAGE_CODE }}' === 'zh-hant';
    title_area.introduction.content = "{% trans '日誌依照版本號由新到舊排序' %}";
    title_area.introduction.is_chinese = '{{ LANGUAGE_CODE }}' === 'zh-hant';    
</script>
{% endblock script_area %}