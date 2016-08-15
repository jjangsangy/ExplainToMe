var ExplainToMe = (function(document) {
    'use strict';
    document.body.querySelectorAll("label").forEach(
        function(item) {
            item.className = 'sr-only';
        }
    );
    document.body.getElementById("input-form").addEventListener("submit", function (e) {
        $("#input-form").fadeOut("slow");
        $("#loader").fadeIn("slow");
    });
})(document);
