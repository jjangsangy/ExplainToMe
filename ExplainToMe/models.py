# -*- coding: utf8 -*-

import json
import requests
import math

from requests import Request, Session
from requests.adapters import HTTPAdapter

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

from breadability.readable import Article
from sumy.utils import cached_property
from sumy.models.dom import Sentence, Paragraph, ObjectDocumentModel
from sumy.parsers.parser import DocumentParser


__all__ = [
    'HtmlParser',
]


class HtmlParser(DocumentParser):

    """Parser of text from HTML format into DOM."""

    SIGNIFICANT_TAGS = (
        'h1',
        'h2',
        'h3',
        'b'
        'strong',
        'big',
        'dfn',
        'em',
        'p'
        )

    @classmethod
    def from_string(
        cls,
        string,
        url,
        tokenizer,
        ):
        return cls(string, tokenizer, url)

    @classmethod
    def from_file(
        cls,
        file_path,
        url,
        tokenizer,
        ):
        with open(file_path, 'rb') as file:
            return cls(file.read(), tokenizer, url)

    @classmethod
    def from_url(cls, url, tokenizer):
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        session  = Session()

        session.mount('http://',  HTTPAdapter(max_retries=2))
        session.mount('https://', HTTPAdapter(max_retries=2))

        cookies  = CookieJar()
        request  = Request(method='GET', url=url, headers=headers, cookies=cookies)
        prepare  = session.prepare_request(request)
        response = session.send(prepare, verify=True)

        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        return cls(response.text, tokenizer, url)

    def __init__(
        self,
        html_content,
        tokenizer,
        url=None,
        ):
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
      # "a", "abbr", "acronym", "b", "big", "blink", "blockquote", "cite", "code",
      # "dd", "del", "dfn", "dir", "dl", "dt", "em", "h", "h1", "h2", "h3", "h4",
      # "h5", "h6", "i", "ins", "kbd", "li", "marquee", "menu", "ol", "pre", "q",
      # "s", "samp", "strike", "strong", "sub", "sup", "tt", "u", "ul", "var",

        headers        = 'h1', 'h2', 'h3'
        annotated_text = self._article.main_text
        paragraphs     = []

        for paragraph in annotated_text:
            sentences, current_text = [], ''

            for (text, annotations) in paragraph:

                if annotations and any(h_tag in annotations for h_tag in headers):
                    sentences.append(Sentence(text, self._tokenizer, is_heading=True))

                elif not (annotations and 'pre' in annotations):
                    # skip <pre> nodes
                    current_text += ' ' + text

            new_sentences = self.tokenize_sentences(current_text)
            sentences.extend(Sentence(s, self._tokenizer) for s in new_sentences)
            paragraphs.append(Paragraph(sentences))

        return ObjectDocumentModel(paragraphs)
