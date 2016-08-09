from flask import Blueprint, render_template, request
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

from ..forms import LinkForm
from ..textrank import alt_extract, summarizer

site = Blueprint('site', __name__)


@site.route('/')
def index():
    form = LinkForm()
    return render_template('index.html', form=form)


@site.route('/summary', methods=['POST'])
def summary():
    max_sent = 10
    language = 'english'
    url = request.form['summary']
    tokenizer = Tokenizer(language)
    article = alt_extract(url)
    parser = PlaintextParser.from_string(article, tokenizer)
    summary = summarizer(parser, max_sent, language).decode('utf-8')
    return render_template('summary.html', url=url, summary=summary)
