# -*- coding: utf8 -*-
from __future__ import print_function

import requests
from breadability.readable import Article
from requests import Request, Session
from requests.adapters import HTTPAdapter
from sumy.models.dom import ObjectDocumentModel, Paragraph, Sentence
from sumy.nlp.stemmers import Stemmer
from sumy.parsers.parser import DocumentParser
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.utils import cached_property, get_stop_words

from six.moves import urllib

from .webapi import HTTPURLEndpoints

try:
    from http.cookiejar import CookieJar
    from urllib.parse import urlencode
except ImportError:
    from cookielib import CookieJar
    from urllib import urlencode


class Client:

    def __init__(self, key=None):
        self.__key = key

    def __repr__(self):
        classname = self.__class__.__name__
        return '%s(key=%r)' % (classname, 'KEY' if self.key else None)

    def is_valid(self):
        if not self.key:
            return False
        assert isinstance(self.key, str)
        assert len(self.key) == 40
        return True

    @property
    def key(self):
        return self.__key


class AlchemyAPI:

    def __init__(self, client, base='http://access.alchemyapi.com/calls'):
        self.base = base
        self.client = client
        self.session = requests.session()
        self.endpoint = HTTPURLEndpoints.build_endpoints()

    def text(self, flavor, data, options={}):
        """
        Extracts the cleaned text (removes ads, navigation, etc.)
            for text, a URL or HTML.
        For an overview, please refer to:
            http://www.alchemyapi.com/products/features/text-extraction/
        For the docs, please refer to:
            http://www.alchemyapi.com/api/text-extraction/

        Input:
        ======
        :param flavor: str
            Which version of the call ['text', 'url', 'html']
        :param data:
            The data to analyze, either the text, the url or html code.
        :param options:
            various parameters that can be used to adjust how the API works,

        Available Options:
        ==================
        :option useMetadata: utilize meta description data
                          0: disabled
                          1: enabled (default)
        :option extractLinks: include links
                          0: disabled (default)
                          1: enabled

        Output:
        =======
        :return response: JSON
            The response, already converted from JSON to a Python object
        """
        # Make sure this request supports this flavor
        if flavor not in self.endpoint['text']:
            return {'status': 'ERROR',
                    'statusInfo':
                    'clean text extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data

        return self.connect(self.endpoint['text'][flavor], options)

    def connect(self, endpoint, params, post_data=bytearray()):
        """
        HTTP Request wrapper that is called by the endpoint functions.
        This function is not intended to be called through an
        external interface.
        It makes the call, then converts the
        returned JSON string into a Python object.

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object.
        """

        # Add the API Key and set the output mode to JSON
        params['apikey'] = self.client.key
        params['outputMode'] = 'json'
        # Insert the base url

        post_url = ""
        try:
            post_url = self.base + endpoint + \
                '?' + urllib.parse.urlencode(params).encode('utf-8')
        except TypeError:
            post_url = self.base + endpoint + '?' + urlencode(params)

        results = ""
        try:
            results = self.session.post(url=post_url, data=post_data)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}


class HtmlParser(DocumentParser):
    """Parser of text from HTML format into DOM."""

    SIGNIFICANT_TAGS = ('h1', 'h2', 'h3', 'b'
                        'strong', 'big', 'dfn', 'em', 'p')

    @classmethod
    def from_string(cls,
                    string,
                    url,
                    tokenizer, ):
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
                'Chrome/23.0.1271.64 Safari/537.11'
            ]),
            'Accept': ','.join([
                'text/html', 'application/xhtml+xml', 'application/xml;q=0.9',
                '*/*;q=0.8'
            ]),
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        session = Session()

        session.mount('http://', HTTPAdapter(max_retries=2))
        session.mount('https://', HTTPAdapter(max_retries=2))

        cookies = CookieJar()
        request = Request(method='GET',
                          url=url,
                          headers=headers,
                          cookies=cookies)
        prepare = session.prepare_request(request)
        response = session.send(prepare, verify=True)

        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        return cls(response.text, tokenizer, url)

    def __init__(self, html_content, tokenizer, url=None):
        super(HtmlParser, self).__init__(tokenizer)
        self._article = Article(html_content, url)

    @cached_property
    def significant_words(self):
        words = []
        for paragraph in self._article.main_text:

            for (text, annotations) in paragraph:
                if not self._contains_any(annotations, *self.SIGNIFICANT_TAGS):
                    continue
                words.extend(self.tokenize_words(text))

        if words:
            return tuple(words)
        else:
            return self.SIGNIFICANT_WORDS

    @cached_property
    def stigma_words(self):
        words = []
        for paragraph in self._article.main_text:
            for (text, annotations) in paragraph:
                if self._contains_any(annotations, 'a', 'strike', 's'):
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
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)

    summarizer.stop_words = get_stop_words(language)

    output = [str(sentence)
              for sentence in summarizer(parser.document, sentences)]

    return ' '.join(output)
