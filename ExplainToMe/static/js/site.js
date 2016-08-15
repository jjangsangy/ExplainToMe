'use strict';

document.querySelectorAll("label").forEach(
    function(item) {
        item.className = 'sr-only';
    }
);

document.getElementById("input-form").addEventListener("submit", function (e) {
    $("#input-form").fadeOut();
    $("#loader").fadeIn();
});
