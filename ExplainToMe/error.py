from flask import render_template, request, current_app, session
from flask_wtf.csrf import CSRFError
from flask import current_app as app

def error_not_found(e):
    app.logger.error('Not Found: {}'.format(request.url))
    return render_template('404.html')
