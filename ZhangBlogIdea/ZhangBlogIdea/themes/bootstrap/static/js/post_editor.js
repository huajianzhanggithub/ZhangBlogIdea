$(document).ready(function ($) {
    var $content_md = $('.form-row.field-content_md');
    var $content_ck = $('.form-row.field-content_ck');
    var $is_md = $('#id_is_md');
    var switch_editor = function (is_md) {
        if (is_md) {
            $content_md.show();
            $content_ck.hide();
        } else {
            $content_md.hide();
            $content_ck.show();
        }
    }
    $is_md.on('click', function () {
        switch_editor($(this).is(':checked'));
    });
    switch_editor($is_md.is(':checked'));
});