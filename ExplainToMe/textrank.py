# -*- coding: utf8 -*-
from __future__ import print_function

import requests
import six
from breadability.readable import Article
from cachecontrol import CacheControl
from goose import Goose
from requests import Request, Session
from requests.adapters import HTTPAdapter
from requests.cookies import RequestsCookieJar
from sumy.models.dom import ObjectDocumentModel, Paragraph, Sentence
from sumy.nlp.stemmers import Stemmer
from sumy.parsers.parser import DocumentParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.utils import cached_property, get_stop_words

if six.PY2:
    str = unicode


class HtmlParser(DocumentParser):
    """
    Parser of text from HTML format into DOM.
    """
    SIGNIFICANT_TAGS = ('h1', 'h2', 'h3', 'b',
                        'strong', 'big', 'dfn', 'em', 'p')

    @classmethod
    def from_string(cls,
                    string,
                    url,
                    tokenizer):
        return cls(string, tokenizer, url)

    @classmethod
    def from_file(cls, file_path, url, tokenizer):
        with open(file_path, 'rb') as file:
            return cls(file.read(), tokenizer, url)

    @classmethod
    def from_url(cls, url, tokenizer):
        headers = {
            'User-Agent': ' '.join([
                'Mozilla/5.0 (X11; Linux x86_64)',
                'AppleWebKit/537.11 (KHTML, like Gecko)',
                'Chrome/23.0.1271.64 Safari/537.11',
            ]),
        }
        session = CacheControl(Session())
        session.mount('http://', HTTPAdapter(max_retries=2))
        session.mount('https://', HTTPAdapter(max_retries=2))
        request = Request(method='GET',
                          url=url,
                          headers=headers,
                          cookies=RequestsCookieJar())
        prepare = session.prepare_request(request)
        response = session.send(prepare, verify=True)

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

        if words:
            return tuple(words)

        else:
            return self.STIGMA_WORDS

    def _contains_any(self, sequence, *args):
        if sequence is None:
            return False

        for item in args:
            if item in sequence:
                return True

        return False

    @cached_property
    def document(self):
        # a abbr acronym b big blink blockquote cite code
        # dd del dfn dir dl dt em h h1 h2 h3 h4
        # h5 h6 i ins kbd li marquee menu ol pre q
        # s samp strike strong sub sup tt u ul var
        headers = 'h1', 'h2', 'h3'
        annotated_text = self._article.main_text
        paragraphs = []

        for paragraph in annotated_text:
            sentences, current_text = [], ''

            for (text, annotations) in paragraph:

                if annotations and any(h_tag in annotations
                                       for h_tag in headers):
                    sentences.append(Sentence(text,
                                              self._tokenizer,
                                              is_heading=True))

                elif not (annotations and 'pre' in annotations):
                    # skip <pre> nodes
                    current_text += ' ' + text

            new_sentences = self.tokenize_sentences(current_text)
            sentences.extend(Sentence(s, self._tokenizer)
                             for s in new_sentences)
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


def get_parser(url, tokenizer):
    article = Goose()
    try:
        g = article.extract(url=url)
    except IndexError:
        g = article.extract(raw_html=requests.get(url).text)
    meta = {
        k: v for (k, v) in g.infos.items()
        if k not in ('cleaned_text', 'links', 'tweets', 'movies')
    }
    html = HtmlParser.from_url(url, tokenizer)
    return (
        html
        if len(set(g.cleaned_text.split())) < len(html.document.words)
        else PlaintextParser(g.cleaned_text, tokenizer)
    ), meta
