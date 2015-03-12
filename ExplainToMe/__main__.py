# -*- coding: utf8 -*-
from __future__ import print_function

from argparse import ArgumentParser

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from .__version__ import __version__, __build__

from .models import HtmlParser

__all__ = (
    'summarizer',
)



def summarizer(parser, sentences, language='english'):
    """
    :params parser: Parser for selected document type
    :params sentences: Maximum sentences for summarizer.

    :returns summary: Summarized page.
    """
    stemmer    = Stemmer(language)
    summarizer = Summarizer(stemmer)

    summarizer.stop_words = get_stop_words(language)

    output = [str(sentence) for sentence in summarizer(parser.document, sentences)]

    return ' '.join(output)


def command_line():
    """
    Parses command line arguments.

    Returns
    =======
    :returns: Namespace containing parsed arguments
    :rtype  : argparse.ArgumentParser
    """
    description = 'A Text Summarizer for Humans'
    version = ' '.join([__version__, __build__])

    parser = ArgumentParser(prog='ExplainToMe', description=description)

    parser.add_argument('-v', '--version',
                        action='version',
                        version="{name} v{version}".format(name='ExplainToMe', version=version))

    parser.add_argument('url',
                        type=str,
                        default='http://wikipedia.org/wiki/Automatic_summarization',
                        help='Summarize website contents.')

    parser.add_argument('limit',
                        type=int,
                        default=10,
                        help='Give a sentence limit')

    parser.add_argument('--language',
                        type=str,
                        default='english',
                        help='This feature is still in testing')

    return parser.parse_args()


def main():
    """
    Main application entry point. This is the part that will be run
    by the command line tool.

    Returns:
    ========
    :returns: Upon successful completion returns 0
    :rtype  : int
    """
    language   = 'english'
    args       = command_line()
    tokenizer  = Tokenizer(language)

    limit  = args.limit
    url    = args.url

    parser = HtmlParser.from_url(url, tokenizer)

    summary = summarizer(parser, limit, language)

    print(summary)

    return 0
