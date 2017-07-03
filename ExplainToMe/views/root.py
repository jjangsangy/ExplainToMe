import json

try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap

from sumy.nlp.tokenizers import Tokenizer
from flask import Blueprint, render_template, request, session
from flask import current_app as app

try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap

from .. forms import LinkForm
from .. textrank import get_parser, run_summarizer

root = Blueprint('root', __name__)

@root.route('/', methods=['GET', 'POST'])
def index():
    form = LinkForm()
    if form.validate_on_submit():
        url, max_sent = request.form.get('url'), request.form.get('max_sent')
        language = 'english'
        parser, meta = get_parser(url, Tokenizer(language))
        new_meta = meta.pop('meta', {})
        meta.update(new_meta)
        session['summary'] = run_summarizer(parser, max_sent, language=language)
        session['url'] = url
        session['max_sent'] = max_sent
        session['meta'] = meta
        session['favicon'] = meta.get('favicon', '/favicon.ico')

    return render_template('index.html',
                           form=form,
                           url=session.get('url'),
                           max_sent=session.get('max_sent'),
                           summary=session.get('summary'),
                           meta=session.get('meta', {}),
                           favicon=session.get('favicon', '/favicon.ico'))
