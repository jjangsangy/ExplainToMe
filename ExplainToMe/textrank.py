# -*- coding: utf8 -*-
from __future__ import print_function

import requests
import six
from breadability.readable import Article
from goose import Goose
from sumy.models.dom import ObjectDocumentModel, Paragraph, Sentence
from sumy.nlp.stemmers import Stemmer
from sumy.parsers.parser import DocumentParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.utils import cached_property, get_stop_words
from itertools import chain
from sumy.nlp.tokenizers import Tokenizer

from iso639 import languages

if six.PY2:
    str = six.text_type


class HtmlParser(DocumentParser):
    """
    Parser of text from HTML format into DOM.
    """
    SIGNIFICANT_TAGS = (
        'h1', 'h2', 'h3', 'b', 'i' 'blockquote',
        'strong', 'big', 'dfn', 'em', 'p'
    )

    @classmethod
    def from_string(cls, string, url, tokenizer):
        return cls(string, tokenizer, url)

    @classmethod
    def from_file(cls, file_path, url, tokenizer):
        with open(file_path, 'rb') as file:
            return cls(file.read(), tokenizer, url)

    @classmethod
    def from_url(cls, url, tokenizer,
                 useragent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',  # noqa
                 **kwargs):
        headers = {
            'Accept-Encoding': 'identity, deflate, compress, gzip',
            'Accept': '*/*',
            'User-Agent': useragent,
        }
        response = requests.get(url=url,
            headers=dict(chain(headers.items(), kwargs.items()))
        )
        return cls(response.text, tokenizer, url)

    def __init__(self, html_content, tokenizer, url=None):
        super(HtmlParser, self).__init__(tokenizer)
        self._article = Article(html_content, url)

    @cached_property
    def significant_words(self):
        words = []
        for paragraph in self._article.main_text:
            for text, annotations in paragraph:
                if not self._contains_any(annotations, *self.SIGNIFICANT_TAGS):
                    continue
                words.extend(self.tokenize_words(text))
        return tuple(words) if words else self.SIGNIFICANT_WORDS

    @cached_property
    def stigma_words(self):
        words = []
        for paragraph in self._article.main_text:
            for (text, annotations) in paragraph:
                if self._contains_any(annotations, 'a', 'strike', 's', 'span'):
                    words.extend(self.tokenize_words(text))
        return tuple(words) if words else self.STIGMA_WORDS

    def _contains_any(self, sequence, *args):
        if sequence is None:
            return False
        return any([True for item in args if item in sequence])

    @cached_property
    def document(self):
        # a abbr acronym b big blink blockquote cite code
        # dd del dfn dir dl dt em h h1 h2 h3 h4
        # h5 h6 i ins kbd li marquee menu ol pre q
        # s samp strike strong sub sup tt u ul var
        headers, annotated_text = ('h1', 'h2', 'h3'), self._article.main_text
        paragraphs = []
        for paragraph in annotated_text:
            sentences, current_text = list(), str()
            for text, annotations in paragraph:
                if annotations and any(h_tag in annotations for h_tag in headers):  # noqa
                    sentences.append(Sentence(text, self._tokenizer, is_heading=True))  # noqa
                # Skip <pre> Tags
                elif not (annotations and 'pre' in annotations):  # noqa
                    current_text += ' ' + text
            new_sentences = self.tokenize_sentences(current_text)
            sentences.extend(Sentence(s, self._tokenizer) for s in new_sentences)  # noqa
            paragraphs.append(Paragraph(sentences))

        return ObjectDocumentModel(paragraphs)


def run_summarizer(parser, sentences, language='english'):
    """
    :params parser: Parser for selected document type
    :params sentences: Maximum sentences for summarizer.

    :returns summary: Summarized page.
    """

    summarizer = Summarizer(Stemmer(language))
    summarizer.stop_words = get_stop_words(language)
    return [str(sentence)
            for sentence in summarizer(parser.document, sentences)]


def get_lang(name):
    return languages.inverted.get(name.title()).part1

def get_parser(url, language):
    tokenizer = Tokenizer(language)
    useragent = ' '.join([
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)",
        "AppleWebKit/537.36 (KHTML, like Gecko)",
        "Chrome/52.0.2743.116 Safari/537.36"])

    twitter_bypass = ['wsj.com']
    extra_headers = {}

    if any(i for i in twitter_bypass if i in url):
        extra_headers['Referer'] = r'https://t.co/T1323aaaa'
    # Scrape Web Page With HTMLParser and Goose and select the best scrape
    html_parser = HtmlParser.from_url(url, tokenizer, **extra_headers)
    article = Goose({'browser_user_agent': useragent, 'target_language': get_lang(language)})

    # Goose raises IndexError when requesting unfamiliar sites.
    try:
        extract = article.extract(url=url)
    except:
        req = requests.get(url)
        print(req.apparent_encoding)
        extract = article.extract(
            raw_html=req.content.decode(encoding=req.apparent_encoding)
        )

    goose_parser = PlaintextParser(extract, tokenizer)

    # Aggregate Site Metadata
    meta = {
        k: v for (k, v) in extract.infos.items()
        if k not in ('cleaned_text', 'links', 'tweets', 'movies')
    }
    # Select Best Parser
    parser = (
        html_parser
        if len(goose_parser.document.words) < len(html_parser.document.words) else  # noqa
        goose_parser)

    return parser, meta
