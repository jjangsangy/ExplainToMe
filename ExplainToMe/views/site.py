from flask import (Blueprint, flash, make_response, redirect, render_template,
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


@site.route('/webhook', methods=['POST'])
def webhook():
    sig = request.headers("x-hub-signature", '')
    if not sig:
        return {"error": "could not validate signature"}
    return redirect(url_for('site.index'), code=200)


@site.route('/summary', methods=['POST'])
def summary():
    language = 'english'
    url = request.form.get('url', '')
    max_sent = int(request.form.get('max_sent', 10))
    tokenizer = Tokenizer(language)
    parser, meta = get_parser(url, tokenizer)
    summary = run_summarizer(parser, max_sent, language)
    session_data = dict(
        summary=summary,
        url=url,
        meta=meta,
        max_sent=max_sent
    )
    session.update(session_data)
    return redirect(url_for('site.index', _anchor='summary'))


@site.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           url=session.get('url'),
                           meta=session.get('meta'),
                           summary=session.get('summary'),
                           max_sent=session.get('max_sent'),
                           form=LinkForm())
