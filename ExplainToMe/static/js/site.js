(function () {
    'use strict';
    var label = Array.prototype.slice.call(document.body.querySelectorAll('label'));
    label.forEach(function (items) {
        items.className = 'sr-only';
    });
    $("#input-form").each(function () {
        this.preventNextSubmit = true;
    }).submit(function (event) {
        if (this.preventNextSubmit) {
            this.preventNextSubmit = false;
            event.preventDefault();
            var form = $(this);
            $('#loader').slideToggle("fast", function () {
                form.slideToggle("slow", function () {
                    form.submit();
                });
            });
        }
    });
})();
