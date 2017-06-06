
from sumy.nlp.tokenizers import Tokenizer

from .. textrank import get_parser, run_summarizer


def get_summary(url, max_sent=10, language='english'):
    tokenizer = Tokenizer(language)
    parser, meta = get_parser(url, tokenizer)
    summary = run_summarizer(parser, max_sent, language)
    return dict(
        summary=summary,
        url=url,
        meta=meta,
        max_sent=max_sent
    )
