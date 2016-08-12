"""
Main
=====
"""

import click
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

from .textrank import alt_extract, get_summarizer


@click.command()
@click.argument('url')
@click.option('--max-sent', default=10, help='The maximum number of sentences')
@click.option('--language', default='english', help='Article language')
def main(url, max_sent, language='english'):
    tokenizer = Tokenizer(language)
    article = alt_extract(url)
    parser = PlaintextParser.from_string(article, tokenizer)
    return click.echo(get_summarizer(parser, max_sent, language))


if __name__ == '__main__':
    main()
