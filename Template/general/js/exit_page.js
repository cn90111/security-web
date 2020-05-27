<script>
    window.onbeforeunload = function(e) {
      var dialogText = '離開此頁面後，檔案與設定皆不會保留，確定要離開嗎?';
      e.returnValue = dialogText;
      return dialogText;
    };
    
    
</script>