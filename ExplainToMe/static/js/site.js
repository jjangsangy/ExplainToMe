let label = Array.from(document.body.querySelectorAll('label'));
label.forEach(function (items) {
    items.className = 'sr-only';
});

document.getElementById('input-form').addEventListener('submit', function (e) {
    $('#input-form').fadeOut('slow');
    $('#loader').fadeIn('slow');
});
