from flask import Blueprint, render_template, request
from sumy.nlp.tokenizers import Tokenizer

from ..forms import LinkForm
from ..textrank import HtmlParser, run_summarizer

site = Blueprint('site', __name__)


@site.route('/')
def index():
    form = LinkForm()
    return render_template('index.html', form=form)


@site.route('/summary', methods=['POST'])
def summary():
    language = 'english'
    url = request.form.get('url', '')
    max_sent = int(request.form.get('max_sent', 10))
    tokenizer = Tokenizer(language)
    parser = HtmlParser.from_url(url, tokenizer)
    summary = run_summarizer(parser, max_sent, language).decode('utf-8')
    return render_template('summary.html', url=url, summary=summary)
