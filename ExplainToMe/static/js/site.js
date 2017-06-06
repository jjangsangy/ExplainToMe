{
    let inputForm = document.getElementById("input-form");
    inputForm.addEventListener('submit', function cb(event)  {
        var form = $(this);
        if (this.hasAttribute('animated')) {
            event.preventDefault();
            this.removeAttribute('animated')
            $('#loader').slideToggle({duration: 400, complete: form.slideToggle(800), always: form.submit()});
        }
    });

    $('body').attr('data-spy', 'scroll').scrollspy({target: '#bs-example-navbar-collapse-1'})
}
