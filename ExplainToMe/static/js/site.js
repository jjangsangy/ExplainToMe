(function () {
    'use strict';
    var label = Array.prototype.slice.call(document.body.querySelectorAll('label'));
    label.forEach(function (items) {
        items.className = 'sr-only';
    });
    $("#input-form").each(function () {
        this.preventNextSubmit = true;
    }).submit(function (event) {
        var form = $(this);
        if (this.preventNextSubmit) {
            this.preventNextSubmit = false;
            event.preventDefault();
            $('#loader').slideToggle({duration: 400, complete: form.slideToggle(800), always: form.submit()});
        }
    });
})();
