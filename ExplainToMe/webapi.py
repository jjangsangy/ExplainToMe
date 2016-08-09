from collections import defaultdict

import requests

from six.moves import urllib

try:
    from http.cookiejar import CookieJar
    from urllib.parse import urlencode
except ImportError:
    from cookielib import CookieJar
    from urllib import urlencode


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


class HTTPURLEndpoints(defaultdict):

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return self.__getitem__(key)

    def __setattr__(self, name, value):
        if hasattr(HTTPURLEndpoints, name):
            raise AttributeError()
        else:
            self[name] = value

    def __getitem__(self, name):
        if name not in self:
            self[name] = HTTPURLEndpoints()
        return super(HTTPURLEndpoints, self).__getitem__(name)

    def serialize(self):
        base = {}
        if '_ipython_display_' in self:
            self.pop('_ipython_display_')
        if '_getAttributeNames' in self:
            self.pop('_getAttributeNames')
        if 'trait_names' in self:
            self.pop('trait_names')
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.serialize()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(item.serialize() if
                                        isinstance(item, type(self)) else item
                                        for item in value)
            else:
                base[key] = value
        return base

    @classmethod
    def build_endpoints(cls):

        webapi = HTTPURLEndpoints()

        webapi.sentiment.url = '/url/URLGetTextSentiment'
        webapi.sentiment.text = '/text/TextGetTextSentiment'
        webapi.sentiment.html = '/html/HTMLGetTextSentiment'
        webapi.sentiment_targeted.url = '/url/URLGetTargetedSentiment'
        webapi.sentiment_targeted.text = '/text/TextGetTargetedSentiment'
        webapi.sentiment_targeted.html = '/html/HTMLGetTargetedSentiment'
        webapi.author.url = '/url/URLGetAuthor'
        webapi.author.html = '/html/HTMLGetAuthor'
        webapi.keywords.url = '/url/URLGetRankedKeywords'
        webapi.keywords.text = '/text/TextGetRankedKeywords'
        webapi.keywords.html = '/html/HTMLGetRankedKeywords'
        webapi.concepts.url = '/url/URLGetRankedConcepts'
        webapi.concepts.text = '/text/TextGetRankedConcepts'
        webapi.concepts.html = '/html/HTMLGetRankedConcepts'
        webapi.entities.url = '/url/URLGetRankedNamedEntities'
        webapi.entities.text = '/text/TextGetRankedNamedEntities'
        webapi.entities.html = '/html/HTMLGetRankedNamedEntities'
        webapi.category.url = '/url/URLGetCategory'
        webapi.category.text = '/text/TextGetCategory'
        webapi.category.html = '/html/HTMLGetCategory'
        webapi.relations.url = '/url/URLGetRelations'
        webapi.relations.text = '/text/TextGetRelations'
        webapi.relations.html = '/html/HTMLGetRelations'
        webapi.language.url = '/url/URLGetLanguage'
        webapi.language.text = '/text/TextGetLanguage'
        webapi.language.html = '/html/HTMLGetLanguage'
        webapi.text.url = '/url/URLGetText'
        webapi.text.html = '/html/HTMLGetText'
        webapi.text_raw.url = '/url/URLGetRawText'
        webapi.text_raw.html = '/html/HTMLGetRawText'
        webapi.title.url = '/url/URLGetTitle'
        webapi.title.html = '/html/HTMLGetTitle'
        webapi.feeds.url = '/url/URLGetFeedLinks'
        webapi.feeds.html = '/html/HTMLGetFeedLinks'
        webapi.microformats.url = '/url/URLGetMicroformatData'
        webapi.microformats.html = '/html/HTMLGetMicroformatData'
        webapi.combined.url = '/url/URLGetCombinedData'
        webapi.combined.text = '/text/TextGetCombinedData'
        webapi.image.url = '/url/URLGetImage'
        webapi.imagetagging.url = '/url/URLGetRankedImageKeywords'
        webapi.imagetagging.image = '/image/ImageGetRankedImageKeywords'
        webapi.facetagging.url = '/url/URLGetRankedImageFaceTags'
        webapi.facetagging.image = '/image/ImageGetRankedImageFaceTags'
        webapi.taxonomy.url = '/url/URLGetRankedTaxonomy'
        webapi.taxonomy.html = '/html/HTMLGetRankedTaxonomy'
        webapi.taxonomy.text = '/text/TextGetRankedTaxonomy'

        return webapi.serialize()


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
