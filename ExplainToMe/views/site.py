from flask import (Blueprint, make_response, redirect, render_template,
                   request, session, url_for)
from sumy.nlp.tokenizers import Tokenizer
from wtforms.validators import URL

from ..forms import LinkForm
from ..textrank import get_parser, run_summarizer

site = Blueprint('site', __name__)


def valid_url(raw_url):
    validator = URL()
    match = validator.regex.match(raw_url)
    if not match:
        return False
    return validator.validate_hostname(match.group('host'))


@site.route('/summary', methods=['POST'])
def summary():
    language = 'english'
    url = request.form.get('url', '')
    max_sent = int(request.form.get('max_sent', 10))
    tokenizer = Tokenizer(language)
    parser, meta = get_parser(url, tokenizer)
    summary = run_summarizer(parser, max_sent, language)
    session.update(dict(summary=summary, url=url, meta=meta))
    return redirect(url_for('site.index'))


@site.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', url=session.get('url'), meta=session.get('meta'), summary=session.get('summary'), form=LinkForm())
